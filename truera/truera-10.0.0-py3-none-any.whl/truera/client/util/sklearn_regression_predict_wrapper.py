import cloudpickle


class PredictWrapper(object):

    def __init__(self, model):
        self.model = model

    def predict(self, df):
        return self.model.predict(df).ravel()

    def get_model(self):
        return self.model


def _load_model_from_local_file(path):
    with open(path, "rb") as f:
        return PredictWrapper(cloudpickle.load(f))


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
