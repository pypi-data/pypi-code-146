import pandas as pd
from .df_processor import DFProcessor
from .abs_source import AbsSource
from typing import Union, Optional, List, Dict, Any


# TableSource: Class for creating custom tables
class TableSource(AbsSource):
    """
    This Class inherits from :class:`~Reporter.data_sources.abs_source.AbsSource`

    a data source for creating a custom table from a pandas `DataFrame`_

    Attributes
    ----------
    src: Union[`ndarray`_, Iterable, Dict[Any, Any], `DataFrame`_]
        the data to be transformed into a pandas `DataFrame`_

    post_processor: Optional[:class:`~Reporter.data_sources.df_processor.DFProcessor`]
        the procesor used to transform the imported raw table from the source

        **Default**: ``None``
    """
    def __init__(self, src, post_processor: Optional[Union[Dict[str, DFProcessor], DFProcessor]] = None):
        super().__init__(post_processor)
        self.src = src


    # import_data(): Creates the custom table
    def import_data(self) -> pd.DataFrame:
        """
        Creates the table from a pandas `DataFrame`_

        Returns
        -------
        `DataFrame`_
            The created `DataFrame`_
        """
        return pd.DataFrame(self.src)
