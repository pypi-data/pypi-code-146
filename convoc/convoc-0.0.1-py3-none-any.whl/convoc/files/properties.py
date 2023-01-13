import csv
import glob
import json
import os
import re
from collections import UserDict, UserList
from typing import Any, Dict, Generator, List, Optional, Union

import toml
import yaml
from pydantic import BaseModel, Field, dataclasses, validator

from convoc.tools import exception, log

logger = log.get_logger(__name__)


@dataclasses.dataclass
class File:

    path: str

    @validator("path", always=True)
    def restruct_path(cls, v):
        if isinstance(v, str):
            return re.sub(r"[\s, \u3000, \t]", "_", v)
        else:
            raise FileNotFoundError("file path is invalid.")

    @property
    def suffix(self) -> str:
        _, ext = os.path.splitext(self.path)
        return str(ext)

    @property
    def name(self) -> str:
        base = os.path.basename(self.path)
        return str(base)

    @property
    def parents(self) -> str:
        parent, _ = os.path.splitext(self.path)
        return os.path.dirname(parent)

    @property
    def depth(self) -> int:
        return len(self.parents.split(os.path.sep))


@dataclasses.dataclass
class AttributeFile:

    file: File
    data: Dict[str, Any] = Field(default_factory=dict)
    name: str = "attribute"

    def read_json(self) -> Dict[Any, Any]:
        try:
            with open(self.file.path, mode="r", encoding="utf-8") as f:
                contents = json.load(f)
        except json.JSONDecodeError as e:
            logger.debug(e)
            contents = {}
        self.data.update(contents)
        return contents

    def to_json(self, *, output_path: Optional[str] = None):
        if not output_path:
            output_path = os.path.join(self.file.path, self.name + ".json")
        with open(output_path, mode="w", encoding="utf-8") as fp:
            json.dump(self.data, fp, indent=4, ensure_ascii=False)
        return json.dumps(self.data, indent=4, ensure_ascii=False)

    def read_toml(self) -> Dict[Any, Any]:
        try:
            with open(self.file.path, mode="r", encoding="utf-8") as f:
                contents = toml.load(f)
        except Exception as e:
            logger.debug(e)
            contents = {}
        self.data.update(contents)
        return contents

    def to_toml(self, *, output_path: Optional[str] = None):
        if not output_path:
            output_path = os.path.join(self.file.path, self.name + ".toml")
        with open(output_path, mode="w", encoding="utf-8") as fp:
            toml.dump(self.data, fp)
        return toml.dumps(self.data)

    def read_yaml(self):
        try:
            with open(self.file.path, mode="r", encoding="utf-8") as f:
                contents = yaml.safe_load(f)
        except Exception as e:
            logger.debug(e)
            contents = {}
        self.data.update(contents)
        return contents

    def to_yaml(self, *, output_path: Optional[str] = None):
        if not output_path:
            output_path = os.path.join(self.file.path, self.name + ".yaml")
        with open(output_path, mode="w", encoding="utf-8") as fp:
            yaml.safe_dump(
                self.data, fp, indent=4, encoding="utf-8", allow_unicode=True
            )
        return yaml.dump(self.data, indent=4, encoding="utf-8", allow_unicode=True)

    def read_text(self, *, demiliter: str = ",") -> Dict[Any, Any]:
        contents: Dict[Any, Any] = {}
        try:
            with open(self.file.path, mode="r", encoding="utf-8") as f:
                for line in f.readlines():
                    data = line.split(demiliter)
                    contents[data[0]] = data[1:]
        except Exception as e:
            logger.debug(e)
            contents = {}
        self.data.update(contents)
        return contents

    def to_text(self, *, output_path: Optional[str] = None, demiliter: str = ","):
        if not output_path:
            output_path = os.path.join(self.file.path, self.name + ".txt")
        try:
            fp = open(output_path, mode="w", encoding="utf-8")
            for key, value in self.data.items():
                fp.write(f"{key}{demiliter}{value}\n")
        except Exception as e:
            logger.debug("write error")
            fp.close()
        return self.data

    def read_csv(self) -> List[Dict[Any, Any]]:
        try:
            with open(self.file.path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                contents = [row for row in reader]
        except Exception as e:
            logger.debug(e)
            contents = []
        return contents

    def to_csv(
        self, *, header: Optional[List[str]] = None, output_path: Optional[str] = None
    ):
        if not output_path:
            output_path = os.path.join(self.file.path, self.name + ".csv")
        if not header:
            header = list(self.data.keys())
        with open(output_path, mode="w", encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=header)
            writer.writeheader()
            writer.writerow(self.data)
        return self.data


class AttributeMap(UserDict):
    def __getitem__(self, key):
        if key not in self:
            self[key] = AttributeMap()
        return super().__getitem__(key)


class UserCSV(UserList):
    """CSV file used by user

    Object csv for user use
    Can also be read out in a form that includes header information

    Attributes:
        root_dir: Directory path where csv is stored
        head: csv header information

    About Data:
        Data is held as follows...
        self.data = {
            (header itme1): { Attribute Value1 },
            (header itme2): { Attribute Value2 },...
        }

    Exsample:
        <csv>
            L1: 1,2,3,4,5,6,7
            L2: 1,2,3,word1,word2,word3,word4
        <result>
            Result of reading sample.csv using self.read()->
            self.data = [
                {'1': '1', '2': '2', '3': '3', '4': 'word1', '5': 'word2', '6': 'word3', '7': 'word4'},...
            ]
    """

    def __init__(self, root_dir: str):
        super().__init__()
        self.root_dir = root_dir
        self.head: List[str] = []

    def read(self, path: str, *, is_header: bool = False) -> "UserCSV":
        file = File(path=path)
        with open(file.path, mode="r", encoding="utf-8") as f:
            csv_reader = csv.reader(f)
            if is_header:
                self.head = next(csv_reader)
            else:
                self.head = [str(i + 1) for i in range(len(next(csv_reader)))]
                f.seek(0)
            for item in csv_reader:
                self.data.append({key: val for key, val in zip(self.head, item)})
        return self

    def get_header(self) -> List[str]:
        return self.head

    def header(self, item: List[str]) -> List[str]:
        self.head = item
        return self.head

    def get_readline(self) -> Generator[Dict[str, Any], None, None]:
        for item in self.data:
            yield item

    def additem(self, item: Union[str, int, list]) -> "UserCSV":
        if isinstance(item, (str, int, list)):
            self.data.append(item)
        else:
            raise exception.NotSupportedType(
                "Unsupported data type.Select: str, int, list"
            )
        return self

    def write(self, output: str) -> "UserCSV":
        with open(output, mode="w", encoding="utf-8") as f:
            writer = csv.writer(f)
            if self.head:
                writer.writerow(self.head)
            writer.writerows(self.data)
        return self


class Dirs:

    depth: int = 0

    def __init__(self, target_dir: str):
        self.root_dir = target_dir

    @classmethod
    def scan_auto_depth(cls, target_path: str) -> int:
        if not os.path.exists(target_path):
            error_text = f"File Not Found: {target_path}"
            logger.debug(error_text)
            return 0
        for root, _, _ in os.walk(target_path, topdown=True):
            current_depth = len(root.split(os.sep))
            if cls.depth < current_depth:
                cls.depth = current_depth

        return cls.depth

    @classmethod
    def make_target_dir(
        cls, target_path: Union[str, List[str]], *, parent: Optional[str] = None
    ) -> Optional[str]:
        """Function to generate the desired directory.
        If the target path contains unnecessary whitespae, it is removed.

        Args:
            target_pathlist (List[str]): Dataset of directory path to be created.If empty, it will not be generated.
            parent (str): Parent directory of the direcotry to be generated.

        Returns:
            Optional[pathlib.Path]: If the direcotry was successfully created, the filepath is returened
                                    if not, None is returned.

        Exsample:
            rtn = make_target_dir(['deep1', 'deep2'], "target")
            print(rtn)
            # >> "target/deep1/deep2"
        """
        if parent is None:
            parent = ""

        if isinstance(target_path, str):
            target_path = [target_path]

        target_path = [re.sub(r"[\s, \u3000, \t]", "_", path) for path in target_path]
        extract_dirpath = os.path.join(parent, os.path.join(*target_path))
        try:
            os.makedirs(extract_dirpath, exist_ok=True)
        except Exception as e:
            logger.debug(e)
            return None
        return extract_dirpath

    @classmethod
    def search_attribute(
        cls, dir_path: str, depth: int
    ) -> Generator["AttributeFile", None, None]:
        """Search for attribute files in the target directory

        Recursively traverses the target directory and returns the path to the attritbute file.

        Args:
            dir_path (str): Directory path to search
            depth (str): Depth of hierarchy to be searched

        Yields:
            AttributeFile : attribute file object
        """
        files = glob.glob(dir_path, recursive=True)
        for f in files:
            fobj = File(path=f)
            if fobj.depth <= depth:
                yield AttributeFile(file=fobj)
