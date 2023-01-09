#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Module to read/write ASDF files."""

from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterator, Mapping, Sequence, Union

if TYPE_CHECKING:
    import pandas as pd


def to_asdf(filename: Union[str, Path], dct: Mapping[str, Any]) -> None:
    """Write data to a ASDF file."""
    try:
        import asdf
    except ImportError as exc:
        raise ImportError(
            "Missing optional package 'asdf'.\n"
            "Please install it with 'pip install pyxel-sim[io]' "
            "or 'pip install pyxel-sim[all]'"
        ) from exc

    if dct["version"] != 1:
        raise NotImplementedError

    # Convert a 'DataFrame' into a `dict`
    df: pd.DataFrame = dct["data"]["charge"]["frame"]
    frame_dct: Mapping[str, Sequence[float]] = df.to_dict(orient="list")

    dct["data"]["charge"]["frame"] = frame_dct

    with asdf.AsdfFile(dct) as af:
        af.write_to(filename)


@contextmanager
def from_asdf(filename: Union[str, Path]) -> Iterator[Mapping[str, Any]]:
    """Read data from a HDF5 file."""
    import pandas as pd

    try:
        import asdf
    except ImportError as exc:
        raise ImportError(
            "Missing optional package 'asdf'.\n"
            "Please install it with 'pip install pyxel-sim[io]' "
            "or 'pip install pyxel-sim[all]'"
        ) from exc

    dct: Dict[str, Any] = {}

    with asdf.open(filename, copy_arrays=True) as af:
        # TODO: Use a JSON schema to validate 'dct'
        if "version" not in af:
            raise ValueError("Missing 'version' !")

        version: int = af["version"]
        if version != 1:
            raise NotImplementedError

        dct["version"] = version

        if "type" not in af:
            raise ValueError("Missing 'type' !")

        dct["type"] = af["type"]

        # Get properties
        dct["properties"] = af["properties"]
        dct["data"] = af["data"]

        # Convert a 'dict' to a 'DataFrame'
        frame_dct: Mapping[str, Sequence[float]] = dct["data"]["charge"]["frame"]
        df = pd.DataFrame(frame_dct)

        dct["data"]["charge"]["frame"] = df

        yield dct
