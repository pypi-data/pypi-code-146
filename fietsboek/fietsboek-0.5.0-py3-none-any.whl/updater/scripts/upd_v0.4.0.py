"""Revision upgrade script v0.4.0

Date created: 2022-11-28 20:16:35.062503
"""
from fietsboek.updater.script import UpdateScript

update_id = 'v0.4.0'
previous = [
    'initial',
]
alembic_revision = 'd085998b49ca'


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
