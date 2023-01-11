# Ref: https://keras.io/examples/vision/mnist_convnet/
import os
from pathlib import Path

import PIL
import numpy as np
import numpy.typing as npt
from tensorflow import keras
from tensorflow.keras import layers
from typing import Any, Dict, Tuple, Union

from cinnaroll_internal.rollout_config import RolloutConfig
from cinnaroll_internal.rollout import rollout

NUM_CLASSES = 10
INPUT_SHAPE = (28, 28, 1)


def load_data(
    num_classes: int, limit: int
) -> Dict[str, Dict[str, npt.NDArray[np.float64]]]:
    # Load the data and split it between train and test sets
    data_array = keras.datasets.mnist.load_data()

    if limit is not None:
        tmp = data_array

        data_array = [[None] * 2, [None] * 2]
        for j in range(2):
            for k in range(2):
                data_array[j][k] = tmp[j][k][:limit]

    all_data = {
        "test": {"X": data_array[1][0], "Y": data_array[1][1]},
        "train": {"X": data_array[0][0], "Y": data_array[0][1]},
    }

    print("\nDataset info:")

    for key, val in all_data.items():
        print(f"Number of samples in {key} set: {val['X'].shape[0]}")
        # the range of each pixel should be a float in [0, 1] interval
        val["X"] = val["X"].astype("float32") / 255
        # every image should have shape (28, 28, 1)
        val["X"] = np.expand_dims(val["X"], -1)  # type: ignore
        # convert numerical labels to one-hot encodings
        val["Y"] = keras.utils.to_categorical(val["Y"], num_classes)

    return all_data


def construct_model(num_classes: int, input_shape: Tuple[int, int, int]) -> Any:
    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )

    # print model summary
    print("\nModel info:")
    model.summary()

    # compile model
    model.compile(
        loss=keras.losses.CategoricalCrossentropy(),
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        metrics=["accuracy"],
    )

    return model


def preprocess_image(input_data: str) -> npt.NDArray[np.float64]:
    img = PIL.Image.open(input_data)
    img_processed = img.convert("L").resize(INPUT_SHAPE[:2])
    img_array = np.array(img_processed).reshape((1,) + INPUT_SHAPE)
    return img_array


def make_prediction(x: npt.NDArray[np.float64]) -> int:
    return int(np.argmax(x))


class MyRolloutConfig(RolloutConfig):
    @staticmethod
    def train_eval(
        model_object: Any,
    ) -> Dict[str, Union[str, float]]:  # training and evaluation with metric extraction
        all_data = load_data(num_classes=NUM_CLASSES, limit=100)
        X = all_data["train"]["X"]
        Y = all_data["train"]["Y"]

        model_object.fit(X, Y, epochs=5)
        X_test = all_data["test"]["X"]
        Y_test = all_data["test"]["Y"]
        loss, accuracy = model_object.evaluate(X_test, Y_test)

        metrics = {"dataset": "MNIST", "loss": loss, "accuracy": accuracy}
        return metrics

    @staticmethod
    def infer(
        model_object: Any, input_data: str
    ) -> Dict[str, int]:  # input -> processing -> inference -> output
        img_array = preprocess_image(input_data)
        out = model_object.predict(img_array)
        return {"output": make_prediction(out)}


if __name__ == "__main__":
    if 'PROJECT_ID' in os.environ:
        project_id = os.environ['PROJECT_ID']
    else:
        project_id = "8ed8a20a-5f4e-46aa-ae71-dfbea78cf6b1"

    # define the number of classes and expected input shape
    all_data = load_data(num_classes=NUM_CLASSES, limit=100)
    model_object = construct_model(num_classes=NUM_CLASSES, input_shape=INPUT_SHAPE)

    model_input_sample = all_data["test"]["X"][0, :, :, :].reshape(1, 28, 28, 1)
    infer_func_input_sample = str(Path(__file__).parent / "test_image.png")

    myRolloutConfig = MyRolloutConfig(
        project_id=project_id,  # project's unique identifier
        model_name="mnist keras model",
        model_object=model_object,
        model_input_sample=model_input_sample,  # sample you can pass to model object's predict function
        infer_func_input_format="file",  # "json", "img" or "file"
        infer_func_output_format="json",  # "json" or "img" currently supported
        infer_func_input_sample=infer_func_input_sample,  # note - for file or img just pass file path
    )

    rollout(myRolloutConfig)
