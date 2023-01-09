from pathlib import Path

from nbproject._logger import logger
from nbproject.dev import test


def test_notebooks():
    # assuming this is in the tests dir
    docs_dir = Path(__file__).parents[1] / "docs/"

    for check_dir in docs_dir.glob("./**"):
        # these are the notebook testpaths
        if not str(check_dir).endswith(("guides", "tutorials")):
            continue
        logger.debug(f"\n{check_dir}")
        test.execute_notebooks(check_dir, write=True)
