from nabu.utils import Progress
from .cli_configs import StitchingConfig
from ..pipeline.config import parse_nabu_config_file
from nabu.stitching.z_stitching import z_stitching
from nabu.stitching.config import dict_to_config_obj
from .utils import parse_params_values


def main():
    args = parse_params_values(
        StitchingConfig,
        parser_description="Run stitching from a configuration file. Configuration can be obtain from `stitching-config`",
    )

    conf_dict = parse_nabu_config_file(args["input_file"], allow_no_value=True)

    stitching_config = dict_to_config_obj(conf_dict)

    progress = Progress("z-stitching")
    progress.set_name("initialize z-stitching")
    progress.set_advancement(0)
    z_stitching(stitching_config, progress=progress)
    exit(0)
