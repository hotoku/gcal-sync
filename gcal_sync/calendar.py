from abc import ABC, abstractclassmethod, abstractstaticmethod

from .gcp.calendar import Calendar as GoogleCalendar


class Calendar(ABC):
    @abstractclassmethod
    def create(cls, name: str, id: str, provider: str):
        return NotImplemented

    @staticmethod
    def parse(s: str) -> "Calendar":
        ss = s.split(":")
        assert len(ss) == 3, f"invalid format: {s}"
        if ss[2] == "google":
            return GoogleCalendar.create(*ss)
        assert False, f"panic, unknown provider: {ss[2]}"
