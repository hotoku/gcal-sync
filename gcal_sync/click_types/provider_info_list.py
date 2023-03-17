from typing import Any, Optional, Tuple
from dataclasses import dataclass

import click

from ..calendar import CalendarProvider
from ..calendar_util import provider_factory


@dataclass(frozen=True)
class ProviderInfo:
    name: str
    provider: CalendarProvider


class ProviderInfoList(click.ParamType):
    name = "ProviderInfoList"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> list[ProviderInfo]:
        if isinstance(value, str):
            ss = value.split(",")
            ret: list[ProviderInfo] = []
            for s in ss:
                pair = s.split(":")
                assert len(pair) == 2, f"panic, invalid format: {s}"
                name, prov = pair
                ret.append(ProviderInfo(name, provider_factory(prov)))
            return ret
        if isinstance(value, list):
            return value
        if param is None and ctx is None:
            return []
        assert False, "panic. ProviderInfoList:convert"
