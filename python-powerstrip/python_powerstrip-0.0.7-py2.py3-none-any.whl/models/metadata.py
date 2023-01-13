import logging
from pathlib import Path
from typing import Union
from io import TextIOWrapper

import yaml

from powerstrip.cerberusutils.customvalidator import CustomValidator
from powerstrip.cerberusutils.schema import plugin_metadata_schema
from powerstrip.exceptions import MetadataException
from powerstrip.utils.semver import SemVer
from powerstrip.utils.utils import ensure_path


# prepare logger
log = logging.getLogger(__name__)


class Metadata:
    """
    metadata class
    """
    METADATA_FILENAME = "metadata.yml"

    def __init__(self):
        """
        initialize the Metadata class
        """
        self.hash = None
        self.name = None
        self.author = None
        self.description = None
        self.version = None
        self.license = None
        self.category = None
        self.url = None
        self.tags = None

    @property
    def hash(self) -> str:
        """
        returns the plugin hash

        :return: plugin hash
        :rtype: str
        """
        return self._hash or ""

    @hash.setter
    def hash(self, value: str):
        """
        set the plugin hash

        :param value: plugin hash
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._hash = value

    @property
    def name(self) -> str:
        """
        returns the plugin name or empty string, if not set

        :return: plugin name or empty string, if not set
        :rtype: str
        """
        return self._name or ""

    @name.setter
    def name(self, value: str):
        """
        set the plugin name

        :param value: plugin name
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._name = value

    @property
    def description(self) -> str:
        """
        returns the plugin description or empty string, if not set

        :return: plugin description or empty string, if not set
        :rtype: str
        """
        return self._description or ""

    @description.setter
    def description(self, value: str):
        """
        set the plugin description

        :param value: plugin description
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._description = value

    @property
    def author(self) -> str:
        """
        returns the plugin author or empty string, if not set

        :return: plugin author or empty string, if not set
        :rtype: str
        """
        return self._author or ""

    @author.setter
    def author(self, value: str):
        """
        set the plugin author

        :param value: plugin author
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._author = value

    @property
    def license(self) -> str:
        """
        returns the plugin license or empty string, if not set

        :return: plugin license or empty string, if not set
        :rtype: str
        """
        return self._license or ""

    @license.setter
    def license(self, value: str):
        """
        set the plugin license

        :param value: plugin license
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._license = value

    @property
    def version(self) -> SemVer:
        """
        returns the semantic version of the plugin

        :return: semantic version version
        :rtype: SemVer
        """
        return self._version

    @version.setter
    def version(self, value: str):
        """
        set the semantic version of the plugin

        :param value: semantic version string
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        if value in ("", None):
            self._version = SemVer()
        else:
            self._version = SemVer.create_from_str(value)

    @property
    def tags(self) -> list:
        """
        returns the list of tags

        :return: list of tags
        :rtype: list
        """
        return self._tags

    @tags.setter
    def tags(self, value: str) -> None:
        """
        set list of tags by provided comma separated string

        :param value: comma separated string
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        if value in (None, ""):
            # return empty list
            self._tags = []

        else:
            # return list of lower-case tags
            self._tags = [
                s.strip().lower()
                for s in value.split(",")
                if s.strip() != ""
            ]

    @property
    def category(self) -> str:
        """
        returns the plugin category or empty string, if not set

        :return: plugin category or empty string, if not set
        :rtype: str
        """
        return self._category or ""

    @category.setter
    def category(self, value: str):
        """
        set the plugin category or if None, use "default"

        :param value: plugin category or if None, "default"
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._category = value or "default"

    @property
    def url(self) -> str:
        """
        returns the plugin url or empty string, if not set

        :return: plugin url or empty string, if not set
        :rtype: str
        """
        return self._url or ""

    @url.setter
    def url(self, value: str):
        """
        set the plugin url

        :param value: plugin url
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._url = value

    @property
    def plugin_name(self) -> str:
        """
        returns the plugin filename derived from name and version

        :return: plugin name
        :rtype: str
        """
        return f"{self.name}-{self.version}"

    @property
    def dict(self) -> dict:
        """
        returns metadata representation as dictionary

        :return: dictionary of metadata
        :rtype: dict
        """
        return {
            "name": self.name,
            "author": self.author,
            "description": self.description,
            "hash": self.hash,
            "license": self.license,
            "version": str(self.version),
            "category": self.category,
            "url" : self.url,
            "tags": ", ".join(self.tags)
        }

    def from_dict(self, d: dict):
        """
        set Metadata properties by given dict

        :param d: metadata values in dictionary
        :type d: dict
        :raises MetadataException: if invalid values in dictionary
        """
        assert isinstance(d, dict)

        # validate given dictionary
        validator = CustomValidator(plugin_metadata_schema)
        if not validator.validate(d):
            # invalid content => raise exception with errors
            raise MetadataException(validator.errors)

        # set internal properties based on dictionary
        for k, v in d.items():
            setattr(self, k, v)

    @staticmethod
    def create_from_dict(d: dict) -> "Metadata":
        """
        create new instance of Metadata based on given dict

        :return: instance of the Metadata
        :rtype: Metadata
        """
        assert isinstance(d, dict)

        md = Metadata()
        md.from_dict(d)

        return md

    @staticmethod
    def create_from_directory(
        plugin_directory: Union[str, Path] = "."
    ) -> "Metadata":
        """
        create an instance of Metadata from given directory

        :param plugin_directory: plugin directory, defaults to "."
        :type plugin_directory: Union[str, Path], optional
        :return: [description]
        :rtype: [type]
        """
        assert isinstance(plugin_directory, (str, Path))

        md = Metadata()

        # ensure that metadata file exists
        filename = md.get_filename(plugin_directory)
        ensure_path(filename, must_exist=True)

        # load content from metadata file
        with filename.open("r") as f:
            md.load(f)

        return md

    @staticmethod
    def create_from_f(f: TextIOWrapper) -> "Metadata":
        """
        create new instance of Metadata based on given file object

        :return: instance of the Metadata
        :rtype: Metadata
        """
        assert isinstance(f, TextIOWrapper)

        md = Metadata()
        md.load(f)

        return md

    def get_filename(self, plugin_directory: Union[str, Path] = ".") -> Path:
        """
        returns metadata filename including the plugin directory

        :param plugin_directory: plugin directory, defaults to "."
        :type plugin_directory: Union[str, Path], optional
        :return: metadata filename
        :rtype: Path
        """
        assert isinstance(plugin_directory, (str, Path))

        # ensure that plugin directory is a Path
        plugin_directory = ensure_path(plugin_directory, must_exist=True)

        return plugin_directory.joinpath(self.METADATA_FILENAME)

    def save(self, f: TextIOWrapper):
        """
        save metadata to given file object

        :param f: file object metadata is written to
        :type f: TextIOWrapper
        """
        assert isinstance(f, TextIOWrapper)

        yaml.safe_dump(self.dict, f, sort_keys=False)

    def save_to_directory(
        self,
        plugin_directory: Union[str, Path] = "."
    ):
        """
        save instance of Metadata to given directory

        :param plugin_directory: plugin directory, defaults to "."
        :type plugin_directory: Union[str, Path], optional
        """
        assert isinstance(plugin_directory, (str, Path))

        with self.get_filename(plugin_directory).open("w") as f:
            self.save(f)

    def load(self, f: TextIOWrapper):
        """
        load YAML from file object, validate the input
        and set internal properties of Metadata class

        :param f: file object to load YAML from
        :type f: TextIOWrapper
        :raises MetadataException: if YAML cannot be parsed
        """
        assert isinstance(f, TextIOWrapper)

        y = yaml.safe_load(f) or {}
        self.from_dict(y)

    def __repr__(self) -> str:
        """
        string representation of the Metadata class

        :return: string representation of the Metadata class
        :rtype: str
        """
        return (
            f"<Metadata(hash='{self.hash}', "
            f"name='{self.name}', "
            f"description='{self.description}', "
            f"author='{self.author}', "
            f"license='{self.license}', "
            f"version='{self.version}', "
            f"category='{self.category}', "
            f"tags='{self.tags}', "
            f"url='{self.url}')>"
        )
