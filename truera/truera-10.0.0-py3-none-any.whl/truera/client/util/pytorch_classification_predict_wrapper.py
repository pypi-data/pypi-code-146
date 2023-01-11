import cloudpickle
import numpy as np
import pandas as pd
import torch  # pylint: disable=import-error


class PredictProbaWrapper(object):

    def __init__(self, model):
        self.model = model

    def predict(self, df):
        predictions = self.model(torch.FloatTensor(np.array(df)))
        prob_1 = torch.sigmoid(predictions).detach().numpy()
        probs = np.hstack([1.0 - prob_1, prob_1])
        return pd.DataFrame(probs, columns=[0, 1])


def _load_model_from_local_file(path):
    with open(path, "rb") as f:
        return PredictProbaWrapper(cloudpickle.load(f))


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
