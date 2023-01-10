import pytest


def pytest_addoption(parser):
    group = parser.getgroup('snapshot')
    group.addoption(
        '--approve',
        action='store_true',
        help='Update snapshot files instead of testing against them.',
    )

@pytest.fixture
def approve(request):
    return request.config.getoption('--approve')
    