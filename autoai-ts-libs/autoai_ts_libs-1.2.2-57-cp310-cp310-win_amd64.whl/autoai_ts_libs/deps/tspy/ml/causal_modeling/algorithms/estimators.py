#  /************** Begin Copyright - Do not add comments here **************
#   * Licensed Materials - Property of IBM
#   *
#   *   OCO Source Materials
#   *
#   *   (C) Copyright IBM Corp. 2020, All Rights Reserved
#   *
#   * The source code for this program is not published or other-
#   * wise divested of its trade secrets, irrespective of what has
#   * been deposited with the U.S. Copyright Office.
#   ***************************** End Copyright ****************************/

'''
CausalityEstimator class: to be inherited by causal algorithm implementations
'''

import abc
import sys
from sklearn.base import BaseEstimator

if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta(str('ABC'), (), {})


class CausalityEstimator(BaseEstimator):
    """ 
    """
    def __init__(self, *argv, **kwargs):
        """
        """

    @abc.abstractmethod
    def fit(self, *argv, **kwargs):
        """ 
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_weighted_causes(self, *argv, **kwargs):
        """ 
        """
        raise NotImplementedError

