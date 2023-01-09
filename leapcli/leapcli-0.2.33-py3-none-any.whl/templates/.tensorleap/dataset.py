'''
Integration script documentation: https://docs.tensorleap.ai/guides/integration-script
For more examples, see: https://docs.tensorleap.ai/guides/integration-script/examples
'''

'''
MNIST integration script: 
More info can be found at https://docs.tensorleap.ai/guides/full-guides/mnist-guide 
'''

from typing import List, Union

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# Tensorleap imports
from code_loader import leap_binder
from code_loader.contract.datasetclasses import PreprocessResponse
from code_loader.contract.enums import Metric, DatasetMetadataType


# Preprocess Function
def preprocess_func() -> List[PreprocessResponse]:
    (data_X, data_Y), (test_X, test_Y) = mnist.load_data()

    data_X = np.expand_dims(data_X, axis=-1)  # Reshape :,28,28 -> :,28,28,1
    data_X = data_X / 255  # Normalize to [0,1]
    data_Y = to_categorical(data_Y)  # Hot Vector

    test_X = np.expand_dims(test_X, axis=-1)  # Reshape :,28,28 -> :,28,28,1
    test_X = test_X / 255  # Normalize to [0,1]
    test_Y = to_categorical(test_Y)  # Hot Vector

    train_X, val_X, train_Y, val_Y = train_test_split(data_X, data_Y, test_size=0.2, random_state=42)

    # Generate a PreprocessResponse for each data slice, to later be read by the encoders.
    # The length of each data slice is provided, along with the data dictionary.
    # In this example we pass `images` and `labels` that later are encoded into the inputs and outputs
    train = PreprocessResponse(length=len(train_X), data={'images': train_X, 'labels': train_Y})
    val = PreprocessResponse(length=len(val_X), data={'images': val_X, 'labels': val_Y})
    test = PreprocessResponse(length=len(test_X), data={'images': test_X, 'labels': test_Y})

    response = [train, val, test]
    return response


# Input encoder fetches the image with the index `idx` from the `images` array set in
# the PreprocessResponse data. Returns a numpy array containing the sample's image.
def input_encoder(idx: int, preprocess: PreprocessResponse) -> np.ndarray:
    return preprocess.data['images'][idx].astype('float32')


# Ground truth encoder fetches the label with the index `idx` from the `labels` array set in
# the PreprocessResponse's data. Returns a numpy array containing a hot vector label correlated with the sample.
def gt_encoder(idx: int, preprocessing: Union[PreprocessResponse, list]) -> np.ndarray:
    return preprocessing.data['labels'][idx].astype('float32')


# Metadata functions allow to add extra data for a later use in analysis.
# This metadata adds the int digit of each sample (not a hot vector).
def metadata_label(idx: int, preprocess: Union[PreprocessResponse, list]) -> int:
    one_hot_digit = gt_encoder(idx, preprocess)
    digit = one_hot_digit.argmax()
    digit_int = int(digit)
    return digit_int


LABELS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# Dataset binding functions to bind the functions above to the `Dataset Instance`.
leap_binder.set_preprocess(function=preprocess_func)
leap_binder.set_input(function=input_encoder, name='image')
leap_binder.set_ground_truth(function=gt_encoder, name='classes')
leap_binder.set_metadata(function=metadata_label, metadata_type=DatasetMetadataType.int, name='label')
leap_binder.add_prediction(name='classes', labels=LABELS, metrics=[Metric.Accuracy])
