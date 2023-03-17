from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from datetime import datetime

from .event import Event


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
    def list_events(self, cred: CredentialInfo, cal: Calendar, start_time: datetime, num_days: int) -> list[Event]:
        return NotImplemented

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


class Calendar(ABC):
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
