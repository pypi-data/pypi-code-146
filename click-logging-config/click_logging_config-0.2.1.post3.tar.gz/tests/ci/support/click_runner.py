#
#  Copyright (c) 2020 Russell Smiley
#
#  This file is part of click_logging_config.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import pytest
from click.testing import CliRunner


@pytest.fixture()
def click_runner() -> CliRunner:
    return CliRunner()
