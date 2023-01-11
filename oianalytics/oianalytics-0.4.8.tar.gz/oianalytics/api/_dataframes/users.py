from typing import Optional

import pandas as pd

from .. import _credentials
from .. import endpoints
from .. import utils

__all__ = ["get_users"]


def get_users(
    page: int = 0,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    expand_profile: bool = True,
    extract_from_access_list: Optional[str] = "synthesis",
    expand_access_list: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get configured users from the OIAnalytics API

    Parameters
    ----------
    page: int, optional
        Page number to retrieve. If None, the first page will be retrieved.
        The argument is ignored if 'get_all_pages' is True.
    get_all_pages: bool, default True
        If True, paging is ignored and all elements are retrieved.
    multithread_pages: bool, default False
        Only used when getting all pages. If True, pages are retrieved in multiple threads simultaneously.
    expand_profile: bool, default True
        Whether or not the profile information should be expanded into multiple columns.
    extract_from_access_list: {'all_access', 'tag_list', None}, default 'synthesis'
        What field should be extracted from access list information.
        'tag_list' will only extract the listed accessible tag keys.
        'all_access' will only extract whether or not the user has access to evefything.
        'synthesis' will combine the previous 2 extracting a list of accessible tag keys or 'All' for a full access.
        If None, the full dictionary is kept.
    expand_access_list: bool, default True
        Whether or not the access list information should be expanded into multiple columns.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A DataFrame listing users and their access information
    """

    # Args validation
    if extract_from_access_list not in ["all_access", "tag_list", "synthesis", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_access_list': {extract_from_access_list}"
        )

    if extract_from_access_list is None and expand_access_list is True:
        raise ValueError(
            "Access list cannot be expanded if 'extract_from_access_list' is None"
        )

    # Init
    if get_all_pages is True:
        page = 0

    def get_page(page_num: int):
        page_response = endpoints.users.get_users(
            page=page_num, api_credentials=api_credentials
        )
        return page_response

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])
        page_df["expirationDate"] = pd.to_datetime(page_df["expirationDate"])
        if expand_profile is True:
            page_df = utils.expand_dataframe_column(page_df, "profile")

        # Format acess list
        if extract_from_access_list == "tag_list":
            page_df["accessList"] = page_df["accessList"].apply(
                lambda al: {a["tagKey"]: a["accessibleTagValues"] for a in al}
            )
        elif extract_from_access_list == "all_access":
            page_df["accessList"] = page_df["accessList"].apply(
                lambda al: {a["tagKey"]: a["allTagValuesAccessible"] for a in al}
            )
        elif extract_from_access_list == "synthesis":
            page_df["accessList"] = page_df["accessList"].apply(
                lambda al: {
                    a["tagKey"]: "All"
                    if a["allTagValuesAccessible"] is True
                    else a["accessibleTagValues"]
                    for a in al
                }
            )

        if expand_access_list is True and extract_from_access_list is not None:
            page_df = utils.expand_dataframe_column(
                page_df, "accessList", add_prefix=False
            )

        page_df.set_index("id", inplace=True)
        return page_df

    # Query endpoint
    df = utils.concat_pages_to_dataframe(
        getter=get_page,
        parser=parse_page,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )

    # Output
    return df
