from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest

from gcal_sync import NONCE, calendar
from gcal_sync.gcp.event_util import dump_description

from ..calendar import Calendar as BaseCalendar
from ..calendar import CalendarProvider as BaseCalendarProvider
from ..calendar import CredentialInfo as BaseCredentialInfo
from ..event import Event as BaseEvent
from .event import Event, Record

LOGGER = logging.getLogger(__name__)


def access_token_path(dir_name: str, name: str) -> str:
    return os.path.join(dir_name, name + "-token.json")


def make_access_token(client_token_path: str, cred_dir: str, name: str):
    scopes = ['https://www.googleapis.com/auth/calendar']

    print(f"start making token for {name}")
    flow = InstalledAppFlow.from_client_secrets_file(
        client_token_path, scopes)
    creds = flow.run_local_server(port=0)
    if not isinstance(creds, Credentials):
        raise RuntimeError("unknown result from run_local_server")

    token_path = access_token_path(cred_dir, name)
    with open(token_path, 'w') as token:
        token.write(creds.to_json())


def get_service(creds: Credentials):
    ret = build('calendar', 'v3', credentials=creds)
    return ret


def get_credentials(cred_dir: str, name: str) -> Credentials:
    scopes = ['https://www.googleapis.com/auth/calendar']

    token_path = access_token_path(cred_dir, name)
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if creds is not None and creds.valid:
        return creds

    if creds is not None and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    else:
        raise RuntimeError("credential for %s is not valid" % name)

    return creds


def list_events(creds: Credentials, start_time: datetime, days: int, cal: BaseCalendar) -> list[Event]:
    service = get_service(creds)

    time_min = start_time
    time_max = time_min + timedelta(days=days)

    events_result = service.events().list(
        calendarId=cal.id,
        timeMin=time_min.isoformat(),
        timeMax=time_max.isoformat(),
        maxResults=days * 10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events: list[Record] = events_result.get('items', [])

    return [Event(cal, rec) for rec in events]


def http_callback(action: str, id2event: dict[str, dict[str, Any]], calendar: Calendar):
    def callback(id, _, ex):
        event = id2event[id]
        msg = f'{calendar.name}: {action} id={event.get("id")} summary={event["summary"]} start={event["start"]}'
        if ex is not None:
            LOGGER.warning("exception=%s msg=%s", ex, msg)
        else:
            LOGGER.info(msg)
    return callback


def delete_events_batch(creds: Credentials, calendar: Calendar, events: list[Event]) -> BatchHttpRequest:
    service = get_service(creds)
    id2event = {}

    batch = service.new_batch_http_request(
        callback=http_callback("delete", id2event, calendar))

    for i, e in enumerate(events):
        rec = e.record
        req_id = str(i+1)
        batch.add(
            service.events().delete(
                calendarId=calendar.id,
                eventId=rec["id"]
            ),
            request_id=req_id
        )
        id2event[req_id] = rec
    return batch


def create_events_batch(creds: Credentials, calendar: Calendar, events: list[Event]) -> BatchHttpRequest:
    service = get_service(creds)
    id2event = {}

    batch = service.new_batch_http_request(
        callback=http_callback("create", id2event, calendar))

    for i, e in enumerate(events):
        rec = e.record
        req_id = str(i+1)
        batch.add(
            service.events().insert(
                calendarId=calendar.id,
                body=e.record
            ),
            request_id=req_id
        )
        id2event[req_id] = rec
    return batch


class CredentialInfo(BaseCredentialInfo):
    def __init__(self, obj: Credentials) -> None:
        self.cred = obj


class CalendarProvider(BaseCalendarProvider):
    def authorize(self, client_info: str, cred_dir: str, name: str):
        make_access_token(client_info, cred_dir, name)

    def get_credential(self, cred_dir: str, name: str) -> CredentialInfo:
        cred = get_credentials(cred_dir, name)
        return CredentialInfo(cred)

    def list_events(self, cred: BaseCredentialInfo, cal: BaseCalendar, start_time: datetime, num_days: int) -> list[Event]:
        assert isinstance(cred, CredentialInfo), \
            f"type mismatch. expected: {CredentialInfo}, actual: {type(cred)}"
        return list_events(cred.cred, start_time, num_days, cal)

    def delete_events(self, cred: CredentialInfo, cal: Calendar, events: list[Event]):
        batch = delete_events_batch(cred.cred, cal, events)
        batch.execute()

    def insert_events(self, cred: CredentialInfo, cal: Calendar, events: list[Event]):
        batch = create_events_batch(cred.cred, cal, events)
        batch.execute()


class Calendar(BaseCalendar):
    def __init__(self, name: str, id: str, masked: bool = True) -> None:
        super().__init__(masked)
        self._name = name
        self._id = id
        self._provider = CalendarProvider()

    @classmethod
    def create(cls, name: str, id: str, _: str):
        return cls(name, id)

    def __hash__(self) -> int:
        return hash((self.name, self.id))

    @property
    def name(self) -> str:
        return self._name

    @property
    def provider(self) -> CalendarProvider:
        return self._provider

    @property
    def id(self) -> str:
        return self._id

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Calendar({self.name, self.id})"

    def convert_insert_event(self, event: BaseEvent) -> Event:
        assert \
            isinstance(event, Event), \
            "event is not instance of gcp.event.Event"
        title = event.calendar.name + ":" + (
            "BLOCK" if self.masked else event.title
        )
        desc = None if self.masked else event.description
        rec = {
            "summary": title,
            "start": event.record["start"],
            "end": event.record["end"],
            "description": dump_description(
                {
                    "link": str(event.record.get('htmlLink')),
                    "id": event.record['id'],
                    "update": str(datetime.now()),
                    "MARK": NONCE
                },
                desc
            )
        }
        return Event(self, rec)
