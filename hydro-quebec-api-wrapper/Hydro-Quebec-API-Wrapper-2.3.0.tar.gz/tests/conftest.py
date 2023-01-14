"""pytest configuration file."""
import typing


@typing.no_type_check
def pytest_addoption(parser):
    """Add available option to pytest command."""
    parser.addoption(
        "--new-contract",
        action="store_true",
        default=False,
        help="The contract is now, no history available",
    )
