import click

from .entriy_points import (
    run as run_,
    credentials as credentials_
)


@click.group()
def main():
    pass


run = main.command(run_)
credentials = main.command(credentials_)

main()
