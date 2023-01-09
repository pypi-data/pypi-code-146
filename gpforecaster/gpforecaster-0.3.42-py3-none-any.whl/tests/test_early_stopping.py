import unittest
from gpforecaster.model.gpf import GPF
import tsaugmentation as tsag
import timeit


class TestModel(unittest.TestCase):
    def setUp(self):
        self.data = tsag.preprocessing.PreprocessDatasets("prison").apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]
        self.gpf = GPF("prison", self.data, log_dir="..")

    def test_early_stopping_fn(self):
        self.gpf.val_losses = [5.1, 5.2, 4.9, 5.0, 5.1, 5.2]
        res = self.gpf.early_stopping(2)
        self.assertTrue(res)

    def test_early_stopping_w_patience(self):
        model, like = self.gpf.train(epochs=200, patience=4, track_mem=True)
        self.gpf.plot_losses(5)
        self.assertLess(len(self.gpf.losses), 180)

    def test_compare_execution_times(self):
        n_iter = 100
        elapsed_time_es = timeit.timeit(
            lambda: self.gpf.train(epochs=n_iter, verbose=False), number=1
        )
        print(f"Elapsed time with Early Stopping: {elapsed_time_es} seconds")
        elapsed_time = timeit.timeit(
            lambda: self.gpf.train(epochs=n_iter, early_stopping=False, verbose=False),
            number=1,
        )
        print(f"Elapsed time: {elapsed_time} seconds")

    def test_without_early_stopping(self):
        model, like = self.gpf.train(epochs=500, early_stopping=False, track_mem=True)
        self.assertEqual(len(self.gpf.losses), 500)
