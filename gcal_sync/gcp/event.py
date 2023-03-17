from typing import Any, TypeAlias
from ..event import Event as BaseEvent

Record: TypeAlias = dict[str, Any]


class Event(BaseEvent):
    def __init__(self, rec: Record) -> None:
        self.record = rec
