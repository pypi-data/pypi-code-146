"""Class that uses prediction/correction models on device designs.
"""

import os
import numpy as np
import tensorflow as tf
from keras import models
from google.cloud import aiplatform
from prefab.processor import binarize

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


class Predictor():
    """Class that uses prediction/correction models on device designs.
    """
    def __init__(self, model_type, model_name, model_nums, compute='local'):
        self.model_type = model_type
        self.model_name = model_name
        self.model_nums = model_nums
        self.compute = compute

        os.path.abspath(__file__)

        if compute == 'local':
            self.models = []
            for model_num in self.model_nums:
                model_path = ROOT_DIR + '/models/' + model_name + '/' + \
                    model_type + '_' + model_name + '_' + str(model_num) + \
                    '.pb'
                self.models.append(models.load_model(model_path))
            self.slice_length = int(np.sqrt(self.models[0].weights[-1].shape)
                                    [0])
            self.slice_size = (self.slice_length, self.slice_length)
        elif compute == 'cloud':
            aiplatform.init(project="407811038010", location="us-central1")
            self.endpoint = aiplatform.Endpoint("7418435738930249728")
            self.slice_length = 128
            self.slice_size = (self.slice_length, self.slice_length)

    def predict(self, device, step_length, binary=False):
        # pylint: disable=R0914
        """Make a prediction/correction of a device.
        """
        # slice image up
        x_slices_4d = np.lib.stride_tricks.sliding_window_view(device,
                                                               self.slice_size)
        x_slices_4d = x_slices_4d[::step_length, ::step_length]
        x_slices = x_slices_4d.reshape(-1, *self.slice_size)
        x_slices = tf.reshape(x_slices, [len(x_slices), self.slice_length,
                                         self.slice_length, 1])

        # inferencing
        if self.compute == 'local':
            y_slices = self.infer_local(inputs=x_slices)
        elif self.compute == 'cloud':
            y_slices = self.infer_cloud(inputs=x_slices)
        y_slices = np.squeeze(y_slices).reshape(x_slices_4d.shape)

        # stitch slices back together (needs a better method)
        y_full = np.zeros(device.shape)
        avg_mtx = np.zeros(device.shape)
        y_range = range(0, device.shape[0]-self.slice_length+1, step_length)
        x_range = range(0, device.shape[1]-self.slice_length+1, step_length)
        for k in y_range:
            for j in x_range:
                y_full[k:k+self.slice_length, j:j+self.slice_length] += \
                    y_slices[k//step_length, j//step_length]
                avg_mtx[k:k+self.slice_length, j:j+self.slice_length] += \
                    np.ones(self.slice_size)
        prediction = y_full/avg_mtx

        # binarize or leave as raw (showing uncertainty)
        if binary:
            prediction = binarize(prediction)

        return prediction

    def infer_local(self, inputs):
        """Make single batch inference through local model(s).
        """
        y_sum = 0
        for model in self.models:
            y_slice = model(inputs)
            y_slice = tf.cast(y_slice, tf.float64)
            y_sum += y_slice
        y_slices = y_sum/len(self.models)
        return y_slices

    def infer_cloud(self, inputs):
        """Make single batch inference through single cloud model.
        """
        inputs = inputs.numpy().tolist()
        return self.endpoint.predict(instances=inputs).predictions
