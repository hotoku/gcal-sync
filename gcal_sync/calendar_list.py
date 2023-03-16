from typing import Any, Optional

import click
from .calendar import Calendar


class CalendarList(click.ParamType):
    name = "CalendarList"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> list[Calendar]:
        if isinstance(value, str):
            ss = value.split(",")
            return list(map(Calendar.parse, ss))
        if isinstance(value, list):
            return value
        if param is None and ctx is None:
            return []
        assert False, "panic. CalendarList.convert"
