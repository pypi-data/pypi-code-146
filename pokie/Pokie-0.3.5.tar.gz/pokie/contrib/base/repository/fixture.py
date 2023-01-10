from rick_db import Repository
from pokie.contrib.base.dto import FixtureRecord


class FixtureRepository(Repository):
    def __init__(self, db):
        super().__init__(db, FixtureRecord)
