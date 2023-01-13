"""
Helper functions that help load datasets in Ananke.
"""

import pandas as pd
import os

MODULE_PATH = os.path.dirname(__file__)


def load_conditionally_ignorable_data():
    """
    Load toy data for the conditionally ignorable model
    where the confounder is Viral Load, T is the treatment
    and the outcome is CD4 counts.

    :return: pandas dataframe.
    """

    path = os.path.join(MODULE_PATH, "simulated/conditionally_ignorable.csv")
    return pd.read_csv(path)


def load_afixable_data():
    """
    Load toy data for an adjustment fixable setting
    where T is the treatment and the outcome is CD4 counts.

    :return: pandas dataframe.
    """

    path = os.path.join(MODULE_PATH, "simulated/a_fixable.csv")
    return pd.read_csv(path)


def load_frontdoor_data():
    """
    Load toy data for frontdoor setting
    where T is the treatment and the outcome is CD4 counts.

    :return: pandas dataframe.
    """

    path = os.path.join(MODULE_PATH, "simulated/frontdoor.csv")
    return pd.read_csv(path)


def load_wisconsin_health_study():
    """
    Load the dataset extract from the Wisconsin Health Study presented in [1].
    Columns are defined as follows:
    X: an indicator of whether family income in 1957 was above \$5k;
    Y: an indicator of whether the respondents income in 1992 was above \$37k;
    M: an indicator of whether the respondent was drafted into the military;
    E: an indicator of whether the respondent had education beyond high school.
    count: the count of each event in (X, Y, M, E)

    [1] R. J. Evans and T. S. Richardson, “Smooth, identifiable supermodels of discrete DAG models with latent variables,” Bernoulli, vol. 25, no. 2, pp. 848–876, May 2019, doi: 10.3150/17-BEJ1005.


    """
    path = os.path.join(MODULE_PATH, "real/evans_richardson_wisconsin.csv")
    return pd.read_csv(path)
