from pydantic import BaseModel, Extra, Field
from typing import Optional, Literal, Mapping, Any, Union
from .externaldate import ExternalDate
from .input import Input
from .parameters import Tol, Timestamps, Timestamp

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


class Dummy(BaseModel, extra=Extra.forbid):
    """Dummy parser type, useful for testing."""

    class Params(BaseModel, extra=Extra.allow):
        pass

    parser: Literal["dummy"]
    input: Input
    parameters: Optional[Params]
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class BasicCSV(BaseModel, extra=Extra.forbid):
    """Customisable tabulated file parser."""

    class Params(BaseModel, extra=Extra.forbid):
        sep: str = ","
        """Separator of table columns."""

        strip: str = None
        """A :class:`str` of characters to strip from headers & data."""

        units: Optional[Mapping[str, str]]
        """A :class:`dict` containing ``column: unit`` keypairs."""

        timestamp: Optional[Timestamps]
        """Timestamp specification allowing calculation of Unix timestamp for
        each table row."""

        sigma: Optional[Mapping[str, Tol]] = Field(None, deprecated=True)
        """
        External uncertainty specification.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

        calfile: Optional[str] = Field(None, deprecated=True)
        """
        Column calibration specification.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

        convert: Optional[Any] = Field(None, deprecated=True)
        """
        Column renaming specification.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

    parser: Literal["basiccsv"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class MeasCSV(BaseModel, extra=Extra.forbid):
    """
    Legacy file parser for ``measurement.csv`` files from FHI.

    .. note::

        This parser is deprecated, and the :class:`BasicCSV` parser should be
        used instead.

    """

    class Params(BaseModel, extra=Extra.forbid):
        timestamp: Timestamps = Field(
            Timestamp(timestamp={"index": 0, "format": "%Y-%m-%d-%H-%M-%S"})
        )

        calfile: Optional[str] = Field(None, deprecated=True)
        """
        Column calibration specification.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

        convert: Optional[Any] = Field(None, deprecated=True)
        """
        Column renaming specification.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

    parser: Literal["meascsv"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class FlowData(BaseModel, extra=Extra.forbid):
    """Parser for flow controller/meter data."""

    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["drycal.csv", "drycal.rtf", "drycal.txt"] = "drycal.csv"

        calfile: Optional[str] = Field(None, deprecated=True)
        """
        Column calibration specification.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

        convert: Optional[Any] = Field(None, deprecated=True)
        """
        Column renaming specification.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

    parser: Literal["flowdata"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class ElectroChem(BaseModel, extra=Extra.forbid):
    """Parser for electrochemistry files."""

    class Params(BaseModel, extra=Extra.forbid):

        filetype: Literal["eclab.mpt", "eclab.mpr", "tomato.json"] = "eclab.mpr"

        transpose: bool = True
        """Transpose impedance data into traces (default) or keep as timesteps."""

    class Input(Input):
        encoding: str = "windows-1252"

    parser: Literal["electrochem"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class ChromTrace(BaseModel, extra=Extra.forbid):
    """
    Parser for raw chromatography traces.

    .. note::

        For parsing processed (integrated) chromatographic data, use the
        :class:`ChromData` parser.

    """

    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal[
            "ezchrom.asc",
            "fusion.json",
            "fusion.zip",
            "agilent.ch",
            "agilent.dx",
            "agilent.csv",
        ] = "ezchrom.asc"

        calfile: Optional[str] = Field(None, deprecated=True)
        """
        Species calibration specification.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

        species: Optional[Any] = Field(None, deprecated=True)
        """
        Species information as a :class:`dict`.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

        detectors: Optional[Any] = Field(None, deprecated=True)
        """
        Detector integration parameters as a :class:`dict`.

        .. admonition:: DEPRECATED in ``DataSchema-4.2``

            This feature is deprecated as of ``yadg-4.2`` and will
            stop working in ``yadg-5.0``.

        """

    parser: Literal["chromtrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class ChromData(BaseModel, extra=Extra.forbid):
    """Parser for processed chromatography data."""

    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal[
            "fusion.json",
            "fusion.zip",
            "fusion.csv",
            "empalc.csv",
            "empalc.xlsx",
        ] = "fusion.json"

    parser: Literal["chromdata"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class MassTrace(BaseModel, extra=Extra.forbid):
    """Parser for mass spectroscopy traces."""

    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["quadstar.sac"] = "quadstar.sac"

    parser: Literal["masstrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class QFTrace(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    """Parser for network analyzer traces."""

    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["labview.csv"] = "labview.csv"
        method: Literal["naive", "lorentz", "kajfez"] = "kajfez"
        height: float = 1.0
        distance: float = 5000.0
        cutoff: float = 0.4
        threshold: float = 1e-6

    parser: Literal["qftrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class XPSTrace(BaseModel, extra=Extra.forbid):
    """Parser for XPS traces."""

    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["phi.spe"] = "phi.spe"

    parser: Literal["xpstrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class XRDTrace(BaseModel, extra=Extra.forbid):
    """Parser for XRD traces."""

    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal[
            "panalytical.xy",
            "panalytical.csv",
            "panalytical.xrdml",
        ] = "panalytical.csv"

    parser: Literal["xrdtrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


Steps = Annotated[
    Union[
        Dummy,
        BasicCSV,
        MeasCSV,
        FlowData,
        ElectroChem,
        ChromTrace,
        ChromData,
        MassTrace,
        QFTrace,
        XPSTrace,
        XRDTrace,
    ],
    Field(discriminator="parser"),
]
