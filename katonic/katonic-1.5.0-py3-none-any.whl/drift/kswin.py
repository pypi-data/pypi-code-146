#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Union

import numpy as np
import pandas as pd
from river.drift import KSWIN as KS
from sklearn.utils.validation import check_is_fitted
from sklearn.base import BaseEstimator, ClassifierMixin


class KSWIN(BaseEstimator, ClassifierMixin):

    def __init__(self, **kwargs):
        """
        Calculates Drift using Kolmogorov-Smirnov Windowing method for concept drift detection.
        """
        self.kswin = KS(**kwargs)
        self.X_ = []
        self.result = []
        self.col_names = []
    
    def fit(self, X: Union[pd.DataFrame, np.ndarray]):
        """
        Fit KSWIN on train set.

        Args:
            X (pandas.DataFrame or numpy.ndarray): Shape (n_samples, n_features), where n_samples is the number of samples and 
            n_features is the number of features for train dataset.
        """
        if isinstance(X, pd.DataFrame):
            self.col_names = X.columns
            self.clf_list = [self.kswin.clone() for _ in self.col_names]
            self.clf_ = [[clf for i, val in enumerate(X[col]) if clf.update(val) and i == (len(X[col]) - 1)] for col, clf in zip(self.col_names, self.clf_list)]

        if isinstance(X, np.ndarray):
            self.col_names = range(X.shape[1])
            self.clf_list = [self.kswin.clone() for _ in self.col_names]
            self.clf_ = [[clf for i, val in enumerate(X[:, col]) if clf.update(val) and i == (len(X[:, col]) - 1)] for col, clf in zip(self.col_names, self.clf_list)]

        for clf, col in zip(self.clf_, self.col_names):
            print(f'For column {col} : \n p_value {clf[0].p_value}')
        # Return the classifier
        return self
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]):
        """
        Predict drift using KSWIN on test set.

        Args:
            X (pandas.DataFrame or numpy.ndarray): Shape (n_samples, n_features), where n_samples is the number of samples and 
            n_features is the number of features for test dataset.
        """
        # Check is fit had been called
        check_is_fitted(self)

        if isinstance(X, pd.DataFrame) and isinstance(self.col_names, range):
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1], 'p_value': clf[0].p_value, 'Column name or number': col} for val in X.iloc[:, col]] for col, clf in zip(self.col_names, self.clf_)]
        
        if isinstance(X, pd.DataFrame) and isinstance(self.col_names, pd.core.indexes.base.Index):
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1], 'p_value': clf[0].p_value, 'Column name or number': col} for val in X[col]] for col, clf in zip(self.col_names, self.clf_)]
        
        if isinstance(X, np.ndarray) and isinstance(self.col_names, pd.core.indexes.base.Index):
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1], 'p_value': clf[0].p_value, 'Column name or number': self.col_names[col]} for val in X[:, col]] for col, clf in zip(range(len(self.col_names)), self.clf_)]

        if isinstance(X, np.ndarray)and isinstance(self.col_names, range):
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1], 'p_value': clf[0].p_value, 'Column name or number': col} for val in X[:, col]] for col, clf in zip(self.col_names, self.clf_)]

        return self.result