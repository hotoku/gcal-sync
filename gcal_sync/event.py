from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .calendar import Calendar


class Event(ABC):
    def __init__(self, cal: Calendar) -> None:
        super().__init__()
        self.calendar = cal

    @abstractmethod
    def marked(self) -> bool:
        "gcal_syncによってコピーされたイベントか否かを返す"
        return NotImplemented

    @abstractproperty
    def id(self) -> str:
        """各カレンダーの中で、このイベントを一意に識別するためのidを返す。
        実体は、カレンダープロバイダごとに異なると考えられる。"""
        return NotImplemented

    @abstractproperty
    def title(self) -> str:
        """このイベントの件名を返す。
        実体は、カレンダープロバイダごとに異なる。"""
        return NotImplemented

    @abstractproperty
    def description(self) -> str:
        """このイベントの説明文章を返す。"""
        return NotImplemented

    @abstractproperty
    def start_time(self) -> datetime:
        return NotImplemented

    @abstractproperty
    def end_time(self) -> datetime:
        return NotImplemented

    @property
    def orig_id(self) -> str:
        """gcal_syncによってコピーされたイベントの場合に、その元となったイベントのidを返す。
        そうでない場合は、AssertionErrorが発生する。"""
        assert self.marked(), f"This event is not copied. {self}"
        return self.orig_id_impl()

    @abstractmethod
    def orig_id_impl(self) -> str:
        return NotImplemented

    @property
    def src_name(self) -> str:
        """gcal_syncによってコピーされたイベントの場合に、その元となったイベントが登録されていたカレンダーの名前を返す。
        そうでない場合は、AssertionErrorが発生する。"""
        assert self.marked(), f"This event is not copied. {self}"
        return self.src_name_impl()

    @abstractmethod
    def src_name_impl(self) -> str:
        return NotImplemented
