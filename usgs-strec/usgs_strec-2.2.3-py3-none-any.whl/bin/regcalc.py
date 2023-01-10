#!/usr/bin/env python

# stdlib imports
import sys
from enum import Enum
from typing import Tuple

# third party imports
import typer

# local imports
from strec.calc import select_regions
from strec.utils import render_row

app = typer.Typer(rich_markup_mode="rich")


class FormatType(str, Enum):
    pretty = "pretty"
    csv = "csv"
    excel = "excel"
    json = "json"


@app.command()
def main(
    eqinfo: Tuple[float, float, float] = typer.Option(
        (None, None, None),
        "--eqinfo",
        "-e",
        help=("Calculate region based on lat, lon, depth of earthquake"),
    ),
    event_id: str = typer.Option(
        None,
        "--event-id",
        "-d",
        help=("Calculate region based on ComCat event id (i.e., us6000iasi)."),
    ),
    input_file: str = typer.Option(
        None,
        "--input-file",
        "-i",
        help="Calculate region for events specified in input file.",
    ),
    hypo_columns: Tuple[str, str, str] = typer.Option(
        (None, None, None),
        "--hypo_columns",
        "-c",
        help=(
            (
                "When used with -i/--input-file, specify the columns "
                "that should be used for Latitude, Longitude, Depth."
            )
        ),
    ),
    id_column: str = typer.Option(
        None,
        "--id-column",
        help=(
            (
                "When used with -i/--input-file, specify the column "
                "that should be used for ComCatID."
            )
        ),
    ),
    format: FormatType = typer.Option(
        FormatType.pretty,
        "--format",
        "-f",
        help="Specify output format for results.",
    ),
    output_file: str = typer.Option(
        None,
        "--output-file",
        "-o",
        help="Specify output filename for results (see --format).",
    ),
    moment_info: Tuple[float, float, float, float] = typer.Option(
        (None, None, None, None),
        "--moment-info",
        "-m",
        help="Specify strike, dip, rake and magnitude for single earthquake.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Print out more verbose output.",
    ),
):
    """Determine various seismo-tectonic parameters for given input coordinates.

    The output will consist of the following data fields:

     - TectonicRegion : (Active, Stable, HotSpot, Subduction)
     - FocalMechanism : (RS [Reverse],SS [Strike-Slip], NM [Normal], ALL)
     - TensorType : composite
     - TensorSource : (composite, one of many moment tensor sources like GCMT)
     - KaganAngle : Angle between fault plane and slab orientation.
     - CompositeVariability :  A measure of the uncertainty in the composite
                               moment tensor.
     - NComposite : Number of events used to create composite moment tensor.
     - DistanceToStable : Distance in km from the nearest stable polygon.
     - DistanceToActive : Distance in km from the nearest active polygon.
     - DistanceToSubduction : Distance in km from the nearest subduction
                              polygon.
     - DistanceToHotSpot : Distance in km from the nearest hot spot polygon.
     - Oceanic : Boolean indicating whether we are in an oceanic region,
                 false indicates Continental.
     - DistanceToOceanic : Distance in km to nearest oceanic polygon.
     - DistanceToContinental : Distance in km to nearest continental polygon.
     - SlabModelRegion : Subduction region.
     - SlabModelDepth : Depth of slab2.0 grid at earthquake location.
     - SlabModelDepthUncertainty : Uncertainty of depth to slab.
     - SlabModelDip : Dip of slab at earthquake location.
     - SlabModelStrike : Strike of slab at earthquake location.
     - SlabModelMaximumDepth : Maximum depth of seismogenic zone.
     - NGACategory: Subduction category, one of ["interface", "slab", "crustal",
                    "outer rise", "undetermined", "crustal uncertain",
                    "interface uncertain", "slab uncertain", "outer rise uncertain"]

    where:
        - Active regions are boundaries between two plates that are colliding,
          sliding past each other, or pulling apart.
        - Stable regions are regions where those things are not happening.
        - Subduction regions are those that are above the Slab2.0 grids.
        - HotSpot regions are those that sit above mantle plumes
        - ALL FocalMechanisms that are some combination of the other types


    Input files can be CSV or Excel format (regcalc will
    attempt to determine format automatically) and MUST include columns
    beginning with (case insensitive):

        Lat - Numeric latitude of input earthquake.
        Lon - Numeric longitude of input earthquake.
        Depth - Numeric depth of earthquake (km).

    Input files may optionally contain a column (also case insensitive) called:
    ComCatID - Valid ANSS ComCat ID
    Any other columns present in the input will be copied to the output.

    The output format must be one of the following:

        pretty - A human readable pretty-printed representation of the output.
        json - A JSON representation of the output
        csv - A CSV output, one earthquake per line.
        excel - Microsoft Excel format, one earthquake per line.

    Note that the -c/--columns option will override these defaults.
    """
    # error out on any invalid combinations of options
    if format in ["pretty", "json"] and output_file is not None:
        print(f"Output file is invalid when specified with format of {format}")
        sys.exit(1)

    if format in ["excel"] and output_file is None:
        print("Output format 'excel' is invalid unless an output file is specified")
        sys.exit(1)

    has_eq = int(eqinfo[0] is not None)
    has_id = int(event_id is not None)
    has_file = int(input_file is not None)
    if sum([has_eq, has_id, has_file]) > 1:
        print(
            "Options --eqinfo, --event-id, --input-file are "
            "mutually exclusive. Please choose one."
        )
        sys.exit(1)

    if (hypo_columns[0] is not None or id_column is not None) and input_file is None:
        print(
            "Options --hypo-columns and --id-column only work "
            "when input_file is specified."
        )
        sys.exit(1)

    if moment_info[0] is not None and input_file is not None:
        print("You can only specify moment information for a single earthquake.")
        sys.exit(1)

    regions_frame = select_regions(
        input_file,
        eqinfo,
        moment_info,
        event_id,
        hypo_columns,
        id_column,
        verbose,
    )
    if output_file is None:
        for idx, row in regions_frame.iterrows():
            render_row(row, format, hypo_columns)

    if output_file:
        if format == "csv":
            regions_frame.to_csv(output_file, index=False)
        else:
            regions_frame.to_excel(output_file, index=False)


if __name__ == "__main__":
    app()
