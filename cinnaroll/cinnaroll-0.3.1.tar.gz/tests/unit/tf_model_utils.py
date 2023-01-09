# including keras models
from typing import Tuple, Optional, Dict, Any

import numpy as np
import numpy.typing as npt
import tensorflow as tf
from tensorflow.keras.layers import Dense


class MyDense(tf.Module):  # type: ignore
    """A dense unit initialised with randomised weights and ReLU activation function."""

    def __init__(self, input_dim: int, output_size: int, name: Optional[str] = None):
        super().__init__(name=name)
        self.w = tf.Variable(
            tf.random.normal([input_dim, output_size], dtype=tf.dtypes.float64),
            name=f"{name}.w",
        )
        self.b = tf.Variable(
            tf.random.normal([output_size], dtype=tf.dtypes.float64), name=f"{name}.b"
        )

    def __call__(self, x: tf.Tensor) -> tf.Tensor:
        y = tf.matmul(x, self.w) + self.b
        return tf.nn.relu(y)


class TensorFlowSimpleModel(tf.Module):  # type: ignore
    def __init__(
        self, input_dim: int, dense_layers: Tuple[int, int], name: Optional[str] = None
    ):
        super().__init__(name=name)
        self.dense_1 = MyDense(input_dim, dense_layers[0], name="layer1")
        self.dense_2 = MyDense(dense_layers[0], dense_layers[1], name="layer2")

    @tf.function  # type: ignore
    def __call__(self, x: tf.Tensor) -> tf.Tensor:
        x = tf.nn.relu(self.dense_1(x))
        return self.dense_2(x)

    @staticmethod
    def _MSEloss(y: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
        return tf.reduce_mean(tf.square(y - y_pred))

    def perform_training(
        self,
        X: npt.NDArray[np.float64],
        Y: npt.NDArray[np.float64],
        num_epochs: int = 10,
        learning_rate: float = 1e-3,
    ) -> None:
        for epoch in range(num_epochs):
            with tf.GradientTape(persistent=True) as t:
                current_loss = self._MSEloss(self(X), Y)

            print(f"Epoch {epoch + 1}, loss: {current_loss}")

            for layer in (self.dense_1, self.dense_2):
                for x in ("w", "b"):
                    attr = getattr(layer, x)
                    grad = t.gradient(current_loss, attr)
                    attr.assign_sub(learning_rate * grad)


def create_keras_model_object(
    input_dim: int,
    dense_layers: Tuple[int, int],
    weights: Optional[Dict[str, npt.NDArray[np.float64]]] = None,
) -> Any:
    model_object = tf.keras.models.Sequential(
        [
            Dense(dense_layers[0], input_shape=(input_dim,), activation="relu"),
            Dense(dense_layers[1], activation=None),
        ]
    )
    model_object.compile(
        loss=tf.keras.losses.MeanSquaredError(),
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    )

    if weights is not None:
        for j in range(2):
            model_object.layers[j].set_weights(
                [weights[f"lay{j+1}.w"], weights[f"lay{j+1}.b"]]
            )
    return model_object


def create_tensorflow_model_object(
    input_dim: int,
    dense_layers: Tuple[int, int],
    weights: Optional[Dict[str, npt.NDArray[np.float64]]] = None,
) -> Any:

    model_object = TensorFlowSimpleModel(input_dim, dense_layers)

    if weights is not None:
        for j in range(1, 3):
            for var in ("w", "b"):
                setattr(
                    getattr(model_object, f"dense_{j}"),
                    var,
                    weights[f"lay{j}.{var}"],
                )
    return model_object
