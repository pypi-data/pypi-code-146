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

import os

from mock import patch
from typer import Typer
from typer.testing import CliRunner


class TestInit:
    def test_ok(self, runner: CliRunner, app: Typer, dsn: str) -> None:
        with patch.dict(os.environ, {"HEATH_DSN": dsn}):
            result = runner.invoke(app, ["init"])
            assert result.exit_code == 0


class TestStatus:
    def test_ok(self, runner: CliRunner, app: Typer, db_dsn: str) -> None:
        with patch.dict(os.environ, {"HEATH_DSN": db_dsn}):
            result = runner.invoke(app, ["status"])
            assert result.exit_code == 0


class TestPurge:
    def test_ok(self, runner: CliRunner, app: Typer, db_dsn: str) -> None:
        with patch.dict(os.environ, {"HEATH_DSN": db_dsn}):
            result = runner.invoke(app, ["purge", "a_projector", "--force"])
            assert result.exit_code == 0

    def test_unknown_projector(self, runner: CliRunner, app: Typer, db_dsn: str) -> None:
        with patch.dict(os.environ, {"HEATH_DSN": db_dsn}):
            result = runner.invoke(app, ["purge", "an_unknown_projector", "--force"])
            assert result.exit_code == 1

    def test_stalled_projector(self, runner: CliRunner, app: Typer, db_dsn: str) -> None:
        with patch.dict(os.environ, {"HEATH_DSN": db_dsn}):
            result = runner.invoke(app, ["purge", "a_stalled_projector", "--force"])
            assert result.exit_code == 0

    def test_broken_projector(self, runner: CliRunner, app: Typer, db_dsn: str) -> None:
        with patch.dict(os.environ, {"HEATH_DSN": db_dsn}):
            result = runner.invoke(app, ["purge", "a_broken_projector", "--force"])
            assert result.exit_code == 0

    def test_retired_projector(self, runner: CliRunner, app: Typer, db_dsn: str) -> None:
        with patch.dict(os.environ, {"HEATH_DSN": db_dsn}):
            result = runner.invoke(app, ["purge", "a_retired_projector", "--force"])
            assert result.exit_code == 0


class TestStall:
    def test_ok(self, runner: CliRunner, app: Typer, db_dsn: str) -> None:
        with patch.dict(os.environ, {"HEATH_DSN": db_dsn}):
            result = runner.invoke(app, ["stall", "a_projector"])
            assert result.exit_code == 0

    def test_unknown_projector(self, runner: CliRunner, app: Typer, db_dsn: str) -> None:
        with patch.dict(os.environ, {"HEATH_DSN": db_dsn}):
            result = runner.invoke(app, ["stall", "an_unknown_projector"])
            assert result.exit_code == 1
