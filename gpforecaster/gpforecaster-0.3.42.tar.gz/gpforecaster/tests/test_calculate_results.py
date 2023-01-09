import unittest
import tsaugmentation as tsag
from gpforecaster.model.gpf import GPF


class TestModel(unittest.TestCase):

    def setUp(self):
        self.data = tsag.preprocessing.PreprocessDatasets('prison').apply_preprocess()
        self.n = self.data['predict']['n']
        self.s = self.data['train']['s']
        self.gpf = GPF('prison', self.data)

    def test_calculate_metrics_dict(self):
        model, like = self.gpf.train(epochs=100)
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])
        self.assertLess(res['mase']['bottom'], 5)
