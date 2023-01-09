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
        self.gpf = GPF(
            self.dataset_name,
            self.data,
            log_dir="..",
            gp_type="svg",
            inducing_points_perc=0.75,
        )

    def test_svg_gp(self):
        model, like = self.gpf.train(
            epochs=10,
            patience=4,
            track_mem=True,
            lr=1e-2,
        )
        self.gpf.input_dir = f'./results/gpf/'
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])
        self.gpf.store_metrics(res)
        self.assertLess(self.gpf.losses[-1], 10)
