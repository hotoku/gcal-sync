from typing import Any, Optional
from dataclasses import dataclass

import click


@dataclass(frozen=True)
class CalendarInfo:
    name: str
    provider: str


class CalendarIdList(click.ParamType):
    name = "CalendarIdList"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> list[CalendarInfo]:
        if isinstance(value, str):
            ss = value.split(",")
            ret: list[CalendarInfo] = []
            for s in ss:
                pair = s.split(":")
                assert len(pair) == 2, f"panic, invalid format: {s}"
                ret.append(CalendarInfo(pair[0], pair[1]))
            return ret
        if isinstance(value, list):
            return value
        if param is None and ctx is None:
            return []
        assert False, "panic. CalendarList.convert"
