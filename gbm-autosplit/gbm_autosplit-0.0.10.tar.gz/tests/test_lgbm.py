import unittest

from sklearn import base

from gbm_autosplit import lgbm
from . import utils


class TestLGBM(unittest.TestCase):
    def test_basic_flow_cl(self):
        x, y = utils.get_xy(100, True)
        model = lgbm.LGBMClassifier()
        model.fit(x, y)
        self.assertGreater(5000, model.booster_.num_trees())

    def test_basic_flow_rg(self):
        x, y = utils.get_xy(100, False)
        model = lgbm.LGBMRegressor()
        model.fit(x, y)
        self.assertGreater(5000, model.booster_.num_trees())

    def test_instance_attribute_cl(self):
        model = lgbm.LGBMClassifier()
        instance_attribute_keys = model.__dict__.keys()
        get_params_keys = model.get_params().keys()
        self.assertSetEqual(set(get_params_keys) - set(instance_attribute_keys), set([]))

    def test_instance_attribute_rg(self):
        model = lgbm.LGBMRegressor()
        instance_attribute_keys = model.__dict__.keys()
        get_params_keys = model.get_params().keys()
        self.assertSetEqual(set(get_params_keys) - set(instance_attribute_keys), set([]))

    def test_clone_cl(self):
        model = lgbm.LGBMClassifier()
        base.clone(model)

    def test_clone_rg(self):
        model = lgbm.LGBMRegressor()
        base.clone(model)
