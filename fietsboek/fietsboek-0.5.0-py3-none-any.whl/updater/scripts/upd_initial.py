"""Revision upgrade script initial.

Date created: 2022-11-12 18:20:07.214366
"""
from fietsboek.updater.script import UpdateScript

update_id = 'initial'
previous = [
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
