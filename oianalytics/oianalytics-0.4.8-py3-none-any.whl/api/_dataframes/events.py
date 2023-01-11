from typing import Optional, Union, List
from datetime import datetime

import pandas as pd

from .. import _credentials
from .. import endpoints
from .. import utils

__all__ = ["get_event_types", "get_events"]


def get_event_types(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    extract_from_tag_keys: Optional[str] = "value",
    extract_from_context: Optional[str] = "value",
    expand_context: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get the configured event types from the OIAnalytics API

    Parameters
    ----------
    page: int, optional
        Page number to retrieve. If None, the first page will be retrieved.
        The argument is ignored if 'get_all_pages' is True.
    page_size: int, optional
        The size of each page to retrieve. By default, 20 elements are retrieved.
        The argument is ignored if 'get_all_pages' is True.
    get_all_pages: bool, default True
        If True, paging is ignored and all elements are retrieved.
    multithread_pages: bool, default False
        Only used when getting all pages. If True, pages are retrieved in multiple threads simultaneously.
    extract_from_tag_keys: {'id', 'value', 'dict', None}, default 'value'
        What field should be extracted from tag keys information.
        If 'dict', a dictionary in the form of {id: value} is built. If None, the full dictionary is kept.
    extract_from_context: {'id', 'value', None}, default 'value'
        What field should be extracted from context information. If None, the full dictionary is kept.
    expand_context: bool, default True
        Whether or not the context should be expanded into multiple columns.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A DataFrame listing event types
    """

    # Args validation
    if extract_from_tag_keys not in ["id", "value", "dict", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_tag_keys': {extract_from_tag_keys}"
        )

    if extract_from_context not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_context': {extract_from_context}"
        )

    if expand_context is True and extract_from_context is None:
        raise ValueError("Context cannot be expanded if 'extract_from_context' is None")

    # Init
    if get_all_pages is True:
        page = 0
        page_size = 500

    def get_page(page_num: int):
        page_response = endpoints.events.get_event_types(
            page=page_num, page_size=page_size, api_credentials=api_credentials
        )
        return page_response

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])

        # Expected columns if content is empty
        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(columns=["id", "name", "tagKeys", "tagContext"])

        # Extract from tag keys
        if extract_from_tag_keys == "id":
            page_df["tagKeys"] = page_df["tagKeys"].apply(
                lambda l: [tk["id"] for tk in l]
            )
        elif extract_from_tag_keys == "value":
            page_df["tagKeys"] = page_df["tagKeys"].apply(
                lambda l: [tk["key"] for tk in l]
            )
        elif extract_from_tag_keys == "dict":
            page_df["tagKeys"] = page_df["tagKeys"].apply(
                lambda l: {tk["id"]: tk["key"] for tk in l}
            )

        # Extract from context
        if extract_from_context == "id":
            page_df["tagContext"] = page_df["tagContext"].apply(
                lambda context: {
                    c["tagKey"]["id"]: [atv["id"] for atv in c["accessibleTagValues"]]
                    for c in context
                }
            )
        elif extract_from_context == "value":
            page_df["tagContext"] = page_df["tagContext"].apply(
                lambda context: {
                    c["tagKey"]["key"]: [
                        atv["value"] for atv in c["accessibleTagValues"]
                    ]
                    for c in context
                }
            )

        if expand_context is True and extract_from_context is not None:
            page_df = utils.expand_dataframe_column(
                page_df, "tagContext", add_prefix=False
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


def get_events(
    event_type_id: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    description: Optional[str] = None,
    features_value_ids: Optional[Union[str, List[str]]] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    expand_event_type: bool = True,
    extract_from_features: Optional[str] = "value",
    expand_features: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get event instances from the OIAnalytics API

    Parameters
    ----------
    event_type_id: str
        The id of the event type to be retrieved
    start_date: datetime or str
        The beginning of the period to be retrieved
    end_date: datetime or str
        The end of the period to be retrieved
    description: str, optional
        A string that should be contained by all events description returned
    features_value_ids: str or list of str, optional
        Possibly multiple feature value ids each returned event should match.
        If for a given feature multiple feature value ids are provided than a event will be returned if it
        contains one of them.
    page: int, optional
        Page number to retrieve. If None, the first page will be retrieved.
        The argument is ignored if 'get_all_pages' is True.
    page_size: int, optional
        The size of each page to retrieve. By default, 20 elements are retrieved.
        The argument is ignored if 'get_all_pages' is True.
    get_all_pages: bool, default True
        If True, paging is ignored and all elements are retrieved.
    multithread_pages: bool, default False
        Only used when getting all pages. If True, pages are retrieved in multiple threads simultaneously.
    expand_event_type: bool, default True
        Whether or not the event type information should be expanded into multiple columns.
    extract_from_features: {'id', 'value', None}, default 'value'
        What field should be extracted from features information. If None, the full dictionary is kept.
    expand_features: bool, default True
        Whether or not the features should be expanded into multiple columns.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A DataFrame containing event dates, data and features values
    """

    # Args validation
    if extract_from_features not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_features': {extract_from_features}"
        )

    if expand_features is True and extract_from_features is None:
        raise ValueError(
            "Features cannot be expanded if 'extract_from_features' is None"
        )

    # Init
    if get_all_pages is True:
        page = 0
        page_size = 500

    def get_page(page_num: int):
        page_response = endpoints.events.get_events(
            event_type_id=event_type_id,
            start_date=start_date,
            end_date=end_date,
            description=description,
            features_value_ids=features_value_ids,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )
        return page_response

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])

        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(
                columns=[
                    "eventType",
                    "id",
                    "description",
                    "start",
                    "end",
                    "duration",
                    "values",
                    "features",
                ]
            )

        # Format dataframe
        if expand_event_type is True:
            page_df = utils.expand_dataframe_column(
                page_df, "eventType", expected_keys=["id", "name"]
            )

        if extract_from_features == "id":
            page_df["features"] = page_df["features"].apply(
                lambda fl: {f["tagKey"]["id"]: f["id"] for f in fl}
            )
        elif extract_from_features == "value":
            page_df["features"] = page_df["features"].apply(
                lambda fl: {f["tagKey"]["key"]: f["value"] for f in fl}
            )

        if expand_features is True and extract_from_features is not None:
            page_df = utils.expand_dataframe_column(
                page_df, "features", add_prefix=False
            )

        page_df.set_index("id", inplace=True)

        # Output
        return page_df

    # Query endpoint
    df = utils.concat_pages_to_dataframe(
        getter=get_page,
        parser=parse_page,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )

    # Dates
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])

    # Output
    return df
