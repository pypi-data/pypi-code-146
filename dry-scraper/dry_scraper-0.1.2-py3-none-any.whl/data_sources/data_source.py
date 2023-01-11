import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

import pandas

from dry_scraper.config import config


# noinspection PyUnresolvedReferences
@dataclass(init=False, repr=False, eq=False, order=False, unsafe_hash=False, frozen=False)
class DataSource(ABC):
    """
    Abstract class that represents an online data source.

    ...

    Attributes
    ----------
    desc : str
        brief description of fetcher class for CLI use
    name : str
        identifying name for the CLI
    content : str
        string representation of raw data retrieved by fetch_content() or load_content()
    content_json : dict
        dict representation of raw content parsed by parse_to_json()
    content_csv :
        string representation of content parsed into csv format
    local_path : str
        full path to storage location for file representation of data
    local_path_stub : str
        partial path to storage location. set in config. static for each subclass
    url : str
        fully qualified URL location of data source, completed on instantiation
    url_stub : str
        partial URL location of data source. static for each subclass
    extension : str
        file extension to be used when writing the raw data source to disk e.g. json, HTM
    integrity : dict
        dict containing information about the completeness and integrity of retrieved data
        as determined by validate_content()

    Methods
    -------
    @abstractmethod
    validate_content():
        validate self.content fetched and record result in self.integrity
    @abstractmethod
    fetch_content():
        fetch content from self.url and store response in self.content
    @abstractmethod
    parse_to_json():
        Parse content into dict/json form and store result in self.content_json
    @abstractmethod
    parse_to_csv():
        Parse content into pandas dataframe and store result in self.content_csv
    load_content():
        load source file designated by self.local_path, if it exists, and store
        contents in self.content
    write_content():
        write self.content to local directory specified by self.local_path
    """
    desc: str = field(init=False, default_factory=str)
    name: str = field(init=False, default_factory=str)
    content: str = field(init=False, default_factory=str)
    content_json: dict = field(init=False, default_factory=dict)
    content_csv: pandas.DataFrame = field(init=False, default_factory=pandas.DataFrame)
    local_path_stub: ClassVar[str] = config['DEFAULT']['FetchPath']
    local_path: str = field(init=False, default_factory=str)
    url: str = field(init=False, default_factory=str)
    url_stub: str = field(init=False, default_factory=str)
    extension: str = field(init=False, default_factory=str)
    integrity: dict = field(init=False, default_factory=dict)

    @abstractmethod
    def validate_content(self):
        """Validate self.content fetched and record result in self.integrity"""

    @abstractmethod
    def fetch_content(self):
        """Fetch content from self.url and store response in self.content"""

    @abstractmethod
    def parse_to_json(self):
        """Parse content into dict/json form and store result in self.content_json"""

    @abstractmethod
    def parse_to_csv(self):
        """Parse content into a pandas dataframe and store result in self.content_csv"""

    def load_content(self):
        """Load source file designated by self.local_path, if it exists
           and store contents in self.content"""
        full_path = f'{self.local_path}.{self.extension}'
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r') as f:
                    self.content = f.read()
            except OSError as e:
                print(f'Failed to read {full_path}.')
                print(e)
            except Exception as e:
                print(e)
        else:
            self.content = ''
        return self

    def write_raw_content(self):
        """Write self.content to local directory specified by self.local_path with
           extension specified by self.extension"""
        full_path = f'{self.local_path}.{self.extension}'
        try:
            with open(full_path, 'w') as f:
                f.write(self.content)
        except OSError as e:
            print(f'Failed to write to {full_path}.')
            print(e)
        except Exception as e:
            print(e)
        return self

    def write_json_content(self):
        """Write self.content_json to local directory specified by self.local_path"""
        full_path = f'{self.local_path}.json'
        try:
            with open(full_path, 'w') as f:
                json.dump(self.content_json, f)
        except OSError as e:
            print(f'Failed to write to {full_path}.')
            print(e)
        except Exception as e:
            print(e)
        return self

    def write_csv_content(self):
        """Write self.content_csv to local directory specified by self.local_path"""
        full_path = f'{self.local_path}.csv'
        try:
            with open(full_path, 'w') as f:
                self.content_csv.to_csv(f, index=False)
        except OSError as e:
            print(f'Failed to write to {full_path}.')
            print(e)
        except Exception as e:
            print(e)
        return self
