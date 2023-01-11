import json
from pathlib import (
    Path,
)
import pytest
from typing import (
    Callable,
)

from platonpm import (
    Package,
)
from platon import Web3
from platon.tools.pytest_platon.deployer import (
    Deployer,
)


@pytest.fixture
def deployer(w3: Web3) -> Callable[[Path], Deployer]:
    """
    Returns a `Deployer` instance composed from a `Package` instance
    generated from the manifest located at the provided `path` folder.
    """

    def _deployer(path: Path) -> Deployer:
        manifest = json.loads(path.read_text())
        package = Package(manifest, w3)
        return Deployer(package)

    return _deployer
