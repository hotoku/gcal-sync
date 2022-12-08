from __future__ import print_function

import os
import re
from pprint import pprint
from datetime import datetime
from typing import Any

import click

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource


def secret2token(json_path: str) -> str:
    dir_name = os.path.dirname(json_path)
    base_name = os.path.basename(json_path)
    body = re.sub(r"\.[^\.]+$", "", base_name)
    return os.path.join(dir_name, body + "-token.json")


def get_credentials(json_path: str, message: str) -> Credentials:
    scopes = ['https://www.googleapis.com/auth/calendar']

    token_path = secret2token(json_path)
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if creds is not None and creds.valid:
        return creds

    if creds is not None and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        print(message)
        flow = InstalledAppFlow.from_client_secrets_file(
            json_path, scopes)
        creds = flow.run_local_server(port=0)
        if not isinstance(creds, Credentials):
            raise RuntimeError("unknown result from run_local_server")

    with open(token_path, 'w') as token:
        token.write(creds.to_json())
    return creds


def get_service(creds: Credentials):
    ret = build('calendar', 'v3', credentials=creds)
    return ret


def list_events(creds: Credentials):
    service = get_service(creds)

    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events: list[dict[str, Any]] = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    pprint([(e["id"], e["start"]["dateTime"])
           for e in events])


def create_events(creds: Credentials, event: dict[str, Any]):
    service = get_service(creds)
    ret = service.events().insert(calendarId="primary", body=event).execute()
    print(ret)


@click.command()
@click.argument("from_json", type=click.Path(exists=True, dir_okay=False))
@click.argument("to_json", type=click.Path(exists=True, dir_okay=False))
@click.option("--start_time", type=click.DateTime(),
              default=datetime.now(),
              help="start time of synchronized interval. default to current time.")
@click.option("--duration", type=int,
              default=30,
              help="duration of synchronized interval in days. default to 30.")
def main(from_json: str, to_json: str, start_time: datetime, duration: int):
    from_creds = get_credentials(
        from_json, "start authenticate process for FROM calendar")
    to_creds = get_credentials(
        to_json, "start authenticate process for TO calendar")

    create_events(from_creds, {
        "summary": "test",
        "start": {
            "dateTime": "2022-12-08T18:00:00",
            "timeZone": "Asia/Tokyo"
        },
        "end": {
            "dateTime": "2022-12-08T18:30:00",
            "timeZone": "Asia/Tokyo"
        }
    })


if __name__ == '__main__':
    main()
