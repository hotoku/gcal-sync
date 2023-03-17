from datetime import datetime

import click
import dateutil.tz as dtz

from ..click_types import CalendarList
from ..calendar import Calendar


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
    print(cal2events)
