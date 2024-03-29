import logging
import sys

import click

from .entriy_points import (
    run as run_,
    credentials as credentials_,
    clear as clear_
)

LOGGER = logging.getLogger(__name__)


def setup_logger(debug: bool = False):
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - (pid: %(process)d) - %(threadName)s"
    fmter = logging.Formatter(fmt)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(fmter)
    level = logging.DEBUG if debug else logging.INFO
    handler.setLevel(level)
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)

    g = logging.getLogger("googleapiclient.discovery_cache")
    g.setLevel(logging.WARNING)


@click.group()
def main():
    setup_logger()


run = main.command(run_)
credentials = main.command(credentials_)
clear = main.command(clear_)

main()
