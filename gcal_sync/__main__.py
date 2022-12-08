from __future__ import print_function

import os
import re
from pprint import pprint
from datetime import datetime, timedelta, timezone
from typing import Any
import dateutil.tz as dtz

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


def list_events(creds: Credentials, start_time: datetime, days: int, calendar_id: str) -> list[dict[str, Any]]:
    service = get_service(creds)

    time_min = start_time
    time_max = time_min + timedelta(days=days)

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min.isoformat(),
        timeMax=time_max.isoformat(),
        maxResults=days * 10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events: list[dict[str, Any]] = events_result.get('items', [])

    return events


def delete_events(creds: Credentials, start_time: datetime, days: int, calendar_id: str):
    service = get_service(creds)

    def callback(id, _, ex):
        if ex is not None:
            print("delete exception: ", id, e)
        else:
            print("delete success: ", id)

    batch = service.new_batch_http_request(callback=callback)
    events = list_events(creds, start_time, days, calendar_id)
    for e in events:
        batch.add(service.events().delete(
            calendarId=calendar_id,
            eventId=e["id"]
        ))
    batch.execute()


def create_events(creds: Credentials, events: list[dict[str, Any]], calendar_id: str):
    service = get_service(creds)

    def callback(id, _, ex):
        if ex is not None:
            print("create exception: ", id, e)
        else:
            print("create success: ", id)

    batch = service.new_batch_http_request(callback=callback)
    for e in events:
        batch.add(service.events().insert(
            calendarId=calendar_id,
            body={
                "summary": e["summary"],
                "start": e["start"],
                "end": e["end"],
                "description": "\n".join([
                    f"link: {e['htmlLink']}",
                    f"id: {e['id']}"
                ])
            }))
    batch.execute()

    service = get_service(creds)


@click.command()
@click.argument("from_json", type=click.Path(exists=True, dir_okay=False))
@click.argument("to_json", type=click.Path(exists=True, dir_okay=False))
@click.argument("from_id", type=str)
@click.argument("to_id", type=str)
@click.option("--start_time", type=click.DateTime(),
              default=datetime.now(tz=dtz.gettz("Asia/Tokyo")),
              help="start time of synchronized interval. default to current time.")
@click.option("--duration", type=int,
              default=30,
              help="duration of synchronized interval in days. default to 30.")
def main(from_json: str, to_json: str, from_id: str, to_id: str,
         start_time: datetime, duration: int):
    from_creds = get_credentials(
        from_json, "start authenticate process for FROM calendar")
    to_creds = get_credentials(
        to_json, "start authenticate process for TO calendar")

    delete_events(to_creds, start_time, duration, to_id)
    events = list_events(from_creds, start_time, duration, from_id)
    create_events(to_creds, events, to_id)


if __name__ == '__main__':
    main()
