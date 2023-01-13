import json
from pathlib import Path
from typing import Optional, Type

import pytest

from pglift import prometheus
from pglift.models import helpers, interface
from pglift.types import Manifest


def test_argspec_from_instance_manifest(
    datadir: Path,
    write_changes: bool,
    composite_instance_model: Type[interface.Instance],
) -> None:
    compare_argspec(composite_instance_model, write_changes, datadir)


@pytest.mark.parametrize(
    "manifest_type",
    [
        prometheus.PostgresExporter,
        interface.Role,
        interface.Database,
    ],
)
def test_argspec_from_model_manifest(
    datadir: Path, write_changes: bool, manifest_type: Type[Manifest]
) -> None:
    compare_argspec(manifest_type, write_changes, datadir)


def compare_argspec(
    manifest_type: Type[Manifest],
    write_changes: bool,
    datadir: Path,
    *,
    name: Optional[str] = None,
) -> None:
    actual = helpers.argspec_from_model(manifest_type)
    if name is None:
        name = manifest_type.__name__.lower()
    fpath = datadir / f"ansible-argspec-{name}.json"
    if write_changes:
        fpath.write_text(json.dumps(actual, indent=2, sort_keys=True) + "\n")
    expected = json.loads(fpath.read_text())
    assert actual == expected
