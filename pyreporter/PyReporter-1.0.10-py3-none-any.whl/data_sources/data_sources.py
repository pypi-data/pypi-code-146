import pandas as pd
from .source_manager import SourceManager


# DataSources: All data sources used for a report
class DataSources():
    """
    A class to store and handle many different data sources

    .. container:: operations

        **Supported Operations:**

        .. describe:: data_sources[key] = value

            sets ``value`` as the new :class:`~Reporter.data_sources.source_manager.SourceManager` for the key name, ``key``

            **key**: :class:`str`

                The name of the source

            **value**: :class:`~Reporter.data_sources.source_manager.SourceManager`

                The corresponding :class:`~Reporter.data_sources.source_manager.SourceManager` for the source key name

        .. describe:: result = data_sources[key]

            Returns the corresponding :class:`~Reporter.data_sources.source_manager.SourceManager` to ``result``, based off the name, ``key``

            **key**: :class:`str`

                The name of the source

    """
    def __init__(self):
        self.sources = {}


    def __getitem__(self, key: str):
        return self.sources[key]


    def __setitem__(self, key: str, value: SourceManager):
        assert isinstance(value, SourceManager)
        self.sources[key] = value
