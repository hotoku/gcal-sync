from datetime import datetime
from itertools import product

import click
import dateutil.tz as dtz

from ..edition import Edition
from ..event import Event
from ..click_types import CalendarList
from ..calendar import Calendar


def compare(src_: list[Event], dest_: list[Event], src_name: str) -> Edition:
    src = [e for e in src_ if not e.marked()]
    dest = [e for e in dest_ if e.marked() and e.src_name == src_name]
    src_id2event = {
        e.id: e
        for e in src
    }
    src_ids = list(src_id2event.keys())
    dest_id2event = {
        e.orig_id: e
        for e in dest
    }
    dest_ids = list(dest_id2event.keys())

    delete = set(dest_ids) - set(src_ids)
    insert = set(src_ids) - set(dest_ids)

    intersect = set(src_ids).intersection(set(dest_ids))
    for e in intersect:
        s = src_id2event[e]
        d = dest_id2event[e]
        if s.start_time != d.start_time or s.end_time != d.end_time:
            delete.add(e)
            insert.add(e)

    return Edition(
        [dest_id2event[e] for e in delete],
        [src_id2event[e] for e in insert],
        src_name
    )


@click.argument("cred_dir", type=click.Path(exists=True, file_okay=False))
@click.argument("cals", type=CalendarList())
@click.option("--start_time", type=click.DateTime(),
              default=datetime.now(tz=dtz.gettz("Asia/Tokyo")),
              help="start time of synchronized interval. default to current time.")
@click.option("--duration", type=int,
              default=30,
              help="duration of synchronized interval in days. default to 30.")
def run(cred_dir: str,
        cals: list[Calendar],
        start_time: datetime, duration: int):
    cal2events = {
        cal: cal.list_events(cred_dir, start_time, duration)
        for cal in cals
    }
    cal2editions: dict[Calendar, list[Edition]] = {
        cal: []
        for cal in cals
    }
    for src, dest in product(cal2events.keys(), cal2events.keys()):
        if src == dest:
            continue
        e = compare(cal2events[src], cal2events[dest], src.name)
        cal2editions[dest].append(e)
