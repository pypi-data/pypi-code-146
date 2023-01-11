from pydantic import BaseModel, Extra, Field
from abc import ABC
from typing import Optional, Literal, Mapping, Union
from .externaldate import ExternalDate
from .input import Input
from .parameters import Parameters, Timestamps, Timestamp

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


class Parser(BaseModel, ABC, extra=Extra.forbid):
    """Template ABC for parser classes."""

    parser: str
    input: Input
    filetype: Optional[str]
    parameters: Optional[Parameters]
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class Dummy(Parser):
    """Dummy parser type, useful for testing."""

    class Parameters(BaseModel, extra=Extra.allow):
        pass

    parser: Literal["dummy"]
    parameters: Optional[Parameters]


class BasicCSV(Parser):
    """Customisable tabulated file parser."""

    class Parameters(BaseModel, extra=Extra.forbid):
        sep: str = ","
        """Separator of table columns."""

        strip: str = None
        """A :class:`str` of characters to strip from headers & data."""

        units: Optional[Mapping[str, str]]
        """A :class:`dict` containing ``column: unit`` keypairs."""

        timestamp: Optional[Timestamps]
        """Timestamp specification allowing calculation of Unix timestamp for
        each table row."""

    parser: Literal["basiccsv"]
    parameters: Parameters = Field(default_factory=Parameters)


class MeasCSV(Parser, extra=Extra.forbid):
    """
    Legacy file parser for ``measurement.csv`` files from FHI.

    .. note::

        This parser is deprecated, and the :class:`BasicCSV` parser should be
        used instead.

    """

    class Parameters(BaseModel, extra=Extra.forbid):
        timestamp: Timestamps = Field(
            Timestamp(timestamp={"index": 0, "format": "%Y-%m-%d-%H-%M-%S"})
        )

    parser: Literal["meascsv"]
    parameters: Parameters = Field(default_factory=Parameters)


class FlowData(Parser):
    """Parser for flow controller/meter data."""

    parser: Literal["flowdata"]
    filetype: Literal["drycal.csv", "drycal.rtf", "drycal.txt"] = "drycal.csv"


class ElectroChem(Parser):
    """Parser for electrochemistry files."""

    class Parameters(BaseModel, extra=Extra.forbid):
        transpose: bool = True
        """Transpose impedance data into traces (default) or keep as timesteps."""

    class Input(Input):
        encoding: str = "windows-1252"

    parser: Literal["electrochem"]
    input: Input
    filetype: Literal["eclab.mpt", "eclab.mpr", "tomato.json"] = "eclab.mpr"
    parameters: Parameters = Field(default_factory=Parameters)


class ChromTrace(Parser):
    """
    Parser for raw chromatography traces.

    .. note::

        For parsing processed (integrated) chromatographic data, use the
        :class:`ChromData` parser.

    """

    parser: Literal["chromtrace"]
    filetype: Literal[
        "ezchrom.asc",
        "fusion.json",
        "fusion.zip",
        "agilent.ch",
        "agilent.dx",
        "agilent.csv",
    ] = "ezchrom.asc"


class ChromData(Parser):
    """Parser for processed chromatography data."""

    parser: Literal["chromdata"]
    filetype: Literal[
        "fusion.json",
        "fusion.zip",
        "fusion.csv",
        "empalc.csv",
        "empalc.xlsx",
    ] = "fusion.json"


class MassTrace(Parser):
    """Parser for mass spectroscopy traces."""

    parser: Literal["masstrace"]
    filetype: Literal["quadstar.sac"] = "quadstar.sac"


class QFTrace(Parser):
    """Parser for network analyzer traces."""

    parser: Literal["qftrace"]
    filetype: Literal["labview.csv"] = "labview.csv"


class XPSTrace(Parser):
    """Parser for XPS traces."""

    parser: Literal["xpstrace"]
    filetype: Literal["phi.spe"] = "phi.spe"


class XRDTrace(Parser):
    """Parser for XRD traces."""

    parser: Literal["xrdtrace"]
    filetype: Literal[
        "panalytical.xy",
        "panalytical.csv",
        "panalytical.xrdml",
    ] = "panalytical.csv"


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
