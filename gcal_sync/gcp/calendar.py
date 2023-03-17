from datetime import datetime
from typing import Optional

from .event import Event
from ..calendar import Calendar as BaseCalendar


class Calendar(BaseCalendar):
    def __init__(self, name: str, id: Optional[str]) -> None:
        self.name = name
        self.id = id

    @classmethod
    def create(cls, name: str, id: str, _: str):
        return cls(name, id)

    def __hash__(self) -> int:
        return hash((self.name, self.id))

    def list_events(self, start_time: datetime, num_days: int) -> list[Event]:
        return []
