from typing import Any, TypeAlias

import os
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from ..calendar import Calendar


Event: TypeAlias = list[dict[str, Any]]


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
