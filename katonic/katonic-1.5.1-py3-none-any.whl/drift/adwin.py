#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Union

import numpy as np
import pandas as pd
from river.drift import ADWIN as AD
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_is_fitted


class ADWIN(BaseEstimator, ClassifierMixin):

    def __init__(self, **kwargs):
        """
        Calculates Drift using the Adaptive Windowing method for concept drift detection.
        """
        self.adwin  = AD(**kwargs)
        self.X_ = []
        self.result = []
        self.col_names = []
    
    def fit(self, X : Union[pd.DataFrame, np.ndarray]):
        """
        Fit ADWIN on train set.

        Args:
            X (pandas.DataFrame or numpy.ndarray): Shape (n_samples, n_features), where n_samples is the number of samples and 
            n_features is the number of features for train dataset.
        """
        if isinstance(X, pd.DataFrame): 
            self.col_names = X.columns
            self.clf_list = [self.adwin.clone() for _ in self.col_names]
            self.clf_ = [[clf for i, val in enumerate(X[col]) if clf.update(val) and i == (len(X[col])-1) ] for col, clf in zip(self.col_names, self.clf_list)]


        if isinstance(X, np.ndarray):
            self.col_names = range(X.shape[1])
            self.clf_list = [self.adwin.clone() for _ in self.col_names]
            self.clf_ = [[clf for i, val in enumerate(X[:, col]) if clf.update(val) and i == (len(X[:, col])-1)] for col, clf in zip(self.col_names, self.clf_list)]

        for clf, col in zip(self.clf_, self.col_names):
            print(f'For column {col} : \n variance in window {clf[0].variance / clf[0].width} \n mean in window {clf[0].total / clf[0].width}')
        # Return the classifier
        return self
    
    def predict(self, X: Union[pd.DataFrame,np.ndarray]):
        """
        Predict using ADWIN on test set.

        Args:
            X (pandas.DataFrame or numpy.ndarray): Shape (n_samples, n_features), where n_samples is the number of samples and 
            n_features is the number of features for test dataset.
        """
        check_is_fitted(self)

        if isinstance(X, pd.DataFrame) and isinstance(self.col_names, range) :    
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1], 'Variance of window': clf[0].variance / clf[0].width, 'No of Detections': clf[0].n_detections, 'Mean of widow': clf[0].total / clf[0].width, 'Column name or number': col} for val in X.iloc[:, col]] for col, clf in zip(self.col_names, self.clf_)]
        
        if isinstance(X, pd.DataFrame) and isinstance(self.col_names, pd.core.indexes.base.Index) : 
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1], 'Variance of window': clf[0].variance / clf[0].width, 'No of Detections': clf[0].n_detections, 'Mean of widow': clf[0].total / clf[0].width, 'Column name or number': col} for val in X[col]] for col, clf in zip(self.col_names, self.clf_)]
        
        if isinstance(X, np.ndarray) and isinstance(self.col_names, pd.core.indexes.base.Index):    
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1], 'Variance of window': clf[0].variance / clf[0].width, 'No of Detections': clf[0].n_detections, 'Mean of widow': clf[0].total / clf[0].width, 'Column name or number': self.col_names[col]} for val in X[col]] for col, clf in zip(range(len(self.col_names)), self.clf_)]

        if isinstance(X, np.ndarray) and isinstance(self.col_names, range) :    
            self.result = [[{'Is drift': clf[0].update(val)[0], 'Is warning': clf[0].update(val)[1], 'Variance of window': clf[0].variance / clf[0].width, 'No of Detections': clf[0].n_detections, 'Mean of widow': clf[0].total / clf[0].width, 'Column name or number': col} for val in X[:, col]]for col, clf in zip(self.col_names, self.clf_)]
            
        return self.result