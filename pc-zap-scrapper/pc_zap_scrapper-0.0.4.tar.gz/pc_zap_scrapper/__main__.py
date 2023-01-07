import os
import pc_zap_scrapper
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
import click
from click_default_group import DefaultGroup

from pc_zap_scrapper import ACTION, LOCALIZATION, TYPE
from pc_zap_scrapper.load import load
from pc_zap_scrapper.scrap import search_estates
from pc_zap_scrapper.transform import format_data
from pc_zap_scrapper.utils import validate_environment, configure

@click.group(cls=DefaultGroup, default='main', default_if_no_args=True)
def cli():
    pass

@cli.command(name="env")
def env():
    logger.info("--> ENV Function")

    # Import .env file
    _path = os.path.join(Path(pc_zap_scrapper.__file__).resolve().parents[1], "temp", ".env")

    if not load_dotenv(dotenv_path=_path):
        error_message = "No '.env' file was found."
        logger.error(error_message)
        raise Exception(error_message)

    validate_environment()

@cli.command(name="search")
@click.option(
    "-a",
    "--action",
    default=ACTION,
    help="Action to find. Can be 'venda' or 'aluguel'",
    type=str,
)
@click.option(
    "-t",
    "--estate_type",
    default=TYPE,
    help="Estate type. Can be 'imoveis', 'casas' ou 'apartamentos'",
    type=str,
)
@click.option(
    "-l",
    "--location",
    default=LOCALIZATION,
    help="City and state, in the format 'uf+city-name'",
    type=str,
)
def search(action, estate_type, location):
    logger.info("--> Search Function")
    search_estates(action, estate_type, location)

@cli.command(name="format-data")
def format():
    logger.info("--> Format Data Function")
    format_data()

@cli.command(name="db-ingest")
def db_ingest():
    logger.info("--> DB Ingest Function")
    load()

@cli.command(name="configure")
@click.option(
    "-p",
    "--dotenv_path",
    default=None,
    help="Path to the .env file",
    type=str,
)
def config(dotenv_path):
    print("--> Config")
    configure(dotenv_path)

@cli.command()
def main():
    """ Main function. """

    logger.info("--> Main Function")

    #env()
    #search()
    #format()
    #db_ingest()

if __name__ == "__main__":

    try:
        cli()

    except Exception as err:
        logger.error(err)
