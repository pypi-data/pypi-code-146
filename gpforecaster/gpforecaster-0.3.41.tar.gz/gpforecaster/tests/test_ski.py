import unittest

import tsaugmentation as tsag

from gpforecaster.model.gpf import GPF
from gpforecaster.visualization.plot_predictions import plot_predictions_vs_original


class TestModel(unittest.TestCase):
    def setUp(self):
        self.dataset_name = "prison"
        self.data = tsag.preprocessing.PreprocessDatasets(self.dataset_name).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]
        self.gpf = GPF(
            self.dataset_name,
            self.data,
            log_dir=".",
            gp_type="ski",
            inducing_points_perc=0.75,
        )

    def test_ski_gp(self):
        model, like = self.gpf.train(epochs=10, patience=4, track_mem=True)
        preds, preds_scaled = self.gpf.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf.original_data,
            inducing_points=self.gpf.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf.gp_type,
        )
        self.gpf.plot_losses(5)
        self.gpf.metrics(preds[0], preds[1])
        self.assertLess(self.gpf.losses[-1], 5)
