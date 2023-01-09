import unittest

import tsaugmentation as tsag

from gpforecaster.model.gpf import GPF
from gpforecaster.visualization.plot_predictions import plot_predictions_vs_original


class TestModel(unittest.TestCase):
    def setUp(self):
        self.dataset_name = "prison"
        self.data = tsag.preprocessing.PreprocessDatasets(
            self.dataset_name
        ).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]
        self.gpf_ngd = GPF(
            self.dataset_name,
            self.data,
            log_dir="..",
            gp_type="ngd_predloglike",
            inducing_points_perc=0.75,
        )
        self.gpf_svg = GPF(
            self.dataset_name,
            self.data,
            log_dir="..",
            gp_type="svg_predloglike",
            inducing_points_perc=0.75,
        )

    def test_svg_pll_gp(self):
        model, like = self.gpf_svg.train(
            epochs=100,
            patience=4,
            track_mem=True
        )
        preds, preds_scaled = self.gpf_svg.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf_svg.original_data,
            inducing_points=self.gpf_svg.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf_svg.gp_type,
        )
        self.gpf_svg.plot_losses(5)
        self.gpf_svg.metrics(preds[0], preds[1])
        self.assertLess(self.gpf_svg.losses[-1], 5)

    def test_ngd_pll_gp(self):
        model, like = self.gpf_ngd.train(
            epochs=100,
            patience=4,
            track_mem=True
        )
        preds, preds_scaled = self.gpf_ngd.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf_ngd.original_data,
            inducing_points=self.gpf_ngd.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf_ngd.gp_type,
        )
        self.gpf_ngd.plot_losses(5)
        self.gpf_ngd.metrics(preds[0], preds[1])
        self.assertLess(self.gpf_ngd.losses[-1], 5)
