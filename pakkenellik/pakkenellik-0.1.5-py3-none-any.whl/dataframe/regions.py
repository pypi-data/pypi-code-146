from typing import Optional

import pandas as pd


def add_municipality_name(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame, municipality_col: Optional[str] = "municipality"
) -> pd.DataFrame:
    """
    Utility function to add the municipality name to a dataframe

    Args:
        _df (dataframe): the dataframe to add the municipality name to
        municipality_col (str, optional): The municipality column.
        Defaults to "municipality".

    Returns:
        dataframe: the dataframe with the municipality name added
    """
    df_muni = pd.read_csv(
        "https://raw.githubusercontent.com/BergensTidende/bord4-data/master/data/csv/norwegian_regions.csv"  # noqa: E501
    )
    df_muni["municipality_id"] = df_muni["municipality_id"].astype(str)

    _df[municipality_col] = _df[municipality_col].astype(str)
    _df = _df.merge(
        df_muni[["municipality_id", "municipality"]],
        left_on=municipality_col,
        right_on="municipality_id",
        how="left",
    )

    return _df


def add_county_name(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame, county_col: Optional[str] = "county"
) -> pd.DataFrame:
    """
    Utility function to add the county name to a dataframe

    Args:
        _df (dataframe): the dataframe to add the county name to
        county_col (str, optional): The county column. Defaults to "county".

    Returns:
        dataframe: the dataframe with the county name added
    """
    df_county = pd.read_csv(
        "https://raw.githubusercontent.com/BergensTidende/bord4-data/master/data/csv/norwegian_regions.csv"  # noqa: E501
    )
    df_county["county_id"] = df_county["county_id"].astype(str)

    _df[county_col] = _df[county_col].astype(str)
    _df = _df.merge(
        df_county[["county_id", "county"]],
        left_on=county_col,
        right_on="county_id",
        how="left",
    )

    return _df
