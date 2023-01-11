import json
from typing import (
    Any,
    Dict,
)

from platonpm import (
    ASSETS_DIR,
    get_platonpm_spec_dir,
)


def get_platonpm_spec_manifest(use_case: str, filename: str) -> Dict[str, Any]:
    platonpm_spec_dir = get_platonpm_spec_dir()
    return json.loads((platonpm_spec_dir / 'examples' / use_case / filename).read_text())


def get_platonpm_local_manifest(use_case: str, filename: str) -> Dict[str, Any]:
    return json.loads((ASSETS_DIR / use_case / filename).read_text())
