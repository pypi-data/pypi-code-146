import os
from typing import Any, List, Optional

from convoc.files.properties import Dirs, UserCSV
from convoc.tools import exception as ex
from convoc.tools import log

logger = log.get_logger(__name__)


def dir2csv(
    root_dir: str,
    output: str,
    *,
    level: Optional[int] = None,
    attribute_type: str = "json",
) -> List[Any]:
    """Convert directories and csv to each other

    Export directory structure and attribute files in the specified hierarchy to csv.
    The attribute file type corresponds to json/yaml/toml/csv/text.
    Hierarchy (argument level) is optimized to the deepest hierarchical level unless specified otherwise.

    Args:
        root_dir (str): root directory path to be read
        output (str): destination path for csv files
        level (Optional[int], optional): number of hierarchies of read directories. Defaults to None.
        attribute_type (str, optional): attribute file type. Defaults to "json".

    Returns:
        List[Any]: Return directories in a list structure
    """
    if level is None:
        level = Dirs.scan_auto_depth(root_dir)

    user_csv = UserCSV(root_dir)
    search_path = os.path.join(root_dir, "**/*." + attribute_type)
    for attr in Dirs.search_attribute(search_path, level):
        if attr.file.name == "":
            continue

        if attribute_type == "json":
            attr.read_json()
        elif attribute_type == "yaml":
            attr.read_yaml()
        elif attribute_type == "toml":
            attr.read_toml()
        elif attribute_type == "txt":
            attr.read_text()
        elif attribute_type == "csv":
            attr.read_csv()
        else:
            ex.NotSupportedMode(
                "Unsupported attribute type. Choose from json/toml/yaml/csv/txt."
            )

        user_csv.header(list(attr.data.keys()))
        user_csv.additem(list(attr.data.values()))

    if not os.path.exists(os.path.dirname(output)):
        logger.debug(os.path.dirname(output))
        os.makedirs(os.path.dirname(output), exist_ok=True)

    user_csv.write(output)
    return user_csv.data
