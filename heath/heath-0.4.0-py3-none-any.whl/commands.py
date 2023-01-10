# heath --- Manage projections
# Copyright © 2022 Bioneland
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

from dataclasses import dataclass
from typing import Callable

from bles import Status
from blessql import LEDGER_REGISTRY, Ledger
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore


@dataclass
class ProjectionInfo:
    name: str
    status: str
    position: int


class UnknownProjection(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"Unknown projection `{name}`!")


def session_maker(dsn: str) -> sessionmaker:
    return sessionmaker(bind=create_engine(dsn))()


def initialise(dsn: str) -> None:
    LEDGER_REGISTRY.metadata.create_all(create_engine(dsn))


def status(dsn: str, echo: Callable[[str], None]) -> None:
    echo(_serialize_info(_collect_info(dsn)))


def _collect_info(dsn: str) -> list[ProjectionInfo]:
    data: list[ProjectionInfo] = []
    with session_maker(dsn) as session:
        ledger = Ledger(session)
        ledger.status(
            lambda status, name, position: data.append(
                ProjectionInfo(name, status, int(position))
            )
        )
    return data


def _serialize_info(data: list[ProjectionInfo]) -> str:
    text = _status_summary(data)
    for d in data:
        text += f"\n[{d.status}] `{d.name}` at position {d.position}."
    return text


def _status_summary(data: list[ProjectionInfo]) -> str:
    if not data:
        return "WARNING: no projections are registered."

    broken = [d for d in data if d.status == "BROKEN"]
    other = [d for d in data if d.status != "BROKEN" and d.status != "OK"]
    if broken:
        return (
            "CRITICAL: some projections are broken"
            + " ("
            + ", ".join([f"'{b.name}'" for b in broken])
            + ")."
        )
    elif other:
        return (
            "WARNING: some projections are not OK"
            + " ("
            + ", ".join([f"'{o.name}'" for o in other])
            + ")."
        )
    else:
        return "OK: all projections are OK."


def purge(dsn: str, name: str) -> None:
    with session_maker(dsn) as session:
        ledger = Ledger(session)
        if not ledger.knows(name):
            raise UnknownProjection(name)

        ledger.forget(name)
        create_engine(dsn).connect().execute(f"DROP TABLE IF EXISTS {name}")
        session.commit()


def stall(dsn: str, name: str) -> None:
    with session_maker(dsn) as session:
        ledger = Ledger(session)
        if not ledger.knows(name):
            raise UnknownProjection(name)

        ledger.mark_as(name, Status.STALLED)
        session.commit()
