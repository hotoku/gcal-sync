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
        return NotImplemented

    @abstractproperty
    def id(self) -> str:
        return NotImplemented

    @abstractproperty
    def orig_id(self) -> str:
        return NotImplemented

    @abstractproperty
    def start_time(self) -> datetime:
        return NotImplemented

    @abstractproperty
    def end_time(self) -> datetime:
        return NotImplemented

    @abstractproperty
    def src_name(self) -> str:
        return NotImplemented
