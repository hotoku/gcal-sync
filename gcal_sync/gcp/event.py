from abc import abstractproperty
from datetime import datetime
from typing import Any, TypeAlias

from ..event import Event as BaseEvent
from ..calendar import Calendar
from .. import NONCE

from .event_util import parse_description

Record: TypeAlias = dict[str, Any]


class Event(BaseEvent):
    def __init__(self, cal: Calendar, rec: Record) -> None:
        super().__init__(cal)
        self.record = rec

    def marked(self) -> bool:
        return "description" in self.record and NONCE in self.record["description"]

    @property
    def id(self) -> str:
        return self.record["id"]

    def orig_id_impl(self) -> str:
        desc = self.record["description"]
        vals = parse_description(desc)
        return vals["id"]

    @property
    def start_time(self) -> datetime:
        return self.record["start"]

    @property
    def end_time(self) -> datetime:
        return self.record["end"]

    def src_name_impl(self) -> str:
        summary = self.record["summary"]
        return summary.split(":")[0]

    def __repr__(self) -> str:
        return f"Event({self.record})"

    @property
    def title(self) -> str:
        return self.record["summary"]

    @property
    def description(self) -> str:
        if "description" in self.record:
            return self.record["description"]
        else:
            return ""
