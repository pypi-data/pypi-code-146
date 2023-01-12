import click

from transfermarket.market import Market


@click.group()
def cli():
    """Interact with competition data"""
    pass


@cli.command("list")
def list_competitions():
    """List all competitions."""
    market = Market()
    competitions = market.get_competitions()

    for competition in competitions:
        click.echo(competition)
