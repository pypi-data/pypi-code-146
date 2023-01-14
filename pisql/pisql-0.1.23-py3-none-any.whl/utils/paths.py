import os
import json
from pathlib import Path

package_dir = Path(__file__).parent.parent
base_dir = package_dir.parent
tests_dir = base_dir / "tests"
assets_dir = package_dir / "assets"
data_dir = assets_dir / "data"

pisql_home = Path(os.path.expanduser("~")) / "pisql"

config = json.loads(open(assets_dir / "config.json", "r").read())