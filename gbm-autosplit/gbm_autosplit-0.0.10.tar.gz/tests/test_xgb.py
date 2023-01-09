import unittest

from sklearn import base

from gbm_autosplit import xgb
from . import utils


class TestXGB(unittest.TestCase):
    def test_basic_flow_cl(self):
        x, y = utils.get_xy(100, True)
        model = xgb.XGBClassifier()
        model.fit(x, y)
        model.predict(x)
        self.assertGreater(5000, model.get_num_boosting_rounds())

    def test_basic_flow_rg(self):
        x, y = utils.get_xy(100, False)
        model = xgb.XGBRegressor()
        model.fit(x, y)
        model.predict(x)
        self.assertGreater(5000, model.get_num_boosting_rounds())

    def test_instance_attribute_cl(self):
        model = xgb.XGBClassifier()
        instance_attribute_keys = model.__dict__.keys()
        get_params_keys = model.get_params().keys()
        self.assertSetEqual(set(get_params_keys) - set(instance_attribute_keys), set([]))

    def test_instance_attribute_rg(self):
        model = xgb.XGBRegressor()
        instance_attribute_keys = model.__dict__.keys()
        get_params_keys = model.get_params().keys()
        self.assertSetEqual(set(get_params_keys) - set(instance_attribute_keys), set([]))

    def test_clone_cl(self):
        model = xgb.XGBClassifier()
        base.clone(model)

    def test_clone_rg(self):
        model = xgb.XGBRegressor()
        base.clone(model)
