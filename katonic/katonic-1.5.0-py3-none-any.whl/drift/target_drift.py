#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

import numpy as np
import pandas as pd
from sklearn.utils.validation import check_is_fitted


class PSI(object):
     
    def __init__(self):
        """
        Calculates the Population Stability Index (PSI) for target variables.
        """
        self.threshold = []
        self.bucket = 10  
        self.window = np.array([])
    
    def fit(self, actual):
        """
        Fit the PSI model according to the given scoring data.

        Args:
            actual (array-like of shape (n_samples,)): Target values (probability(real number) in classification, real numbers in regression)

        Returns:
            self: object
        """        
        self.threshold = np.stack([np.percentile(actual, b) for b in np.arange(0, self.bucket + 1) / (self.bucket) * 100])
        self.X_ = actual
        self.train_size =len(actual)
         
        return self

    def predict(self, X_test):
        """
        Calculate the PSI score taking training (reference data) and test target columns.

        Args:
            X_test (array-like of shape (n_samples, )): Target values (probability (real number) in classification, real numbers in regression)

        Returns:
            float: total PSI score
        """        
        check_is_fitted(self)

        PSI_ = np.array([0])
        self.window = np.concatenate([self.window, X_test])
        test_size = len(self.window)
        if test_size >= self.train_size:
            X_test_batch = self.window[: self.train_size]
            train_counts = np.histogram(self.X_, self.threshold)[0]
            test_counts  = np.histogram(X_test_batch, self.threshold)[0]
            train_counts_pct = train_counts / len(self.X_)
            train_counts_pct[train_counts_pct == 0] = 0.0001
            test_count_pct = test_counts / len(X_test_batch)
            test_count_pct[test_count_pct == 0] = 0.0001
            trainpct_minus_testpct = train_counts_pct - test_count_pct
            ln_trainpct_div_testpct = np.log(train_counts_pct / test_count_pct)
            PSI_ = trainpct_minus_testpct * ln_trainpct_div_testpct
            new_batch_win = test_size - self.train_size
            new_batch_win = new_batch_win + self.train_size
            self.window = self.window[: new_batch_win]
        
        #print(self.window.size) 
        return PSI_.sum()

class CSI(object):
    
    def __init__(self, breakpoint=0.2):
        """
        Calculates CSI score for all the columns fed to model, used when PSI score>=0.2
        """    
        self.threshold = []
        self.bucket = 10  
        self.column_names = []
        self.window = np.array([])
        self.wthreshold = breakpoint
    
    def fit(self, actual):
        """
        Fit the CSI model according to the given features.

        Args:
            actual ({array-like, sparse matrix} of shape (n_samples, n_features)): Training vectors, where n_samples is the number of samples and n_features is the number of features.

        Returns:
            self: object
        """
        if len(actual.shape) == 0:
            raise Exception("No input columns present")

        if len(actual.shape) == 1 and isinstance(actual, np.ndarray):
            self.column_names = ['col1']

        if isinstance(actual, pd.Series):
            self.column_names = actual.name or ['col1']
            actual = actual.to_numpy()

        if isinstance(actual, np.ndarray):
            self.column_names = [f'col{str(i)}' for i in range(actual.shape[1])]

        if isinstance(actual, pd.DataFrame):
            self.column_names = actual.columns.tolist()
            actual = actual.to_numpy()    

        self.X_ = actual
        self.train_size = len(actual)

        if len(actual.shape) == 1:
            self.threshold.append(np.stack([np.percentile(actual, b) for b in np.arange(0, self.bucket + 1) / (self.bucket) * 100]))
        else:
            for column in range(actual.shape[1]):
                x = actual[:, column]
                self.threshold.append(np.stack([np.percentile(x, b) for b in np.arange(0, self.bucket+1) / (self.bucket) * 100]))

        return self

    def predict(self, X_test):
        """
        Calculate the CSI score taking training (reference data) and test feature columns.

        Args:
            X_test ({array-like, sparse matrix} of shape (n_samples, n_features)): features from the testing data

        Raises:
            Exception: when number of columns does not match between training and test data

        Returns:
            list: list of column names that led to drift in scoring variable
        """        
        columnresult = []
        test_columns = []
        train_counts = np.empty(1,)
        test_counts = np.empty(1,)
        psiresult = {}
        #check if predict is called
        check_is_fitted(self)

        if isinstance(X_test, np.ndarray):
            test_columns = [f'col{str(i)}' for i in range(X_test.shape[1])]

        if isinstance(X_test, pd.DataFrame):
            test_columns = X_test.columns.tolist()
            X_test = X_test.to_numpy()

        if isinstance(X_test, pd.Series):
            test_columns = X_test.name or ['col1']
            X_test = X_test.to_numpy()

        columns = len(self.column_names)
        if test_columns != self.column_names:
            raise Exception("Column names or number of columns does not match")

        if  self.window.size == 0:  
            self.window = X_test
        else:    
            self.window = np.concatenate([self.window, X_test])
        test_size = len(self.window)
        if test_size >= self.train_size:
            X_test_batch = self.window[: self.train_size]
            for cutpoint, column in zip(self.threshold, range(columns)):
                if  columns == 1:
                    train_counts = np.histogram(self.X_, cutpoint)[0]
                    test_counts = np.histogram(X_test_batch, cutpoint)[0]
                else:
                    train_counts = np.histogram(self.X_[:, column], cutpoint)[0]
                    test_counts = np.histogram(X_test_batch[:, column], cutpoint)[0]
                train_counts_pct = train_counts / len(self.X_)
                train_counts_pct[train_counts_pct == 0] = 0.0001
                test_count_pct = test_counts / len(X_test_batch)
                test_count_pct[test_count_pct == 0] = 0.0001
                trainpct_minus_testpct = train_counts_pct - test_count_pct
                ln_trainpct_div_testpct = np.log(train_counts_pct / test_count_pct)
                PSI_ = trainpct_minus_testpct * ln_trainpct_div_testpct
                psiresult[column] = PSI_.sum()

            columnresult.extend(name for col, name in zip(psiresult.keys(), self.column_names) if psiresult[col] >= self.wthreshold)

            new_batch_win = test_size-self.train_size
            new_batch_win = new_batch_win + self.train_size
            self.window = self.window[: new_batch_win]

        return columnresult