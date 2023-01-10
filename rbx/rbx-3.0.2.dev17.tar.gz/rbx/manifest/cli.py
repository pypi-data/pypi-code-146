import click

from .processor import AssetFetcher, CreativeBuilder, zip_creatives
from ..settings import AWS_BUCKET, AWS_REGION


@click.command(help="Get the manifest from a url.")
@click.argument("url")
@click.option("-f", "--filename", default="out", help="Name of Zip File to output.")
@click.option(
    "-m",
    "--mode",
    type=click.Choice([e.name for e in AssetFetcher.Mode], case_sensitive=False),
    default=AssetFetcher.Mode.HTTP.name,
    help="Mode of Download (http or s3).",
)
@click.option("-b", "--bucket", default=AWS_BUCKET, help="Optional bucket path")
@click.option("-r", "--region", default=AWS_REGION, help="Optional region")
def build_creative(url, filename, mode, bucket, region):
    """Using the specified URL location, will retrieve, process manifest and write creatives to zip.

    Parameters:
        url (str):
            The location of the manifest to download and build image from.
        filename (str):
            The filename of the final zip file to generate.
        mode (str):
            If we are retrieving the manifest from http or aws.
        bucket (str):
            The name of the bucket where the file is stored.
        region (str):
            The region of the bucket where the file is stored.
    """
    client = AssetFetcher(AssetFetcher.Mode[mode], bucket, region)

    builder = CreativeBuilder(url, client)

    creatives = builder.build()
    click.echo("Creatives Generated!")

    zip_creatives(creatives, filename=filename)
    click.echo(f"Creatives Now Available in {filename}.zip")
