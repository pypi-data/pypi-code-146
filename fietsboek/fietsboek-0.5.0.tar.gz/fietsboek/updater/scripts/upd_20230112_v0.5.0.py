"""Revision upgrade script v0.5.0

Date created: 2023-01-12 20:30:35.424420
"""
from fietsboek.updater.script import UpdateScript

update_id = 'v0.5.0'
previous = [
    'lu8w3rwlz4ddcpms',
]
alembic_revision = 'c939800af428'


class Up(UpdateScript):
    def pre_alembic(self, config):
        pass

    def post_alembic(self, config):
        pass


class Down(UpdateScript):
    def pre_alembic(self, config):
        pass

    def post_alembic(self, config):
        pass
