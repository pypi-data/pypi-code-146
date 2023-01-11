import catboost  # pylint: disable=import-error
import pandas as pd


class PredictProbaWrapper(object):

    def __init__(self, model):
        self.model = model

    def predict(self, df):
        return pd.DataFrame(
            self.model.predict_proba(df), columns=self.model.classes_
        )

    def get_model(self):
        return self.model


def _load_model_from_local_file(path):
    clf = catboost.CatBoostClassifier()
    clf.load_model(path, "cbm")
    return PredictProbaWrapper(clf)


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
