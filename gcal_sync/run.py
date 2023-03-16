from datetime import datetime

import click
import dateutil.tz as dtz

from gcal_sync.utils import get_credentials

from .calendar_list import CalendarList
from .calendar import Calendar


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
    cal2cred = {
        cal: get_credentials(cred_dir, cal.name)
        for cal in cals
    }
    cal2events = {
        cal: cal
        for cal in cals
    }
    pass
