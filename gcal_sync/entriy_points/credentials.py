import os

import click

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

from .calendar_id_list import CalendarIdList, CalendarInfo


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


@click.argument("client_json", type=click.Path(exists=True, dir_okay=False))
@click.argument("cred_dir", type=click.Path(exists=True, file_okay=False, writable=True))
@click.argument("infos", type=CalendarIdList())
def credentials(client_json: str, cred_dir: str, infos: list[CalendarInfo]):
    # todo:
    # 現状、googleカレンダーにしか対応していないのでプロバイダ部分は無視している。
    for info in infos:
        ret = input(
            f"We are going to get access token for calendar {info}. (Y/n): ")
        if not (ret == "" or ret == "Y"):
            print("stopping.")
            return
        make_access_token(client_json, cred_dir, info.name)
