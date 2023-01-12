"""Revision upgrade script lu8w3rwlz4ddcpms

Update to embed the GPX metadata (title, description, author) into the GPX
files.

Note that the down-revision is a no-nop - while we could use the backed-up
files to restore the metadata, it seems a bit unnecessary to go through the
effort of parsing them and extracting the old metadata.

Date created: 2023-01-03 21:01:04.770362
"""
import datetime
from pathlib import Path

import brotli
import gpxpy
from sqlalchemy import create_engine

from fietsboek.updater.script import UpdateScript

update_id = 'lu8w3rwlz4ddcpms'
previous = [
    '30ppwg8zi4ujb46f',
]
alembic_revision = 'c939800af428'


class Up(UpdateScript):
    def pre_alembic(self, config):
        engine = create_engine(config["sqlalchemy.url"])
        connection = engine.connect()
        data_dir = Path(config["fietsboek.data_dir"])

        sql = (
            "SELECT tracks.id, tracks.title, tracks.description, tracks.date_raw, "
            "tracks.date_tz, users.name "
            "FROM tracks, users "
            "WHERE tracks.owner_id = users.id;"
        )
        for row in connection.execute(sql):
            track_id, title, description, date_raw, date_tz, author_name = row
            if isinstance(date_raw, str):
                date_raw = datetime.datetime.strptime(date_raw, "%Y-%m-%d %H:%M:%S.%f")
            if date_tz is None:
                timezone = datetime.timezone.utc
            else:
                timezone = datetime.timezone(datetime.timedelta(minutes=date_tz))
            date = date_raw.replace(tzinfo=timezone)

            self.tell(f"Embedding metadata for track {track_id}")
            track_dir = data_dir / "tracks" / str(track_id)
            gpx_path = track_dir / "track.gpx.br"

            raw_gpx = brotli.decompress(gpx_path.read_bytes())
            gpx = gpxpy.parse(raw_gpx)

            for track in gpx.tracks:
                track.name = None
                track.description = None

            gpx.author_name = author_name
            gpx.name = title
            gpx.description = description
            gpx.time = date

            gpx_path.write_bytes(brotli.compress(gpx.to_xml().encode("utf-8"), quality=4))

    def post_alembic(self, config):
        pass


class Down(UpdateScript):
    def pre_alembic(self, config):
        pass

    def post_alembic(self, config):
        pass
