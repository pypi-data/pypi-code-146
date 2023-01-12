import click

from transfermarket.market import Market


@click.group()
def cli():
    """Interact with team data"""
    pass


@cli.command("list")
@click.argument("competition_id")
def list_teams(competition_id):
    """List all teams for a given competition."""
    market = Market()
    teams = market.get_teams(competition_id)

    for team in teams:
        click.echo(team)
