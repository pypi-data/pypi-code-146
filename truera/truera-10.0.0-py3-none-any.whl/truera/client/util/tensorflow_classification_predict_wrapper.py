import pickle

import numpy as np
import pandas as pd
from tensorflow import keras  # pylint: disable=import-error
import tensorflow as tf  # pylint: disable=import-error


class PredictProbaWrapper(object):

    def __init__(self, model):
        self.model = model

    def predict(self, df):
        predictions = self.model.predict(df, batch_size=len(df))
        prob_1 = tf.sigmoid(predictions)
        probs = np.hstack([1.0 - prob_1, prob_1])
        return pd.DataFrame(probs, columns=[0, 1])


def _load_model_from_local_file(path):
    return PredictProbaWrapper(tf.keras.models.load_model(path))


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
