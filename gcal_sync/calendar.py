from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from datetime import datetime
import logging

from .edition import Edition
from .event import Event


LOGGER = logging.getLogger(__name__)


class CredentialInfo:
    pass


class CalendarProvider(ABC):
    """クラウドのAPIとの接続を管理するクラス。

    - 認可情報の取得と保存
    - 認可情報を利用したAPIとの通信

    を行う。認可情報は、各関数の引数として渡されるcred_dirの中に保存する。
    その際、同時に渡されるnameによってカレンダーごとに認可情報を分けて保存する。
    """

    @abstractmethod
    def authorize(self, client_info: str, cred_dir: str, name: str):
        """サーバーから認可を得る。

        client_info: アプリケーションクライアントの認証情報
        cred_dir: 認可情報を保存するディレクトリへのパス
        name: 対象カレンダーの名前
        """
        return NotImplemented

    @abstractmethod
    def get_credential(self, cred_dir: str, name: str) -> CredentialInfo:
        return NotImplemented

    @abstractmethod
    def delete_events(self, cred: CredentialInfo, cal: Calendar, events: list[Event]):
        return NotImplemented

    @abstractmethod
    def insert_events(self, cred: CredentialInfo, cal: Calendar, events: list[Event]):
        return NotImplemented

    @abstractmethod
    def list_events(self, cred: CredentialInfo, cal: Calendar, start_time: datetime, num_days: int) -> list[Event]:
        return NotImplemented


class Calendar(ABC):
    def __init__(self, masked: bool = False) -> None:
        super().__init__()
        self.masked = masked

    @abstractclassmethod
    def create(cls, name: str, id: str, provider: str):
        # todo: providerは、各実装が知っているはずなので引数には不要
        return NotImplemented

    @abstractproperty
    def provider(self) -> CalendarProvider:
        return NotImplemented

    @abstractproperty
    def name(self) -> str:
        return NotImplemented

    @abstractproperty
    def id(self) -> str:
        return NotImplemented

    def list_events(self, cred_dir: str, start_time: datetime, num_days: int) -> list[Event]:
        cred = self.provider.get_credential(cred_dir, self.name)
        return self.provider.list_events(cred, self, start_time, num_days)

    @abstractmethod
    def __hash__(self) -> int:
        return NotImplemented

    @abstractmethod
    def convert_insert_event(self, event: Event) -> Event:
        return NotImplemented

    def execute(self, cred_dir: str, editions: list[Edition]):
        cred = self.provider.get_credential(cred_dir, self.name)

        delete = []
        for e in editions:
            delete += e.delete

        LOGGER.info("deleting: %s", delete)
        self.provider.delete_events(cred, self, delete)

        insert = []
        for edit in editions:
            for e in edit.create:
                insert.append(
                    self.convert_insert_event(e)
                )
        self.provider.insert_events(cred, self, insert)
