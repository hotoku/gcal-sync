from typing import Any, TypeAlias
from ..event import Event

record: TypeAlias = dict[str, Any]


class GoogleEvent(Event):
    pass
