import click

from .maps import Client
from .packer import LocationPacker


@click.command(help="Fetch the Geocode for the given location.")
@click.argument("location")
@click.option("-c", "--country", help="Optional country code.")
@click.option("--key", help="google Cloud API key.", required=True)
def geocode(location, country=None, key=None):
    client = Client(key=key)
    geocode = client.geocode(location, country)

    if geocode is None:
        click.echo("Maps can't find '{}'".format(location))

    else:
        click.echo(click.style(geocode.location, fg="green"))
        click.echo(
            "{}: {} ({})".format(
                click.style("Precision", bold=True),
                geocode.location_type.name,
                geocode.location_type.value,
            )
        )
        click.echo(
            "{}: {}, {}".format(
                click.style(" > Southwest", bold=True),
                geocode.viewport.southwest[0],
                geocode.viewport.southwest[1],
            )
        )
        click.echo(
            "{}: {}, {}".format(
                click.style(" > Northeast", bold=True),
                geocode.viewport.northeast[0],
                geocode.viewport.northeast[1],
            )
        )


@click.command(help="Fetch the Location the given lat/lon.")
@click.argument("latlon")
@click.option("--key", help="google Cloud API key.", required=True)
def reverse_geocode(latlon, key=None):
    client = Client(key=key)
    location = client.reverse_geocode(latlon)

    if location is None:
        click.echo("Maps can't find '{}'".format(latlon))

    else:
        click.echo(click.style(location.formatted_address, fg="green"))
        click.echo("{}: {}".format(click.style("Country", bold=True), location.country))
        click.echo("{}: {}".format(click.style("Region", bold=True), location.region))
        click.echo("{}: {}".format(click.style("City", bold=True), location.city))
        click.echo(
            "{}: {}".format(click.style("Postcode", bold=True), location.postcode)
        )
        click.echo(
            "{}: {}".format(click.style("Place ID", bold=True), location.place_id)
        )


@click.command(help="Unpack the GeoIP databases from the DB_PATH folder.")
@click.argument("db_path")
@click.option(
    "-d",
    "--data-dir",
    default="data",
    help='Destination folder for the extracted data (defaults to "./data").',
)
@click.option(
    "-v",
    "--version",
    default="latest",
    help='GeoIP databases version (defaults to "latest").',
)
def unpack(db_path, data_dir, version):
    packer = LocationPacker(db_path=db_path, data_dir=data_dir, version=version)
    click.echo(f'Unpacking GeoIP2 databases to "{packer.data_dir}".')

    try:
        packer()
    except SystemExit:
        click.echo(click.style("Cannot find the database files.", fg="red"))
        raise SystemExit(1)
    else:
        click.echo("\U0001F44D Done.")
        click.echo(
            f'Now run "aws s3 sync {packer.data_dir} s3://<bucket>/rig/geo/{version}"'
            " to upload to S3."
        )
