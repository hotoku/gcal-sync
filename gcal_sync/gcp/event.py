from datetime import datetime
from typing import Any, TypeAlias

from gcal_sync.gcp.event_util import parse_description

from .. import NONCE
from ..event import Event as BaseEvent

Record: TypeAlias = dict[str, Any]


class Event(BaseEvent):
    def __init__(self, rec: Record) -> None:
        self.record = rec

    def marked(self) -> bool:
        return "description" in self.record and NONCE in self.record["description"]

    def id(self) -> str:
        return self.record["id"]

    def orig_id(self) -> str:
        desc = self.record["description"]
        vals = parse_description(desc)
        return vals["id"]

    def start_time(self) -> datetime:
        return self.record["start"]

    def end_time(self) -> datetime:
        return self.record["end"]

    def src_name(self) -> str:
        summary = self.record["summary"]
        return summary.split(":")[0]

    def __repr__(self) -> str:
        return f"Event({self.record})"
