import unittest
import tsaugmentation as tsag
from gpforecaster.model.gpf import GPF
import shutil


class TestModel(unittest.TestCase):

    def setUp(self):
        self.preproc = tsag.preprocessing.PreprocessDatasets('tourism', test_size=228*10)
        self.data = self.preproc._tourism()
        self.n = self.data['predict']['n']
        self.s = self.data['train']['s']
        self.gpf = GPF(dataset='tourism', groups=self.data)

    def test_results_mean_and_prediction_interval(self):
        model, like = self.gpf.train(epochs=10)
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])

        # Test shape of results
        self.assertTrue(res['mase']['bottom_ind'].shape == (self.s, ))
        self.assertTrue(res['CRPS']['bottom_ind'].shape == (self.s, ))
        self.assertTrue(res['rmse']['bottom_ind'].shape == (self.s, ))

    def test_results_mean_and_prediction_interval_without_storing_results(self):
        self.gpf = GPF(dataset='tourism', groups=self.data)
        model, like = self.gpf.train(epochs=10)
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])

        # Test shape of results
        self.assertTrue(res['mase']['bottom_ind'].shape == (self.s, ))
        self.assertTrue(res['CRPS']['bottom_ind'].shape == (self.s, ))
        self.assertTrue(res['rmse']['bottom_ind'].shape == (self.s, ))

        # Test shape of predictions
        # Test number of objects predicted and stored
        self.assertTrue(len(res) == 4)

