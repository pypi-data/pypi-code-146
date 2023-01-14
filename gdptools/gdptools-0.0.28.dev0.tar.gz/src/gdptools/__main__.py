"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Gdptools."""


if __name__ == "__main__":
    main(prog_name="gdptools")  # pragma: no cover
