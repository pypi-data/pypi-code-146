from pathlib import Path
from typing import List

import pytest

from gl_parser.models import ParserConfig


@pytest.fixture(scope='session')
def output_folder():
    folder = Path(__file__).parent.parent / 'output'
    return folder


@pytest.fixture(scope='session')
def fixtures_folder():
    folder = Path(__file__).parent.parent / 'tests' / 'fixtures'
    return folder


@pytest.fixture(scope='function')
def default_parser_config() -> ParserConfig:
    parser_config = ParserConfig()
    return parser_config


@pytest.fixture(scope='function')
def page_headers() -> List[str]:
    headers = ['My Super company, Inc.', 'General Ledger',
               'For the Period From Jan 1, 2022 to Sep 30, 2022',
               'Filter Criteria includes: Report order is by ID. Report is printed in Detail Format. ']
    return headers
