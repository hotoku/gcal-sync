from .calendar import Calendar, CalendarProvider
from .gcp import Calendar as GoogleCalendar, CalendarProvider as GoogleCalendarProvider

UNMASKED_CAL_NAMES = ["ME"]


def provider_factory(s: str) -> CalendarProvider:
    if s == "google":
        return GoogleCalendarProvider()
    assert False, f"panic, unknown provider: {s}"


def parse(s: str) -> Calendar:
    ss = s.split(":")
    assert len(ss) == 3, f"invalid format: {s}"
    if ss[2] == "google":
        ret = GoogleCalendar.create(*ss)
        if ret.name in UNMASKED_CAL_NAMES:
            ret.masked = False
        return ret
    assert False, f"panic, unknown provider: {ss[2]}"
