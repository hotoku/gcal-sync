from typing import Any, Optional

import click


class CalendarIdList(click.ParamType):
    name = "CalendarIdList"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> list[str]:
        if isinstance(value, str):
            ss = value.split(",")
            return ss
        if isinstance(value, list):
            return value
        if param is None and ctx is None:
            return []
        assert False, "panic. CalendarList.convert"
