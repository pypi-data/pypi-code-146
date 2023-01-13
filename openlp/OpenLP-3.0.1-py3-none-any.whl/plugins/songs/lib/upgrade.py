# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2023 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
The :mod:`upgrade` module provides a way for the database and schema that is the
backend for the Songs plugin
"""
import json
import logging
from pathlib import Path

from sqlalchemy import Column, ForeignKey, Table, types
from sqlalchemy.sql.expression import false, func, null, text

from openlp.core.common import sha256_file_hash
from openlp.core.common.applocation import AppLocation
from openlp.core.common.db import drop_columns
from openlp.core.common.json import OpenLPJSONEncoder, OpenLPJSONDecoder
from openlp.core.lib.db import PathType, get_upgrade_op


log = logging.getLogger(__name__)
__version__ = 8


# TODO: When removing an upgrade path the ftw-data needs updating to the minimum supported version
def upgrade_1(session, metadata):
    """
    Version 1 upgrade.

    This upgrade removes the many-to-many relationship between songs and
    media_files and replaces it with a one-to-many, which is far more
    representative of the real relationship between the two entities.

    In order to facilitate this one-to-many relationship, a song_id column is
    added to the media_files table, and a weight column so that the media
    files can be ordered.

    :param session:
    :param metadata:
    """
    op = get_upgrade_op(session)
    metadata.reflect()
    if 'media_files_songs' in [t.name for t in metadata.tables.values()]:
        op.drop_table('media_files_songs')
        op.add_column('media_files', Column('song_id', types.Integer(), server_default=null()))
        op.add_column('media_files', Column('weight', types.Integer(), server_default=text('0')))
        if metadata.bind.url.get_dialect().name != 'sqlite':
            # SQLite doesn't support ALTER TABLE ADD CONSTRAINT
            op.create_foreign_key('fk_media_files_song_id', 'media_files', 'songs', ['song_id', 'id'])
    else:
        log.warning('Skipping upgrade_1 step of upgrading the song db')


def upgrade_2(session, metadata):
    """
    Version 2 upgrade.

    This upgrade adds a create_date and last_modified date to the songs table
    """
    op = get_upgrade_op(session)
    songs_table = Table('songs', metadata, autoload=True)
    if 'create_date' not in [col.name for col in songs_table.c.values()]:
        op.add_column('songs', Column('create_date', types.DateTime(), default=func.now()))
        op.add_column('songs', Column('last_modified', types.DateTime(), default=func.now()))
    else:
        log.warning('Skipping upgrade_2 step of upgrading the song db')


def upgrade_3(session, metadata):
    """
    Version 3 upgrade.

    This upgrade adds a temporary song flag to the songs table
    """
    op = get_upgrade_op(session)
    songs_table = Table('songs', metadata, autoload=True)
    if 'temporary' not in [col.name for col in songs_table.c.values()]:
        if metadata.bind.url.get_dialect().name == 'sqlite':
            op.add_column('songs', Column('temporary', types.Boolean(create_constraint=False), server_default=false()))
        else:
            op.add_column('songs', Column('temporary', types.Boolean(), server_default=false()))
    else:
        log.warning('Skipping upgrade_3 step of upgrading the song db')


def upgrade_4(session, metadata):
    """
    Version 4 upgrade.

    This upgrade adds a column for author type to the authors_songs table
    """
    # This is now empty due to a bug in the upgrade
    pass


def upgrade_5(session, metadata):
    """
    Version 5 upgrade.

    This upgrade adds support for multiple songbooks
    """
    # This is now empty due to a bug in the upgrade
    pass


def upgrade_6(session, metadata):
    """
    Version 6 upgrade

    This version corrects the errors in upgrades 4 and 5
    """
    op = get_upgrade_op(session)
    metadata.reflect()
    # Move upgrade 4 to here and correct it (authors_songs table, not songs table)
    authors_songs = Table('authors_songs', metadata, autoload=True)
    if 'author_type' not in [col.name for col in authors_songs.c.values()]:
        # Since SQLite doesn't support changing the primary key of a table, we need to recreate the table
        # and copy the old values
        op.create_table(
            'authors_songs_tmp',
            Column('author_id', types.Integer(), ForeignKey('authors.id'), primary_key=True),
            Column('song_id', types.Integer(), ForeignKey('songs.id'), primary_key=True),
            Column('author_type', types.Unicode(255), primary_key=True,
                   nullable=False, server_default=text('""'))
        )
        op.execute('INSERT INTO authors_songs_tmp SELECT author_id, song_id, "" FROM authors_songs')
        op.drop_table('authors_songs')
        op.rename_table('authors_songs_tmp', 'authors_songs')
    # Move upgrade 5 here to correct it
    if 'songs_songbooks' not in [t.name for t in metadata.tables.values()]:
        # Create the mapping table (songs <-> songbooks)
        op.create_table(
            'songs_songbooks',
            Column('songbook_id', types.Integer(), ForeignKey('song_books.id'), primary_key=True),
            Column('song_id', types.Integer(), ForeignKey('songs.id'), primary_key=True),
            Column('entry', types.Unicode(255), primary_key=True, nullable=False)
        )

        # Migrate old data
        op.execute('INSERT INTO songs_songbooks SELECT song_book_id, id, song_number FROM songs\
                    WHERE song_book_id IS NOT NULL AND song_number IS NOT NULL AND song_book_id <> 0')

        # Drop old columns
        if metadata.bind.url.get_dialect().name == 'sqlite':
            drop_columns(op, 'songs', ['song_book_id', 'song_number'])
        else:
            op.drop_constraint('songs_ibfk_1', 'songs', 'foreignkey')
            op.drop_column('songs', 'song_book_id')
            op.drop_column('songs', 'song_number')
    # Finally, clean up our mess in people's databases
    op.execute('DELETE FROM songs_songbooks WHERE songbook_id = 0')


def upgrade_7(session, metadata):
    """
    Version 7 upgrade - Move file path from old db to JSON encoded path to new db. Upgrade added in 2.5 dev
    """
    log.debug('Starting upgrade_7 for file_path to JSON')
    old_table = Table('media_files', metadata, autoload=True)
    if 'file_path' not in [col.name for col in old_table.c.values()]:
        op = get_upgrade_op(session)
        op.add_column('media_files', Column('file_path', PathType()))
        conn = op.get_bind()
        results = conn.execute('SELECT * FROM media_files')
        data_path = AppLocation.get_data_path()
        for row in results.fetchall():
            file_path_json = json.dumps(Path(row.file_name), cls=OpenLPJSONEncoder, base_path=data_path)
            sql = 'UPDATE media_files SET file_path = :file_path WHERE id = :id'
            conn.execute(sql, {'file_path': file_path_json, 'id': row.id})
        # Drop old columns
        if metadata.bind.url.get_dialect().name == 'sqlite':
            drop_columns(op, 'media_files', ['file_name', ])
        else:
            op.drop_constraint('media_files', 'foreignkey')
            op.drop_column('media_files', 'filenames')


def upgrade_8(session, metadata):
    """
    Version 8 upgrade - add sha256 hash to media
    """
    log.debug('Starting upgrade_8 for adding sha256 hashes')
    old_table = Table('media_files', metadata, autoload=True)
    if 'file_hash' not in [col.name for col in old_table.c.values()]:
        op = get_upgrade_op(session)
        op.add_column('media_files', Column('file_hash', types.Unicode(128)))
        conn = op.get_bind()
        results = conn.execute('SELECT * FROM media_files')
        data_path = AppLocation.get_data_path()
        for row in results.fetchall():
            file_path = json.loads(row.file_path, cls=OpenLPJSONDecoder)
            full_file_path = data_path / file_path
            if full_file_path.exists():
                hash = sha256_file_hash(full_file_path)
            else:
                log.warning('{audio} does not exists, so no sha256 hash added.'.format(audio=str(file_path)))
                # set a fake "hash" to allow for the upgrade to go through. The image will be marked as invalid
                hash = 'NONE'
            sql = 'UPDATE media_files SET file_hash = :hash WHERE id = :id'
            conn.execute(sql, {'hash': hash, 'id': row.id})
