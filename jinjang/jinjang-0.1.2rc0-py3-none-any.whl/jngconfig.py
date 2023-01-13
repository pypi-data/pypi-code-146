#!/usr/bin/env python3

###
# This module manages the ¨configs of the user.
###


from typing import Union

from pathlib import Path
from yaml    import safe_load as yaml_load


# ---------------------- #
# -- SPECIFIC CONFIGS -- #
# ---------------------- #

AUTO_CONFIG = ":auto-config:"
NO_CONFIG   = ":no-config:"

DEFAULT_CONFIG_FILE = "cfg.jng.yaml"


TAG_HOOKS = 'hooks'
TAG_PRE   = 'pre'
TAG_POST  = 'post'


###
# prototype::
#     config : ¨configs used to allow extra features.
#              ``NO_CONFIG`` prohibits the use of a configuration file.
#              ``AUTO_CONFIG`` requires the use of a file named
#              ``DEFAULT_CONFIG_FILE`` in the template directory.
#              In other cases, the value will be interpreted as a path
#              to a path::``YAML`` file to be used for configurations.
#            @ config in [AUTO_CONFIG, NO_CONFIG]
#              or
#              exists path(config)
#     parent : the parent directory of the template which is the folder
#              where to look for the default ¨config file.
#              This parameter is ignored if ``config = AUTO_CONFIG``
#
#     :return: a ¨python ¨dict of the ¨configs that is ready-to-use
###
def build_config(
    config: str,
    parent: Union[Path, None] = None
) -> dict:
# No config used.
    if config == NO_CONFIG:
        return dict()

# Default name for the config file?
    if config == AUTO_CONFIG:
        if parent is None:
            raise ValueError(
                 "Missing parent directory for the default config file."
            )

        config = parent / DEFAULT_CONFIG_FILE

# User's config file.
    else:
        config = Path(config)

        if config.suffix != '.yaml':
            raise ValueError(
                 "The config file is not a YAML one. See:\n"
                f"  + {config}"
            )

# One YAML direct conversion.
    with config.open(
        encoding = 'utf-8',
        mode     = "r",
    ) as f:
        dictfound = yaml_load(f)

# Default values.
    if TAG_HOOKS not in dictfound:
        dictfound[TAG_HOOKS] = {}

    for tag in [TAG_POST, TAG_PRE]:
        if tag not in dictfound[TAG_HOOKS]:
            dictfound[TAG_HOOKS][tag] = []

# The dict has been normalized.
    return dictfound
