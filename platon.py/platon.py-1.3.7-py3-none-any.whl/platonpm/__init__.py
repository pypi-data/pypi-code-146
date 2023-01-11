from pathlib import Path


ETHPM_DIR = Path(__file__).parent
ASSETS_DIR = ETHPM_DIR / "assets"


def get_platonpm_spec_dir() -> Path:
    platonpm_spec_dir = ETHPM_DIR / "platonpm-spec"
    v3_spec = platonpm_spec_dir / "spec" / "v3.spec.json"
    if not v3_spec.is_file():
        raise FileNotFoundError(
            "The platonpm-spec submodule is not available. "
            "Please import the submodule with `git submodule update --init`"
        )
    return platonpm_spec_dir


from .package import Package
from .backends.registry import RegistryURI
