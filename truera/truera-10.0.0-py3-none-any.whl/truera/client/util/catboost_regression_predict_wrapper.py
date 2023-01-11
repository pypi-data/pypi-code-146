import catboost  # pylint: disable=import-error
import pandas as pd


class PredictWrapper(object):

    def __init__(self, model):
        self.model = model

    def predict(self, df):
        return self.model.predict(df)

    def get_model(self):
        return self.model


def _load_model_from_local_file(path):
    clf = catboost.CatBoostRegressor()
    clf.load_model(path, "cbm")
    return PredictWrapper(clf)


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
