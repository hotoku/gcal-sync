from dataclasses import dataclass

from .event import Event


@dataclass(frozen=True)
class Edition:
    delete: list[Event]
    create: list[Event]
    src_name: str
