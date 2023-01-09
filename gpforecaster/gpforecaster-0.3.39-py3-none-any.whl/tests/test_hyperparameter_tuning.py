import unittest
import timeit

import tsaugmentation as tsag

from gpforecaster.model.gpf import GPF
from gpforecaster.model.hyperparameter_tuning import optimize_hyperparameters


class TestModel(unittest.TestCase):
    def setUp(self):
        self.dataset_name = "prison"
        self.data = tsag.preprocessing.PreprocessDatasets(
            self.dataset_name
        ).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]

    def test_early_stopping_w_patience(self):
        best_hyperparameters = optimize_hyperparameters(
            dataset_name=self.dataset_name, hierarchical_data=self.data, num_trials=2
        )
        self.assertIsNotNone(best_hyperparameters)
