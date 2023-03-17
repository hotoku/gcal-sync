from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod
from datetime import datetime

from .event import Event


class Calendar(ABC):
    @abstractclassmethod
    def create(cls, name: str, id: str, provider: str):
        return NotImplemented

    @abstractmethod
    def list_events(self, start_time: datetime, num_days: int) -> list[Event]:
        return NotImplemented

    @abstractmethod
    def __hash__(self) -> int:
        return NotImplemented
