# heath --- Manage projections
# Copyright © 2021, 2022 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import tempfile
from typing import Any, Iterator

import pytest
from bles import Status
from blessql import LEDGER_REGISTRY, Ledger
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from typer import Typer
from typer.testing import CliRunner

from heath import app as heath_app


@pytest.fixture()
def runner() -> Iterator[CliRunner]:
    yield CliRunner()


@pytest.fixture()
def app() -> Iterator[Typer]:
    yield heath_app


@pytest.fixture()
def dsn() -> Iterator[str]:
    # We cannot use ":memory:" because the app create one connection per request
    with tempfile.NamedTemporaryFile() as a_file:
        yield f"sqlite:///{a_file.name}"


@pytest.fixture()
def init_ledger(dsn: str) -> Any:
    e_engine = create_engine(dsn)
    LEDGER_REGISTRY.metadata.create_all(e_engine)
    yield True
    LEDGER_REGISTRY.metadata.drop_all(e_engine)


@pytest.fixture()
def populated_ledger(dsn: str, init_ledger: bool) -> Iterator[Ledger]:
    with sessionmaker(bind=create_engine(dsn))() as session:
        ledger = Ledger(session)
        ledger.register("a_projector")
        ledger.register("a_stalled_projector")
        ledger.mark_as("a_stalled_projector", Status.STALLED)
        ledger.register("a_broken_projector")
        ledger.mark_as("a_broken_projector", Status.BROKEN)
        ledger.register("a_retired_projector")
        ledger.mark_as("a_retired_projector", Status.RETIRED)
        session.commit()
        yield ledger


@pytest.fixture()
def db_dsn(dsn: str, populated_ledger: Ledger) -> Iterator[str]:
    yield dsn
