from __future__ import print_function

import os
from datetime import datetime, timedelta
import sys
from typing import Any, Optional
import logging
from dataclasses import dataclass
import traceback
import io
import requests
import json

import dateutil.tz as dtz
import click

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest

LOGGER = logging.getLogger(__name__)
MARK = "GCAL_SYNC: LKfDbxtwFlL+fQHe38DJkWbhh5lugPUI8wQaMwBAoeZUAbak"


def setup_logger(debug: bool = False):
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - (pid: %(process)d) - %(threadName)s"
    fmter = logging.Formatter(fmt)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(fmter)
    level = logging.DEBUG if debug else logging.INFO
    LOGGER.setLevel(level)
    LOGGER.addHandler(handler)


@dataclass
class Calendar:
    name: str
    id: str

    @classmethod
    def parse(cls, s: str) -> "Calendar":
        ss = s.split(":")
        assert len(ss) == 2, f"invalid format: {s}"
        return cls(*ss)


class CalendarList(click.ParamType):
    name = "CalendarList"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> list[Calendar]:
        if isinstance(value, str):
            ss = value.split(",")
            return list(map(Calendar.parse, ss))
        if isinstance(value, list):
            return value
        if param is None and ctx is None:
            return []
        assert False, "panic. CalendarList.convert"


class CalendarIdList(click.ParamType):
    name = "CalendarIdList"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> list[str]:
        if isinstance(value, str):
            ss = value.split(",")
            return ss
        if isinstance(value, list):
            return value
        if param is None and ctx is None:
            return []
        assert False, "panic. CalendarList.convert"


def access_token_path(dir_name: str, name: str) -> str:
    return os.path.join(dir_name, name + "-token.json")


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


def list_events(creds: Credentials, start_time: datetime, days: int, calendar: Calendar) -> list[dict[str, Any]]:
    service = get_service(creds)

    time_min = start_time
    time_max = time_min + timedelta(days=days)

    events_result = service.events().list(
        calendarId=calendar.id,
        timeMin=time_min.isoformat(),
        timeMax=time_max.isoformat(),
        maxResults=days * 10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events: list[dict[str, Any]] = events_result.get('items', [])

    return events


def http_callback(action: str, id2event: dict[str, dict[str, Any]], calendar: Calendar):
    def callback(id, _, ex):
        event = id2event[id]
        msg = f"""{calendar.name}: {action} id={event["id"]} summary={event["summary"]} start={event["start"]}"""
        if ex is not None:
            LOGGER.warning("exception=%s msg=%s", ex, msg)
        else:
            LOGGER.info(msg)
    return callback


def should_deleted(e: dict[str, Any]) -> bool:
    return "description" in e and MARK in e["description"]


def delete_events_batch(creds: Credentials, start_time: datetime, days: int, calendar: Calendar) -> BatchHttpRequest:
    service = get_service(creds)
    id2event = {}

    batch = service.new_batch_http_request(
        callback=http_callback("delete", id2event, calendar))
    events = list_events(creds, start_time, days, calendar)
    for i, e in enumerate(events):
        info = f"id={e['id']} summary={e['summary']} start={e['start']}"
        if not should_deleted(e):
            LOGGER.info("%s: not deleted %s", calendar.name, info)
            continue
        req_id = str(i+1)
        batch.add(
            service.events().delete(
                calendarId=calendar.id,
                eventId=e["id"]
            ),
            request_id=req_id
        )
        id2event[req_id] = e
    return batch


def make_event(event: dict[str, Any], name: str, mask: bool) -> dict[str, Any]:
    update_time = str(datetime.now())
    summary = name + ":" + (event["summary"] if not mask else "BLOCK")
    if mask:
        return {
            "summary": summary,
            "start": event["start"],
            "end": event["end"],
            "description": "\n".join([
                f"link: {event['htmlLink']}",
                f"id: {event['id']}",
                f"update: {update_time}",
                MARK
            ])
        }
    else:
        copied_keys = [
            "conferenceData",
            "start",
            "end",
            "hangoutLink",
            "htmlLink",
            "organizer"
        ]
        ret = {
            k: event[k] for k in copied_keys if k in event
        }
        desc = event.get("description") or ""
        desc += "\n" + MARK
        ret["summary"] = summary
        ret["description"] = desc
        return ret


def create_events(creds: Credentials, events: list[dict[str, Any]], calendar: Calendar, mask: bool):
    service = get_service(creds)
    id2event = {}

    batch = service.new_batch_http_request(
        callback=http_callback("create", id2event, calendar))
    for i, e in enumerate(events):
        name = e["GCAL_SYNC_CALNAME"]
        batch.add(service.events().insert(
            calendarId=calendar.id,
            body=make_event(e, name, mask)))
        id2event[str(i + 1)] = e
    batch.execute()


def read_url(cred_dir: str) -> str:
    with open(os.path.join(cred_dir, "incoming-webhook.json")) as fp:
        data = json.load(fp)
    return data["url"]


def notify_error(msg: str, url: str):
    requests.post(
        url,
        data=json.dumps({
            "text": msg
        }),
        headers={
            "Content-type": "application/json"
        }
    )


@click.group()
def main():
    pass


@main.command()
@click.argument("cred_dir", type=click.Path(exists=True, file_okay=False))
@click.argument("cals", type=CalendarList())
@click.option("--start_time", type=click.DateTime(),
              default=datetime.now(tz=dtz.gettz("Asia/Tokyo")),
              help="start time of synchronized interval. default to current time.")
@click.option("--duration", type=int,
              default=30,
              help="duration of synchronized interval in days. default to 30.")
def run(cred_dir: str,
        cals: list[Calendar],
        start_time: datetime, duration: int):
    setup_logger(debug=False)

    try:
        events = []
        delete_batches: list[BatchHttpRequest] = []
        for cal in cals:
            creds = get_credentials(cred_dir, cal.name)
            delete_batches.append(delete_events_batch(
                creds, start_time, duration, cal))
            events2 = [
                e for e in list_events(creds, start_time, duration, cal)
                if not should_deleted(e)
            ]
            for e in events2:
                e["GCAL_SYNC_CALNAME"] = cal.name
            events += events2
        for cal in cals:
            creds = get_credentials(cred_dir, cal.name)
            events2 = [
                e for e in events if not e["GCAL_SYNC_CALNAME"] == cal.name
            ]
            mask = cal.name != "ME"
            create_events(creds, events2, cal, mask)
        for b in delete_batches:
            b.execute()
    except Exception as e:
        sio = io.StringIO()
        traceback.print_exception(e, file=sio)
        msg = sio.getvalue()
        LOGGER.error(msg)
        notify_error(msg, read_url(cred_dir))


@main.command()
@click.argument("client_json", type=click.Path(exists=True, dir_okay=False))
@click.argument("cred_dir", type=click.Path(exists=True, file_okay=False, writable=True))
@click.argument("ids", type=CalendarIdList())
def credentials(client_json: str, cred_dir: str, ids: list[str]):
    for id_ in ids:
        ret = input(
            f"We are going to get access token for calendar {id_}. (Y/n): ")
        if not (ret == "" or ret == "Y"):
            print("stopping.")
            return
        make_access_token(client_json, cred_dir, id_)


if __name__ == '__main__':
    main()
