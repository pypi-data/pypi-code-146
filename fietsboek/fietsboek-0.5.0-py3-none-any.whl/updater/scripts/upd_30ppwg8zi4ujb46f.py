"""Revision upgrade script 30ppwg8zi4ujb46f

This script moves the GPX data out of the database and puts them into the data
directory instead.

Date created: 2022-12-14 22:33:32.837737
"""
import gzip
import shutil
from pathlib import Path

import brotli
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from fietsboek.updater.script import UpdateScript

update_id = '30ppwg8zi4ujb46f'
previous = [
    'v0.4.0',
]
alembic_revision = 'c939800af428'


class Up(UpdateScript):
    def pre_alembic(self, config):
        engine = create_engine(config["sqlalchemy.url"])
        connection = engine.connect()
        data_dir = Path(config["fietsboek.data_dir"])

        for row in connection.execute("SELECT id, gpx FROM tracks;"):
            self.tell(f"Moving GPX data for track {row.id} from database to disk")
            track_dir = data_dir / "tracks" / str(row.id)
            track_dir.mkdir(parents=True, exist_ok=True)

            raw_gpx = gzip.decompress(row.gpx)
            gpx_path = track_dir / "track.gpx.br"
            gpx_path.write_bytes(brotli.compress(raw_gpx, quality=5))
            shutil.copy(gpx_path, track_dir / "track.bck.gpx.br")

    def post_alembic(self, config):
        pass


class Down(UpdateScript):
    def pre_alembic(self, config):
        pass

    def post_alembic(self, config):
        engine = create_engine(config["sqlalchemy.url"])
        connection = engine.connect()
        data_dir = Path(config["fietsboek.data_dir"])

        for track_path in (data_dir / "tracks").iterdir():
            track_id = int(track_path.name)
            self.tell(f"Moving GPX data for track {track_id} from disk to database")
            brotli_data = (track_path / "track.gpx.br").read_bytes()
            gzip_data = gzip.compress(brotli.decompress(brotli_data))
            connection.execute(
                text("UPDATE tracks SET gpx = :gpx WHERE id = :id;"),
                gpx=gzip_data, id=track_id
            )

            (track_path / "track.gpx.br").unlink()
            (track_path / "track.bck.gpx.br").unlink(missing_ok=True)
