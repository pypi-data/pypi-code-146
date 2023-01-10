#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Union

import numpy as np
import pandas as pd
from river.drift import HDDM_W as HDD_W
from sklearn.utils.validation import check_is_fitted
from sklearn.base import BaseEstimator, ClassifierMixin


class HDDM_W(BaseEstimator, ClassifierMixin):

    def __init__(self, **kwargs):
        """
        Calculates Drift using Drift Detection Method based on Hoeffding's bounds with moving weighted average-test.
        """
        self.hddm_w = HDD_W(**kwargs)
        self.X_ = []
        self.result = []
        self.col_names = []
    
    def fit(self, X: Union[pd.DataFrame, np.ndarray]):
        """
        Fit HDDM_W on train set.

        Args:
            X (pandas.DataFrame or numpy.ndarray): Shape (n_samples, n_features), where n_samples is the number of samples and 
            n_features is the number of features for train dataset.
        """
        if isinstance(X, pd.DataFrame):
            self.col_names = X.columns
            self.clf_list = [self.hddm_w.clone() for _ in self.col_names]
            self.clf_ = [[clf for i, val in enumerate(X[col]) if clf.update(val) and i == (len(X[col]) - 1)] for col, clf in zip(self.col_names, self.clf_list)]

        if isinstance(X, np.ndarray):
            self.col_names = range(X.shape[1])
            self.clf_list = [self.hddm_w.clone() for _ in self.col_names]
            self.clf_ = [[clf for i, val in enumerate(X[:, col]) if clf.update(val) and i == (len(X[:, col]) - 1)] for col, clf in zip(self.col_names, self.clf_list)]

        return self
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]):
        """
        Predict drift using HDDM_W on test set.

        Args:
            X (pandas.DataFrame or numpy.ndarray): Shape (n_samples, n_features), where n_samples is the number of samples and 
            n_features is the number of features for test dataset.
        """
        # Check is fit had been called
        check_is_fitted(self)

        if isinstance(X, pd.DataFrame) and isinstance(self.col_names, range):
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1]} for val in X.iloc[:, col]] for col, clf in zip(self.col_names, self.clf_)]
        
        if isinstance(X, pd.DataFrame) and isinstance(self.col_names, pd.core.indexes.base.Index):
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1]} for val in X[col]] for col, clf in zip(self.col_names, self.clf_)]
        
        if isinstance(X, np.ndarray) and isinstance(self.col_names, pd.core.indexes.base.Index):
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1]} for val in X[:, col]]for col, clf in zip(range(len(self.col_names)), self.clf_)]

        if isinstance(X, np.ndarray) and isinstance(self.col_names, range):
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1]} for val in X[:, col]] for col, clf in zip(self.col_names, self.clf_)]
        
        return self.result