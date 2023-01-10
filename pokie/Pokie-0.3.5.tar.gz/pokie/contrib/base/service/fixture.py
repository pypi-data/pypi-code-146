from typing import Any, Optional, List

from rick.base import Di
from rick.mixin import Injectable, Runnable
from rick.util.loader import load_class

from pokie.constants import DI_DB, DI_APP
from pokie.contrib.base.dto import FixtureRecord
from pokie.contrib.base.repository.fixture import FixtureRepository


class FixtureError(Exception):
    pass


class FixtureService(Injectable):
    def __init__(self, di: Di):
        super().__init__(di)
        self.db = di.get(DI_DB)

    def list(self) -> List[FixtureRecord]:
        return self.repo_fixture.fetch_all()

    def add(self, record: FixtureRecord):
        self.repo_fixture.insert_pk(record)

    def scan(self):
        """
        Scans all modules for fixture definitions
        :return: list
        """
        result = []
        app = self.get_di().get(DI_APP)
        for name, module in app.modules.items():
            fixtures = getattr(module, "fixtures", None)
            if fixtures:
                if not isinstance(fixtures, (list, tuple)):
                    raise TypeError(
                        "FixtureManager: invalid data type for fixture list in module '{}'".format(
                            name
                        )
                    )
                result.extend(fixtures)
        return result

    def execute(self, fixture_name: str):
        """
        Attempts to load a fixture and execute it
        :param fixture_name:
        :return:
        """
        cls = load_class(fixture_name)
        if cls is None:
            raise FixtureError(
                "FixtureManager: cannot locate fixture class '{}'".format(fixture_name)
            )

        if not issubclass(cls, (Injectable, Runnable)):
            raise FixtureError(
                "FixtureManager: class '{}' must implement Injectable, Runnable mixins".format(
                    fixture_name
                )
            )

        di = self.get_di()
        fixture = cls(di)
        fixture.run(di)

    @property
    def repo_fixture(self) -> FixtureRepository:
        return FixtureRepository(self.db)
