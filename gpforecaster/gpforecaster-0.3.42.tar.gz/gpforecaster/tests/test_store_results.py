import unittest
import pickle

import tsaugmentation as tsag

from gpforecaster.model.gpf import GPF
from gpforecaster import __version__


class TestModel(unittest.TestCase):
    def setUp(self):
        self.dataset_name = "prison"
        self.gp_type = "exact"
        self.version = __version__
        self.data = tsag.preprocessing.PreprocessDatasets(
            self.dataset_name
        ).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]
        self.h = self.data["h"]
        self.gpf = GPF(
            self.dataset_name,
            self.data,
            log_dir="..",
            gp_type=self.gp_type,
            inducing_points_perc=0.75,
        )
        self.gpf.input_dir = f"./results/gpf/"

    def test_store_fit_pred_mean_results_gp(self):
        model, like = self.gpf.train(
            epochs=10,
            patience=4,
            track_mem=True,
            lr=1e-2,
        )
        preds, preds_scaled = self.gpf.predict(model, like)
        res_type = "fitpred"
        res_measure = "mean"
        self.gpf.store_results(preds[0], res_type=res_type, res_measure=res_measure)
        with open(
            f"{self.gpf.input_dir}results_{res_type}_{res_measure}_gp_{self.gp_type}_cov_{self.dataset_name}_{self.version}.pickle",
            "rb",
        ) as handle:
            res = pickle.load(handle)
        self.assertTrue(res.shape == (self.n, self.s))

    def test_store_pred_std_results_gp(self):
        model, like = self.gpf.train(
            epochs=10,
            patience=4,
            track_mem=True,
            lr=1e-2,
        )
        preds, preds_scaled = self.gpf.predict(model, like)
        res_type = "pred"
        res_measure = "std"
        self.gpf.store_results(
            preds[1][self.n - self.h :, :], res_type=res_type, res_measure=res_measure
        )
        with open(
            f"{self.gpf.input_dir}results_{res_type}_{res_measure}_gp_{self.gp_type}_cov_{self.dataset_name}_{self.version}.pickle",
            "rb",
        ) as handle:
            res = pickle.load(handle)
        self.assertTrue(res.shape == (self.h, self.s))

    def test_store_metrics_gp(self):
        model, like = self.gpf.train(
            epochs=10,
            patience=4,
            track_mem=True,
            lr=1e-2,
        )
        self.gpf.input_dir = f"./results/gpf/"
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])
        self.gpf.store_metrics(res)
        with open(
            f"{self.gpf.input_dir}metrics_gp_{self.gp_type}_cov_{self.dataset_name}_{self.version}.pickle",
            "rb",
        ) as handle:
            res = pickle.load(handle)
        keys = list(res.keys())
        self.assertTrue(keys == ['mase', 'rmse', 'CRPS', 'wall_time'])
