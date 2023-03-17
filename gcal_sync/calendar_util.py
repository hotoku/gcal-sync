from .calendar import Calendar
from .gcp import Calendar as GoogleCalendar


@staticmethod
def parse(s: str) -> Calendar:
    ss = s.split(":")
    assert len(ss) == 3, f"invalid format: {s}"
    if ss[2] == "google":
        return GoogleCalendar.create(*ss)
    assert False, f"panic, unknown provider: {ss[2]}"
