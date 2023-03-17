import os
from datetime import datetime
from typing import Optional

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials


from .event import Event
from ..calendar import Calendar as BaseCalendar, CalendarProvider as BaseCalendarProvider


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


class Calendar(BaseCalendar):
    def __init__(self, name: str, id: Optional[str]) -> None:
        self.name = name
        self.id = id
        self._provide = CalendarProvider()

    @classmethod
    def create(cls, name: str, id: str, _: str):
        return cls(name, id)

    def __hash__(self) -> int:
        return hash((self.name, self.id))


class CalendarProvider(BaseCalendarProvider):
    def list_events(self, start_time: datetime, num_days: int) -> list[Event]:
        raise NotImplementedError()

    def authorize(self, client_info: str, cred_dir: str, name: str):
        make_access_token(client_info, cred_dir, name)
