from Shared.certoraUtils import Mode, get_last_confs_directory
import json
from datetime import datetime
from copy import deepcopy
from typing import Dict, Any
import logging
from pathlib import Path
import EVMVerifier.certoraContext as Ctx
from EVMVerifier.certoraContextClass import CertoraContext

"""
This file is responsible for reading and writing configuration files.
"""

# logger for issues regarding the general run flow.
# Also serves as the default logger for errors originating from unexpected places.
run_logger = logging.getLogger("run")


def current_conf_to_file(parsed_options: CertoraContext) -> Dict[str, Any]:
    """
    Saves current command line options to a configuration file
    @param parsed_options: command line options after parsing
    @:return the data that was written to the file (in json/dictionary form)
    """
    json_rep = deepcopy(parsed_options.__dict__)

    """
    We are not saving options if they were not provided (and have a simple default that cannot change between runs).
    Why?
    1. The .conf file is shorter
    2. The .conf file is much easier to read, easy to find relevant arguments when debugging
    3. Reading the .conf file is quicker
    4. Parsing the .conf file is simpler, as we can ignore the null case
    """
    keys_to_delete = ['mode']  # Unnecessary at this point - we were in CONFIG mode
    for (option, value) in json_rep.items():
        if value is None or value is False:
            keys_to_delete.append(option)
    for key in keys_to_delete:
        del json_rep[key]

    parsed_options.conf_file = f"last_conf_{datetime.now().strftime('%d_%m_%Y__%H_%M_%S')}.conf"
    out_file_path = get_last_confs_directory() / parsed_options.conf_file
    run_logger.debug(f"Saving last configuration file to {out_file_path}")
    Ctx.write_output_conf_to_path(json_rep, out_file_path)
    return json_rep


def read_from_conf_file(context: CertoraContext) -> None:
    """
    Reads data from the configuration file given in the command line and adds each key to the context namespace if the
    key is undefined there. For more details, see the invoked method read_from_conf.
    @param context: A namespace containing options from the command line, if any (context.files[0] should always be a
        .conf file when we call this method)
    """
    assert context.mode == Mode.CONF, "read_from_conf_file() should only be invoked in CONF mode"

    conf_file_name = Path(context.files[0])
    assert conf_file_name.suffix == ".conf", f"conf file must be of type .conf, instead got {conf_file_name}"

    with conf_file_name.open() as conf_file:
        configuration = json.load(conf_file)
        read_from_conf(configuration, context)


# features: read from conf. write last to last_conf and to conf_date.
def read_from_conf(configuration: Dict[str, Any], context: CertoraContext) -> None:
    """
    Reads data from the input dictionary [configuration] and adds each key to context if the key is
    undefined there.
    Note: a command line definition trumps the definition in the file.
    If in the .conf file solc is 4.25 and in the command line --solc solc6.10 was given, sol6.10 will be used
    @param configuration: A json object in the conf file format
    @param context: A namespace containing options from the command line, if any
    """
    for option in configuration:
        if hasattr(context, option):
            val = getattr(context, option)
            if val is None or val is False:
                setattr(context, option, configuration[option])

    assert 'files' in configuration, "configuration file corrupted: key 'files' must exist at configuration"
    context.files = configuration['files']  # Override the current .conf file
