"""Script to do maintenance actions for fietsboek."""
import datetime
import logging
import logging.config

import click
import pyramid.paster
from sqlalchemy import create_engine, delete, exists, not_, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from .. import config as mod_config
from .. import models
from ..data import DataManager

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to the Fietsboek configuration file",
)
def cli(config):
    """Runs regular maintenance operations on the instance.

    This does the following:

    \b
    * Deletes pending uploads that are older than 24 hours.
    * Rebuilds the cache for missing tracks.
    """
    logging.config.fileConfig(config)
    settings = pyramid.paster.get_appsettings(config)

    config = mod_config.parse(settings)
    engine = create_engine(config.sqlalchemy_url)

    data_manager = DataManager(config.data_dir)

    LOGGER.debug("Starting maintenance tasks")
    remove_old_uploads(engine)
    rebuild_cache(engine, data_manager)


def remove_old_uploads(engine: Engine):
    """Removes old uploads from the database."""
    LOGGER.info("Deleting old uploads")
    limit = datetime.datetime.now() - datetime.timedelta(hours=24)
    session = Session(engine)
    stmt = delete(models.Upload).where(models.Upload.uploaded_at < limit)
    session.execute(stmt)
    session.commit()


def rebuild_cache(engine: Engine, data_manager: DataManager):
    """Rebuilds the cache entries that are currently missing."""
    LOGGER.debug("Rebuilding caches")
    session = Session(engine)
    needed_rebuilds = select(models.Track).where(
        not_(exists(select(models.TrackCache).where(models.TrackCache.track_id == models.Track.id)))
    )
    with session:
        for track in session.execute(needed_rebuilds).scalars():
            LOGGER.info("Rebuilding cache for track %d", track.id)
            gpx_data = data_manager.open(track.id).decompress_gpx()
            track.ensure_cache(gpx_data)
            session.add(track)
        session.commit()


__all__ = ["cli"]
