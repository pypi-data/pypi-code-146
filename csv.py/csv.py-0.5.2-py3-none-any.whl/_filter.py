import pandas as pd
import math
import numpy as np
from typing import List

def column_equal(*,
        df :pd.DataFrame,
        column_name: str,
        value
) -> pd.DataFrame:
    if column_name in df.columns:
        return df.loc[df[column_name] == value]
    else:
        return pd.DataFrame(columns=df.columns)

def filter_row(
        *,
        df: pd.DataFrame,
        condition: callable,
):
    return df[df.apply(condition,axis=1)]


def count_row(
    *,
    df: pd.DataFrame,
    condition: callable,
):
    return len(df[df.apply(condition,axis=1)])

def is_numeric(const):
    return str(const).isnumeric()


def is_nan(scalar):
    if scalar is None:
        return True
    try:
        scalar = float(scalar)
        return math.isnan(scalar)
    except:
        return False



def count_nan(
    *,
    df: pd.DataFrame,
    column: str
):
    cond = lambda x : is_nan(x[column])
    return count_row(df=df,condition=cond)


def count_numeric(*,
    df: pd.DataFrame,
    column: str
):
    cond = lambda x : is_numeric(x[column])
    return count_row(df=df,condition=cond)


def drop_nan(
    *,
    df: pd.DataFrame,
    column: str,
):
    cond = lambda x : not is_nan(x[column])
    return filter_row(df=df,condition=cond)


def drop_numeric(
    *,
    df: pd.DataFrame,
    column: str,
):
    cond = lambda x : not is_numeric(x[column])
    return filter_row(df=df,condition=cond)


def drop_nan_multicol(
    *,
    df:pd.DataFrame,
    columns: List[str]
):
    cond = lambda x : all([not is_nan(x[col]) for col in columns])
    return filter_row(df=df,condition=cond)

def drop_numeric_multicol(
    *,
    df:pd.DataFrame,
    columns: List[str]
):
    cond = lambda x : all([not is_numeric(x[col]) for col in columns])
    return filter_row(df=df,condition=cond)