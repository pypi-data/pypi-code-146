import os
from typing import Dict, List

from convoc.files.properties import AttributeFile, Dirs, File, UserCSV
from convoc.files.validate import islevel_validator
from convoc.tools import exception as ex
from convoc.tools import log

logger = log.get_logger(__name__)


def csv2dir(
    csvfile: str,
    level: int,
    root_dir: str,
    *,
    isheader: bool = False,
    attribute_type: str = "json",
) -> List[Dict[str, str]]:
    """Parse the hierarchy defined in CSV and create a directory

    Converts hierarchical information from csv to a directory according to the specified level and converts it to a file with attribute information.

    Args:
        csvfile (str): A CSV filename(filepath)
        level (int): Level of directory to be created.
        root_dir (str): Directory path to create a new directory.
        isheader (bool, optional): Flag to determin the presence or absence of csv header.Defaults to False.
        attribute_type (str, optional): Type of attribute file to be stored at the end of the directory. Defaults to "json".

    Raises:
        ex.InvalidArgumrntType: If the argument type is incorrect, an exception is raised.
        ex.NotSupportedMode: If the attribute data is of a type that is not supported, an exception is raised.

    Returns:
        List[Dict[str,str]]: contents of read csv

    Exsample:
        A read file: "csv/sample.csv"
        usage :
          csv2dir(
              csvfile="csv/sample.csv",
              level=2,
              root_dir="target",
              is_header=True
           )
        return :
            [ {'header1': '1', 'header2': '2', 'header3': '3', 'header4': 'word1'},
              {'header1': '1', 'header2': '1.1', 'header3': '1.1.1', 'header4': 'Au'},]

        Note:
            When this function is executed, folders are created according to the specified level.
            In the above example, level=2,

            target/
              |-- 1/
              |   |-- 1/
              |       |--- attribute.json
              |-- 1/
                  |-- 1.1
                      |--- attribute.json
    """

    if not islevel_validator(level):
        raise ex.InvalidArgumrntType("Invalid DataType of Argument! --> level")

    usr_csv = UserCSV(root_dir)
    usr_csv.read(csvfile, is_header=isheader)

    for line in usr_csv.get_readline():
        components = [root_dir] + list(line.values())[:level]
        file = File(path=os.path.join(*components))
        attr = AttributeFile(file=file, data=line)
        Dirs.make_target_dir(attr.file.path)
        if attribute_type == "json":
            attr.to_json()
        elif attribute_type == "toml":
            attr.to_toml()
        elif attribute_type == "yaml":
            attr.to_yaml()
        elif attribute_type == "csv":
            attr.to_csv()
        elif attribute_type == "txt":
            attr.to_text()
        else:
            raise ex.NotSupportedMode(
                "Unsupported attribute type. Choose from json/toml/yaml/csv/txt."
            )

    return usr_csv.data
