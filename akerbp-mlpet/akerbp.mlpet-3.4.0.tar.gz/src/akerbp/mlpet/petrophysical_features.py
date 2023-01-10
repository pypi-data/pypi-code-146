import warnings
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from cognite.client import CogniteClient

import akerbp.mlpet.utilities as utilities


def guess_BS_from_CALI(
    df: pd.DataFrame,
    standard_BS_values: Optional[List[float]] = None,
) -> pd.DataFrame:
    """
    Guess bitsize from CALI, given the standard bitsizes

    Args:
        df (pd.DataFrame): dataframe to preprocess

    Keyword Args:
        standard_BS_values (ndarray): Numpy array of standardized bitsizes to
            consider. Defaults to::

                np.array([6, 8.5, 9.875, 12.25, 17.5, 26])

    Returns:
        pd.DataFrame: preprocessed dataframe

    """
    if standard_BS_values is None:
        standard_BS_values = [6, 8.5, 9.875, 12.25, 17.5, 26]
    BS_values = np.array(standard_BS_values)
    edges = (BS_values[1:] + BS_values[:-1]) / 2
    edges = np.concatenate([[-np.inf], edges, [np.inf]])
    df.loc[:, "BS"] = pd.cut(df["CALI"], edges, labels=BS_values)
    df = df.astype({"BS": np.float64})
    return df


def calculate_CALI_BS(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates CALI-BS assuming at least CALI is provided in the dataframe
    argument. If BS is not provided, it is estimated using the
    :py:meth:`guess_BS_from_CALI <akerbp.mlpet.feature_engineering.guess_BS_from_CALI>`
    method from this module.

    Args:
        df (pd.DataFrame): The dataframe to which CALI-BS should be added.

    Raises:
        ValueError: Raises an error if neither CALI nor BS are provided

    Returns:
        pd.DataFrame: Returns the dataframe with CALI-BS as a new column
    """
    drop_BS = False
    if "CALI" in df.columns:
        if "BS" not in df.columns:
            drop_BS = True
            df = guess_BS_from_CALI(df)
        df["CALI-BS"] = df["CALI"] - df["BS"]
    else:
        raise ValueError(
            "Not possible to generate CALI-BS. At least CALI needs to be present in the dataset."
        )

    if drop_BS:
        df = df.drop(columns=["BS"])

    return df


def calculate_AI(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates AI from DEN and AC according to the following formula::

        AI = DEN * ((304.8 / AC) ** 2)

    Args:
        df (pd.DataFrame): The dataframe to which AI should be added.

    Raises:
        ValueError: Raises an error if neither DEN nor AC are provided

    Returns:
        pd.DataFrame: Returns the dataframe with AI as a new column
    """
    if set(["DEN", "AC"]).issubset(set(df.columns)):
        df["AI"] = df["DEN"] * (304.8 / df["AC"])
    else:
        raise ValueError(
            "Not possible to generate AI as DEN and AC are not present in the dataset."
        )
    return df


def calculate_LI(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates LI from LFI according to the following formula::

        LI = ABS(ABS(LFI) - LFI) / 2

    If LFI is not in the provided dataframe, it is calculated using the
    calculate_LFI method of this module.

    Args:
        df (pd.DataFrame): The dataframe to which LI should be added.

    Raises:
        ValueError: Raises an error if neither NEU nor DEN or LFI are provided

    Returns:
        pd.DataFrame: Returns the dataframe with LI as a new column
    """
    if "LFI" in df.columns:
        pass
    elif set(["NEU", "DEN"]).issubset(set(df.columns)):
        df = calculate_LFI(df)
    else:
        raise ValueError(
            "Not possible to generate LI as NEU and DEN or LFI are not present in dataset."
        )
    df["LI"] = abs(abs(df["LFI"]) - df["LFI"]) / 2
    df = df.drop(columns=["LFI"])
    return df


def calculate_FI(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates FI from LFI according to the following formula::

        FI = (ABS(LFI) + LFI) / 2

    If LFI is not in the provided dataframe, it is calculated using the
    calculate_LFI method of this module.

    Args:
        df (pd.DataFrame): The dataframe to which FI should be added.

    Raises:
        ValueError: Raises an error if neither NEU nor DEN or LFI are provided

    Returns:
        pd.DataFrame: Returns the dataframe with FI as a new column
    """
    if "LFI" in df.columns:
        pass
    elif set(["NEU", "DEN"]).issubset(set(df.columns)):
        df = calculate_LFI(df)
    else:
        raise ValueError(
            "Not possible to generate FI as NEU and DEN or LFI are not present in dataset."
        )
    df["FI"] = (df["LFI"].abs() + df["LFI"]) / 2
    df = df.drop(columns=["LFI"])
    return df


def calculate_LFI(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Calculates LFI from NEU and DEN according to the following formula::

        LFI = 2.95 - ((NEU + 0.15) / 0.6) - DEN

    where:

        * LFI < -0.9 = 0
        * NaNs are filled with 0. unless fill_na is set to False

    Args:
        df (pd.DataFrame): The dataframe to which LFI should be added.

    Raises:
        ValueError: Raises an error if neither NEU nor DEN are provided

    Returns:
        pd.DataFrame: Returns the dataframe with LFI as a new column
    """
    fill_na: bool = kwargs.get("fill_na", True)
    if set(["NEU", "DEN"]).issubset(set(df.columns)):
        df["LFI"] = 2.95 - ((df["NEU"] + 0.15) / 0.6) - df["DEN"]
        df.loc[df["LFI"] < -0.9, "LFI"] = 0
        if fill_na:
            df["LFI"] = df["LFI"].fillna(0)
    else:
        raise ValueError(
            "Not possible to generate LFI as NEU and/or DEN are not present in dataset."
        )
    return df


def calculate_RAVG(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates RAVG from RDEP, RMED, RSHA according to the following formula::

        RAVG = AVG(RDEP, RMED, RSHA), if at least two of those are present

    Args:
        df (pd.DataFrame): The dataframe to which RAVG should be added.

    Raises:
        ValueError: Raises an error if one or less resistivity curves are found
            in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with RAVG as a new column
    """
    r_curves = [c for c in ["RDEP", "RMED", "RSHA"] if c in df.columns]
    if len(r_curves) > 1:
        df["RAVG"] = df[r_curves].mean(axis=1)
    else:
        raise ValueError(
            "Not possible to generate RAVG as there is only one or none resistivities curves in dataset."
        )
    return df


def calculate_VPVS(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates VPVS from ACS and AC according to the following formula::

        VPVS = ACS / AC

    Args:
        df (pd.DataFrame): The dataframe to which VPVS should be added.


    Raises:
        ValueError: Raises an error if neither ACS nor AC are found
            in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with VPVS as a new column
    """
    if set(["AC", "ACS"]).issubset(set(df.columns)):
        df["VPVS"] = df["ACS"] / df["AC"]
    else:
        raise ValueError(
            "Not possible to generate VPVS as both necessary curves (AC and"
            " ACS) are not present in dataset."
        )
    return df


def calculate_PR(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates PR from VP and VS or ACS and AC (if VP and VS are not found)
    according to the following formula::

        PR = (VP ** 2 - 2 * VS ** 2) / (2 * (VP ** 2 - VS ** 2))

    where:

        * VP = 304.8 / AC
        * VS = 304.8 / ACS

    Args:
        df (pd.DataFrame): The dataframe to which PR should be added.

    Raises:
        ValueError: Raises an error if none of AC, ACS, VP or VS are found
            in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with PR as a new column
    """
    drop = False
    if not set(["VP", "VS"]).issubset(set(df.columns)):
        if set(["AC", "ACS"]).issubset(set(df.columns)):
            df = calculate_VP(df)
            df = calculate_VS(df)
            drop = True  # Don't want to add unwanted columns
        else:
            raise ValueError(
                "Not possible to generate PR as none of the neccessary curves "
                "(AC, ACS or VP, VS) are present in the dataset."
            )
    df["PR"] = (df["VP"] ** 2 - 2.0 * df["VS"] ** 2) / (
        2.0 * (df["VP"] ** 2 - df["VS"] ** 2)
    )
    if drop:
        df = df.drop(columns=["VP", "VS"])
    return df


def calculate_VP(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Calculates VP (if AC is found) according to the following formula::

        VP = 304.8 / AC

    Args:
        df (pd.DataFrame): The dataframe to which PR should be added.

    Raises:
        ValueError: Raises an error if AC is not found in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with VP as a new column
    """
    if "AC" in df.columns:
        df["VP"] = 304.8 / df["AC"]
    else:
        raise ValueError("Not possible to generate VP as AC is not present in dataset.")
    return df


def calculate_VS(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Calculates VS (if ACS is found) according to the following formula::

        VS = 304.8 / ACS

    Args:
        df (pd.DataFrame): The dataframe to which PR should be added.

    Raises:
        ValueError: Raises an error if ACS is not found in the provided dataframe

    Returns:
        pd.DataFrame: Returns the dataframe with VS as a new column
    """
    if "ACS" in df.columns:
        df["VS"] = 304.8 / df["ACS"]
    else:
        raise ValueError(
            "Not possible to generate VS as ACS is not present in dataset."
        )
    return df


def calculate_diffRes(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Calculates the difference between two resistivity logs according to the following formula::

        diffRes = RDEP - RMED

    Args:
        df (pd.DataFrame): The dataframe to which diffRes should be added.
        left (str): The name of the left resistivity log. Defaults to None
        right (str): The name of the right resistivity log. Defaults to None
        fill_na (float): An option to fill the NaN values with the provided value. Defaults to None

    Note:
        The returned column is named according to the following convention::

            <left>-<right>

    Returns:
        pd.DataFrame: Returns the dataframe with the calculated column
    """
    left = kwargs.get("left", None)
    right = kwargs.get("right", None)
    fill_na = kwargs.get("fill_na", None)
    if left is None or right is None:
        warnings.warn(
            "Not possible to calculate_diffRes because the kwargs left and/or "
            "right are not provided. Returning the dataframe without any changes."
        )
        return df

    if left not in df.columns or right not in df.columns:
        raise ValueError(
            f"Not possible to generate diffRes as {left} and/or {right} are not present in dataframe."
        )

    df[f"{left}-{right}"] = df[left] - df[right]
    if fill_na is not None:
        df[f"{left}-{right}"] = df[f"{left}-{right}"].fillna(fill_na)

    return df


def calculate_VSH(df: pd.DataFrame, **kwargs):
    """
    Calculates VSH by calling the deployed automatic_vsh function in CDF.

    Refer to the automatic_vsh repo for more information about supported kwargs.

    Args:
        df (pd.DataFrame): pandas df to add depth trend to

    Keyword Args:
        id_column (str): REQUIRED identifier for the well column in the provided dataframe
            Defaults to None
        keyword_arguments (dict): REQUIRED dictionary containing any kwargs for the function call.
            Must contain 'nan_textual_value' & 'nan_numerical_value' key value
            pairs.
        client (CogniteClient): OPTIONAL client for querying depth trend function from CDF
            Defaults to None
        env (str): OPTIONAL environment where function is hosted (typically test or prod). Defaults to prod
        version (str): OPTIONAL version of function to be called. Defaults to latest.
        return_CI (bool): OPTIONAL whether to return confidence interval to the trends.

    Returns:
        pd.DataFrame: dataframe with added depth trend and optionally its confidence intervals
    """

    id_column: str = kwargs.get("id_column", None)
    client: CogniteClient = kwargs.get("client", None)
    env: str = kwargs.get("env", "prod")
    version: str = kwargs.get("version", None)
    return_CI: bool = kwargs.get("return_CI", False)
    user_kwargs: Dict[str, Any] = kwargs.get("keyword_arguments", None)

    # Validate input parameters
    if id_column is None:
        raise ValueError("id column (well name column) is a required kwarg!")
    if user_kwargs is None:
        raise ValueError(
            "keyword_arguments is a required kwarg! Please refer to the docstring for more information."
        )
    else:
        if "nan_textual_value" not in user_kwargs:
            raise ValueError(
                "nan_textual_value is a required kwarg! Please refer to the docstring for more information."
            )
        if "nan_numerical_value" not in user_kwargs:
            raise ValueError(
                "nan_numerical_value is a required kwarg! Please refer to the docstring for more information."
            )

    if "FORMATION_GROUP" not in df.columns:
        if {"FORMATION", "GROUP"}.issubset(set(df.columns)):
            df["FORMATION_GROUP"] = df["FORMATION"].fillna(df["GROUP"])
        else:
            df["FORMATION_GROUP"] = user_kwargs["nan_textual_value"]

    if version is None:
        version = "latest"
        external_id = f"automatic_vsh-prediction-{env}"
    else:
        external_id = f"automatic_vsh-prediction-{env}-{version}"
    df_ = utilities.run_deployed_model(
        df=df,
        id_column=id_column,
        keyword_arguments=user_kwargs,
        cdf_external_id=external_id,
        client=client,
    )

    # For akerbp.mlpet purposes (mostly as feat eng for ML Models) we want to
    # rename VSH_AUT to VSH for better compability with preprocessing
    df_ = df_.rename(columns={"VSH_AUT": "VSH"})
    df_.drop(columns=["FORMATION_GROUP"], inplace=True, errors="ignore")
    if not return_CI:
        output_curves = [c for c in df_.columns if "_P" not in c]
        return df_[output_curves]
    return df_
