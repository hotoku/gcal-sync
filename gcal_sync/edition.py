from dataclasses import dataclass

from .event import Event


@dataclass(frozen=True)
class Edition:
    delete: list[Event]
    update: list[Event]
    create: list[Event]
