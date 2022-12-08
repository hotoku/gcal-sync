from __future__ import print_function

import os
import re
from pprint import pprint
from datetime import datetime

import click

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

CLIENT_KEY_PATH = os.path.join(os.getcwd(), "credentials/gcal_sync.json")


def print_calendar_example():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_KEY_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        pprint([(e["id"], e["start"]["dateTime"])
               for e in events if e["summary"] == "テスト"])

    except HttpError as error:
        print('An error occurred: %s' % error)


def secret2token(json_path: str) -> str:
    dir_name = os.path.dirname(json_path)
    base_name = os.path.basename(json_path)
    body = re.sub(r"\.[^\.]+$", "", base_name)
    return os.path.join(dir_name, body + "-token.json")


def get_credentials(json_path: str) -> Credentials:
    token_path = secret2token(json_path)
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if creds is not None and creds.valid:
        return creds

    if creds is not None and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            json_path, SCOPES)
        creds = flow.run_local_server(port=0)
        if not isinstance(creds, Credentials):
            raise RuntimeError("unknown result from run_local_server")

    with open(token_path, 'w') as token:
        token.write(creds.to_json())
    return creds


def list_events(creds: Credentials):
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    pprint([(e["id"], e["start"]["dateTime"])
           for e in events])


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
    from_creds = get_credentials(from_json)
    to_creds = get_credentials(to_json)

    list_events(from_creds)
    list_events(to_creds)


if __name__ == '__main__':
    main()
