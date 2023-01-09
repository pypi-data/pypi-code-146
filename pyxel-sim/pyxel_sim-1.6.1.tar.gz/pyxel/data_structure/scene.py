#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Pyxel Scene class to track multi-wavelength photon."""

from typing import TYPE_CHECKING, Mapping, Sequence

if TYPE_CHECKING:
    import numpy as np
    from astropy.io.fits import ImageHDU
    from astropy.table import Table
    from scopesim import Source


class Scene:
    """Scene class defining and storing information of all multi-wavelength photon."""

    def __init__(self, source: "Source"):
        self._source: Source = source

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.data == other.data

    # TODO: This method will be removed in the future.
    #       If you want to have a `Source` object, you should use method '.to_scopesim'
    @property
    def data(self) -> "Source":
        """Get a multi-wavelength object."""
        return self._source

    def from_scopesim(self, source: "Source") -> None:
        """Convert a ScopeSim `Source` object into a `Scene` object.

        Parameters
        ----------
        source : scopesim.Source
            Object to convert to a `Scene` object.

        Raises
        ------
        RuntimeError
            If package 'scopesim' is not installed.
        TypeError
            If input parameter 'source' is not a ScopeSim `Source` object.

        Notes
        -----
        More information about ScopeSim `Source` objects at
        this link: https://scopesim.readthedocs.io/en/latest/reference/scopesim.source.source.html
        """
        try:
            from scopesim import Source
        except ImportError as exc:
            raise RuntimeError(
                "Package 'scopesim' is not installed ! "
                "Please run command 'pip install scopesim' from the command line."
            ) from exc

        if not isinstance(source, Source):
            raise TypeError("Expecting a ScopeSim `Source` object for 'source'.")

    def to_scopesim(self) -> "Source":
        """Convert this `Scene` object into a ScopeSim `Source` object.

        Returns
        -------
        Source
            A ScopeSim `Source` object.

        Notes
        -----
        More information about ScopeSim `Source` objects at
        this link: https://scopesim.readthedocs.io/en/latest/reference/scopesim.source.source.html
        """
        return self._source

    def to_dict(self) -> Mapping:
        """Convert an instance of `Scene` to a `dict`."""
        meta: Mapping = self._source.meta
        table_fields: Sequence[Table] = self._source.table_fields
        image_fields: Sequence[ImageHDU] = self._source.image_fields

        # Create 'tables'
        tables: Sequence[Mapping] = [
            {
                "data": table.to_pandas(),
                "units": {
                    key.replace("_unit", ""): value
                    for key, value in table.meta.items()
                    if key.endswith("_unit")
                },
            }
            for table in table_fields
        ]

        images: Sequence[Mapping] = [
            {"header": dict(image.header), "data": np.asarray(image.data)}
            for image in image_fields
        ]

        return {"meta": meta, "tables": tables, "images": images}

    @classmethod
    def from_dict(cls, dct: Mapping) -> "Scene":
        """Create a new instance of a `Scene` object from a `dict`."""
        from astropy.io.fits import Header, ImageHDU
        from astropy.table import Table
        from scopesim import Source

        meta: Mapping = dct["meta"]
        tables: Mapping = dct["tables"]
        images: Mapping = dct["images"]

        table_fields: Sequence[Table] = [
            Table.from_pandas(dataframe=table["data"], units=table["units"])
            for table in tables
        ]

        image_fields: Sequence[ImageHDU] = [
            ImageHDU(data=img["data"], header=Header(img["header"])) for img in images
        ]

        src: Source = Source(
            meta=meta,
            image_fields=image_fields,
            table_fields=table_fields,
        )

        return cls(src)
