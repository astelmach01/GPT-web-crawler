import datetime

import rich_click as click
from .crawl import run_spider


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
    """Run the crawler."""
    start_time = datetime.datetime.now()
    run_spider(url)
    end_time = datetime.datetime.now()
    print(f"Time elapsed: {end_time - start_time}")
