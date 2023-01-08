"""
Library of utilities to support the SkillMetrics package
"""
import numpy as np


def check_arrays(predicted, reference):
    """
    Checks two arrays have the same dimensions.

    Input:
    PREDICTED : predicted field
    REFERENCE : reference field

    Author: Tim Cera
        St. Johns River Water Management District
        University of Florida
        Gainesville, FL
        https://www.linkedin.com/in/timcera
        https://github.com/timcera

    Created on Mar 23, 2019
    """

    pdims = predicted.shape
    rdims = reference.shape
    if not np.array_equal(pdims, rdims):
        raise ValueError(
            """
*
*   The predicted and reference field dimensions do not match.
*       shape(predicted) = {}
*       shape(reference) = {}
*       predicted type: {}
*
""".format(
                pdims, rdims, type(predicted)
            )
        )
