import click

from .run import run as run_
from .credentials import credentials as credentials_


@click.group()
def main():
    pass


run = main.command(run_)
credentials = main.command(credentials_)

main()
