import os
import click

from transfermarket.market import Market


@click.group()
def cli():
    """Interact with player data"""
    pass


@cli.command("list")
@click.argument("team_id")
def list_players(team_id):
    """List all players for a given team."""
    market = Market()
    players = market.get_players(team_id)

    for player in players:
        click.echo(player)


@cli.command("dump")
def dump_players():
    """Dump all players."""
    market = Market()

    competition_count = 0
    team_count = 0
    player_count = 0
    competitions = market.get_competitions()

    if os.path.isfile("output.txt"):
        os.remove("output.txt")

    with open("output.txt", "w") as f:
        for competition in competitions:
            try:
                competition_count += 1
                click.echo(competition)
                f.write(f"{competition}\n")

                teams = market.get_teams(competition.id)
                for team in teams:
                    team_count += 1
                    click.echo(f"\t{team}")
                    f.write(f"\t{team}\n")

                    players = market.get_players(team.id)
                    for player in players:
                        player_count += 1
                        f.write(f"\t\t{player}\n")

                    f.write("\n")

                f.write("\n")
            except ValueError as e:
                click.echo(e)

    click.echo(f"Competitions: {competition_count}")
    click.echo(f"Teams: {team_count}")
    click.echo(f"Players: {player_count}")
