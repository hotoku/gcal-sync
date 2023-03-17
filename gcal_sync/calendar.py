from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from datetime import datetime

from .event import Event


class CalendarProvider(ABC):
    @abstractmethod
    def list_events(self, start_time: datetime, num_days: int) -> list[Event]:
        return NotImplemented

    @abstractmethod
    def authorize(self, client_info: str, cred_dir: str, name: str):
        """サーバーから認可を得る。

        client_info: アプリケーションクライアントの認証情報
        cred_dir: 認可情報を保存するディレクトリへのパス
        name: 対象カレンダーの名前
        """
        return NotImplemented


class Calendar(ABC):
    @abstractclassmethod
    def create(cls, name: str, id: str, provider: str):  # todo: providerは不要
        return NotImplemented

    @abstractproperty
    def provider(self) -> CalendarProvider:
        return NotImplemented

    def list_events(self, start_time: datetime, num_days: int) -> list[Event]:
        return self.provider.list_events(start_time, num_days)

    @abstractmethod
    def __hash__(self) -> int:
        return NotImplemented
