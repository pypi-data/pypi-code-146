#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import logging
from typing import List
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import chi2
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import mutual_info_regression
from sklearn.feature_selection import RFE

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureSelection:
    def __init__(self, input_data: pd.DataFrame, target_column: pd.Series):
        self.input_data = input_data
        self.target_column = target_column

    def recursive_feature_elimination(
        self,
        problem_type: str = "regression",
        no_of_features: int = 10,
        step: Union[int, float] = 1,
        verbose: int = 0,
    ) -> Tuple[pd.DataFrame, sklearn.feature_selection._rfe.RFE]:
        """
        Perform feature selection on training data using Recursive feature elimination
        Parameters:
            problem_type: Wheather the problem statement is a regression or classification
            no_of_features: Number of features to be selected.
            step: If greater than or equal to 1, then step corresponds to the (integer)
                    number of features to remove at each iteration. If within (0.0, 1.0),
                    then step corresponds to the percentage (rounded down) of features to
                    remove at each iteration.
            verbose: Controls verbosity of output.
        Return:
            [pd.DataFrame]: Return pandas dataframe with new selected features
            [sklearn.feature_selection._rfe.RFE]: Recursive feature elimination model
        """
        try:
            if not (problem_type == "classification" or problem_type == "regression"):
                raise ValueError(
                    "problem_type must be either classification or regression"
                )
            if not isinstance(no_of_features, int):
                raise TypeError("no_of_features should be of int type")

            logger.info("Started feature selection on training dataset")
            if problem_type == "classification":
                logger.info(f"Problem type is {problem_type}")
                estimator = RandomForestClassifier()
            else:
                logger.info(f"Problem type is {problem_type}")
                estimator = RandomForestRegressor()
            feature_selection_model = RFE(
                estimator,
                n_features_to_select=no_of_features,
                step=step,
                verbose=verbose,
            )
            feature_selection_model.fit(self.input_data, self.target_column)
            output_array = feature_selection_model.transform(self.input_data)
            selected_features = list(feature_selection_model.get_feature_names_out())
            logger.info(
                f"Select {len(selected_features)} features from {len(self.input_data.columns)}"
            )
            output_df = pd.DataFrame(output_array, columns=selected_features)
            logger.info(f"Selected features are: {selected_features}")
            logger.info("Ended feature selection")

            return output_df, feature_selection_model
        except Exception as e:
            raise e

    def recursive_feature_elimination_on_test(
        self, feature_selection_model: sklearn.feature_selection._rfe.RFE
    ) -> pd.DataFrame:
        """
        Performs feature selection on test data
        Parameters:
            feature_selection_model: Feature selection model trained on test data
        Return:
            [pd.DataFrame]: Return pandas dataframe with selected features
        """
        if not isinstance(feature_selection_model, sklearn.feature_selection._rfe.RFE):
            raise TypeError("sklearn.feature_selection._rfe.RFE type")
        if not feature_selection_model:
            raise ValueError("feature_selection_model cannot be empty")
        selected_features = list(feature_selection_model.get_feature_names_out())

        logger.info("Started feature selection on test data")
        output_df = pd.DataFrame(self.input_data[selected_features])

        logger.info(f"Selected features are: {selected_features}")

        logger.info("Ended feature selection process.")

        return output_df

    def non_null_columns(self) -> pd.DataFrame:
        filtered_data = self.input_data.dropna(axis=1)
        dropped_cols = set(filtered_data.columns.to_list()) ^ set(
            self.input_data.columns.to_list()
        )
        logger.info(f"Dropped columns are: {dropped_cols}")
        return filtered_data

    def non_constant_columns(self, column_list: List[str], threshold: float = 0.1):
        non_zero_variance_column_list = []
        std_dict = self.input_data[column_list].std()
        non_zero_variance_column_list = [
            column
            for column, std in std_dict.items()
            if std and float(std) * 2 > threshold
        ]
        logger.info(f"Non constant columns are: {non_zero_variance_column_list}")
        return non_zero_variance_column_list

    def pearson_spearman_kendall_correlation(
        self, columns_list: List[str], method: str = "pearson"
    ) -> pd.Series:
        """
        Finds pearson/spearman/kendall correlation and return list of columns which has high correlation coefficient
        Args:
            column_list ([list]): [list of numeic column names]
            method ([String]): [pearson / spearman / kendall]
        Returns:
            [list]: [return list with high correlation coefficient]
        """
        try:
            if not (method == "pearson" or method == "spearman" or method == "kendall"):
                raise ValueError("method must be pearson/spearman/kendall")
            if not isinstance(columns_list, list):
                raise TypeError("columns_list should be of list type")

            logger.info(
                f"Started calculation correlation on training dataset with {method} method"
            )
            data = self.input_data[columns_list]
            data["target_col"] = self.target_column
            if method == "pearson":
                cor_values = data.corr()
            elif method == "spearman":
                cor_values = data.corr(method=method)
            else:
                cor_values = data.corr(method=method)
            cor_target = abs(cor_values["target_col"])
            logger.info("Ended feature selection")
            return cor_target
        except Exception as e:
            raise e

    def chi_squared(self, columns_list: List[str]) -> pd.Series:
        """
        Finds p-values value between categoric-categoric variables and return pandas dataframe which has p-value
        Args:
            column_list ([list]): [list of category column names]
            p_value ([float]): [P-value threshold for the operation]
        Returns:
            [Series]: [return pandas series with p-values]
        """
        try:
            if not isinstance(columns_list, list):
                raise TypeError("columns_list should be of list type")
            logger.info("Started calculation chi square on training dataset")
            X = self.input_data[columns_list]
            chi_scores = chi2(X, self.target_column)
            p_values = pd.Series(chi_scores[1], index=X.columns)
            p_values.sort_values(ascending=False, inplace=True)
            return p_values
        except Exception as e:
            raise e

    def mututal_information(
        self, columns_list: List[str], problem_type: str = "regression"
    ) -> pd.DataFrame:
        """
        Finds mutual information score and retuns a dataframe that satisfies the threshold value
        Args:
            column_list ([list]): [list of category column names]
            problem_type ([str]): [Wheather the problem statement is a regression or classification]
        Returns:
            [Dataframe]: [return pandas dataframe]
        """
        try:
            if not isinstance(columns_list, list):
                raise TypeError("columns_list should be of list type")
            if problem_type not in ["classification", "regression"]:
                raise ValueError(
                    "problem_type must be either classification or regression"
                )
            X = self.input_data[columns_list]
            logger.info("Started mutual information calculation on training dataset")
            if problem_type == "classification":
                logger.info(f"Problem type is {problem_type}")
                mi_score = mutual_info_classif(X, self.target_column)
            else:
                logger.info(f"Problem type is {problem_type}")
                mi_score = mutual_info_regression(X, self.target_column)
            return mi_score
        except Exception as e:
            raise e

    def get_selected_features(
        self,
        columns_list: List[str],
        chi2_data: pd.Series,
        mutual_info_data: pd.DataFrame,
        p_value_thresh: float = 0.05,
        mi_threshold: float = 0.2,
    ) -> List[str]:
        """
        Filterout the columns based on the threshold then retun the list
        Args:
            columns_list
            chi2_data ([Series]): [chi-squared pandas series]
            mutual_info_data: ([DataFrame]): [Mutual info pandas dataframe]
            p_value_thresh ([float]): [p-value limit to check hypothesis test]
            mi_threshold([float]): [Mutual inference threshold]
        Returns:
            [list]: [return list of selected features]
        """
        try:
            feature_selected = set()
            X = self.input_data[columns_list]
            chi2_data_selected = chi2_data[chi2_data <= p_value_thresh].index.to_list()
            mi_score_selected_index = np.where(mutual_info_data >= mi_threshold)[0]
            mutual_info_data_selected = X.iloc[
                :, mi_score_selected_index
            ].columns.to_list()
            feature_selected.update(chi2_data_selected)
            feature_selected.update(mutual_info_data_selected)
            logger.info(f"Selected features are: {feature_selected}")
            return sorted(feature_selected)
        except Exception as e:
            raise e

    def feature_selection(
        self,
        categorical_cols: List[str],
        numerical_cols: List[str],
        problem_type: str = "regression",
        method: str = "pearson",
        corr_threshold: float = 0.8,
        p_value_thresh: float = 0.05,
        mi_threshold: float = 0.2,
    ) -> List[str]:
        """
        Finds the list of features that will improve the model performance
        Args:
            categorical_cols ([list]): [Variable categorized categorical columns]
            numerical_cols ([list]): [Variable categorized numerical columns]
            problem_type ([str]): [Wheather the problem statement is a regression or classification]
            method ([String]): [pearson / spearman / kendall]
            corr_threshold ([float]): [threshold value to compair with correlation coefficient]
            p_value_thresh ([float]): [p-value limit to check hypothesis test]
            mi_threshold([float]): [Mutual information threshold]
        Returns:
            [list]: [return list of selected features]
        """
        try:
            all_columns = numerical_cols + categorical_cols
            self.input_data = self.input_data[all_columns]
            corr_data = self.pearson_spearman_kendall_correlation(
                numerical_cols, method
            )
            corr_data_filtered = corr_data[corr_data >= corr_threshold]
            feature_child = {}
            corr_data_selected = []
            for col_name in corr_data_filtered.index.tolist():
                name = col_name.split("_TRANSF")[0]
                feature_child[name] = list(
                    filter(
                        lambda column: (name in column),
                        corr_data_filtered.index.tolist(),
                    )
                )
            for index, value in feature_child.items():
                corr_data_selected.append(max(corr_data_filtered[value].index))
            corr_data_selected.remove("target_col")
            all_columns = categorical_cols + corr_data_selected
            chi2_data = pd.DataFrame()
            if problem_type == "classification":
                non_negative_cols = (
                    self.input_data[categorical_cols]
                    .columns[~(self.input_data[categorical_cols] < 0).any()]
                    .tolist()
                )
                chi2_data = self.chi_squared(non_negative_cols)
            mutual_info_data = self.mututal_information(all_columns, problem_type)
            selected_features = self.get_selected_features(
                all_columns, chi2_data, mutual_info_data, p_value_thresh, mi_threshold
            )
            rejected_features = set(self.input_data.columns) - set(selected_features)
            logger.info(f"Rejected features are: {rejected_features}")
            return selected_features
        except Exception as e:
            raise e
