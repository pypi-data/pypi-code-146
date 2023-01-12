from .cli_configs import BootstrapStitchingConfig
from ..pipeline.config import generate_nabu_configfile
from ..stitching.config import get_default_stitching_config, SECTIONS_COMMENTS as _SECTIONS_COMMENTS
from .utils import parse_params_values


def bootstrap_stitching():
    args = parse_params_values(
        BootstrapStitchingConfig,
        parser_description="Initialize a nabu configuration file",
    )

    prefilled_values = {}

    generate_nabu_configfile(
        fname=args["output"],
        default_config=get_default_stitching_config(args["stitching_type"]),
        comments=True,
        sections_comments=_SECTIONS_COMMENTS,
        options_level=args["level"],
        prefilled_values=prefilled_values,
    )
