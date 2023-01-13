from .sharepoint import SharePoint
from ..df_processor import DFProcessor
from ..abs_source import AbsSource
from shareplum import Site
from ...tools import URLTools
import re
import pandas as pd
from typing import Optional, List, Dict, Any, Union


# SharepointLink(): Stores a url link data from Sharepoint
class SharepointLink():
    def __init__(self, display_name: str, url: str):
        self.display_name = display_name
        self.url = url


# SharePointSource: Source taken from a SharePoint List
class SharepointSource(AbsSource):
    def __init__(self, sharepoint: SharePoint, site: str, list: str, view: str, include_urls: bool = False, post_processor: Optional[Union[Dict[str, DFProcessor], DFProcessor]] = None):
        super().__init__(post_processor)
        self.__sharepoint = sharepoint
        self.__site = site
        self.__list = list
        self.__view = view
        self.__include_urls = include_urls


    # clean_sp_data(cell): Cleans up the data for each cell in the raw Sharepoint
    #   data
    def clean_sp_data(self, cell: Any) -> Any:
        result = cell

        if (isinstance(cell, str)):
            # store link information
            if (URLTools.is_https_link(cell)):
                space_pos = cell.find(" ")

                result = cell[space_pos + 1:]

                if (self.__include_urls):
                    result = SharepointLink(result, cell[:space_pos])

            # store the source data
            else:
                data_seperator = ';#'
                data_seperator_match = re.search(data_seperator, cell)

                if (data_seperator_match is not None):
                    result = cell[data_seperator_match.end():]
        return result


    # clean_dataframe(): Cleans up the raw data in Sharepoint
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.applymap(lambda cell: self.clean_sp_data(cell))


    # import_data(): Imports the sharepoint list
    async def import_data(self) -> pd.DataFrame:
        site = Site(self.__site, authcookie=self.__sharepoint.auth_cookie)
        data = site.List(self.__list).GetListItems(self.__view)

        # clean the sharepoint data to retrieve the needed data
        data_frame = pd.DataFrame(data)
        data_frame = self.clean_dataframe(data_frame)
        return data_frame
