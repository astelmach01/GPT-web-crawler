import datetime

import rich_click as click
from .crawl import crawl_webpage


@click.group("app")
def cli():
    pass


@cli.command("run")
@click.option(
    "--url",
    type=str,
    help="the domain to crawl",
)
def run(url: str):
    """Run the crawler"""
    start = datetime.datetime.now()
    crawl_webpage(url)
    end = datetime.datetime.now()
    click.secho(f"Done in {end - start}", fg="green")
