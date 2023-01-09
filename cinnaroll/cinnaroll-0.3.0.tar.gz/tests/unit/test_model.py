from pathlib import Path

import pytest

from typing import Any, Optional, Tuple, Dict

import numpy as np
import numpy.typing as npt
import tensorflow as tf
import torch

from cinnaroll_internal.constants import (
    KERAS,
    PYTORCH,
    TENSORFLOW,
    VALID_FRAMEWORKS,
)
from cinnaroll_internal.model import (
    create_model,
    ModelInputSampleError,
)
from cinnaroll_internal.utils import clean_path

from tests.unit.tf_model_utils import (
    create_keras_model_object,
    create_tensorflow_model_object,
)
from tests.unit.pytorch_model_utils import create_pytorch_model_object
from tests.unit.model_utils import generate_random_data


def create_model_object(
    framework: str,
    input_dim: int,
    dense_layers: Tuple[int, int],
    weights: Optional[Dict[str, npt.NDArray[np.float64]]] = None,
) -> Any:
    """Create a dense neural network model_object. Optionally set weights of the newly created model."""
    assert framework in VALID_FRAMEWORKS
    if framework == KERAS:
        return create_keras_model_object(input_dim, dense_layers, weights)

    elif framework == TENSORFLOW:
        return create_tensorflow_model_object(input_dim, dense_layers, weights)

    elif framework == PYTORCH:
        return create_pytorch_model_object(input_dim, dense_layers, weights)


def check_model_object(framework: str, model_object: Any, input_dim: int) -> None:
    """Check that model_object can be trained and can executed to make predictions."""
    assert framework in VALID_FRAMEWORKS

    num_samples = np.random.randint(10, 20)
    num_epochs = np.random.randint(10, 20)

    X, Y = generate_random_data(num_samples, input_dim)

    print("\n-- training")
    if framework == KERAS:
        model_object.fit(X, Y, epochs=num_epochs)
    elif framework == TENSORFLOW:
        model_object.perform_training(X, Y, num_epochs=num_epochs)
    elif framework == PYTORCH:
        model_object.perform_training(torch.Tensor(X), torch.Tensor(Y), num_epochs=10)

    print("\n-- making predictions")
    if framework == KERAS:
        print(model_object.predict(X))
    elif framework == TENSORFLOW:
        print(model_object(X))
    elif framework == PYTORCH:
        print(model_object.forward(torch.Tensor(X)))


class TestModel:
    @pytest.mark.parametrize("framework", VALID_FRAMEWORKS)
    def test_model_object_creation(self, framework: str) -> None:
        """Test creating model_objects in all the frameworks and check their validity."""
        num_features = np.random.randint(5, 15)
        dense_layers = (np.random.randint(3, 10), 1)

        print(f"\nChecking {framework} model_object")
        model_object = create_model_object(
            framework, input_dim=num_features, dense_layers=dense_layers
        )
        check_model_object(framework, model_object, num_features)

    @pytest.mark.parametrize("framework", VALID_FRAMEWORKS)
    def test_cinnaroll_model_should_be_loaded(self, framework: str) -> None:
        cache_dir = Path(__file__).parent / "tmp"
        clean_path(cache_dir, True)
        model_save_path = cache_dir / "saved_model"

        num_features = np.random.randint(5, 15)
        dense_layers = (np.random.randint(3, 10), 1)

        print(f"\nTesting framework: {framework}")
        clean_path(model_save_path)
        model_object = create_model_object(
            framework, input_dim=num_features, dense_layers=dense_layers
        )

        print("Create a fresh model_object and save it")

        if framework == KERAS:
            model_object.save(model_save_path)
        elif framework == TENSORFLOW:
            tf.saved_model.save(
                model_object,
                model_save_path,
                signatures=model_object.__call__.get_concrete_function(
                    tf.TensorSpec([None, num_features], tf.float64)
                ),
            )
        elif framework == PYTORCH:
            model_scripted = torch.jit.script(model_object)
            model_scripted.save(model_save_path)

        cinnaroll_model = create_model(model_object, framework, model_save_path)

        print(f"Should be loaded? {cinnaroll_model.should_be_loaded()}")
        assert (
            cinnaroll_model.should_be_loaded()
        ), "Saved model is compatible and should be loaded, but should_be_loaded() returned False."

        clean_path(model_save_path)

        print("Create a different model_object without saving")
        model_object = create_model_object(
            framework, input_dim=num_features + 1, dense_layers=dense_layers
        )
        cinnaroll_model = create_model(model_object, framework, model_save_path)
        print(f"Should be loaded? {cinnaroll_model.should_be_loaded()}")
        assert (
            not cinnaroll_model.should_be_loaded()
        ), "Saved model is not compatible and should not be loaded, but should_be_loaded() returned True."

    @pytest.mark.parametrize("framework", VALID_FRAMEWORKS)
    @pytest.mark.parametrize(
        "extra_features,expectation",
        [(0, None), (1, ModelInputSampleError)],
    )
    def test_cinnaroll_model_find_model_input_sample_error(
        self, framework: str, extra_features: int, expectation: Any
    ) -> None:
        cache_dir = Path(__file__).parent / "tmp"
        clean_path(cache_dir, True)
        model_save_path = cache_dir / "saved_model"

        num_features = np.random.randint(5, 15)
        dense_layers = (np.random.randint(3, 10), 1)

        X0 = generate_random_data(
            np.random.randint(3, 10), num_features + extra_features
        )[0]

        if framework == PYTORCH:
            X = torch.Tensor(X0)
        else:
            X = X0

        print(f"\nTesting framework: {framework}")
        print("Create a fresh model_object")
        model_object = create_model_object(
            framework, input_dim=num_features, dense_layers=dense_layers
        )

        cinnaroll_model = create_model(model_object, framework, model_save_path)

        out = cinnaroll_model.find_model_input_sample_error(X)

        if expectation is None:
            assert out is None
        else:
            assert isinstance(out, expectation)

    @pytest.mark.parametrize("framework", VALID_FRAMEWORKS)
    def test_cinnaroll_save_load(self, framework: str) -> None:
        """Generate a random simple NN model and save it. Then, load it and check that predictions on random data are consistent."""
        cache_dir = Path(__file__).parent / "tmp"
        clean_path(cache_dir, True)
        model_save_path = cache_dir / "saved_model"

        # generate random model parameters
        num_features = np.random.randint(5, 15)
        dense_layers = (np.random.randint(3, 10), 1)

        # generate random input
        num_samples = np.random.randint(10, 20)
        X = np.random.rand(num_samples, num_features)

        print(f"\nTesting framework: {framework}")
        model_object = create_model_object(
            framework, input_dim=num_features, dense_layers=dense_layers
        )
        cinnaroll_model = create_model(model_object, framework, model_save_path)
        cinnaroll_model.save()

        if framework == KERAS:
            Y = model_object.predict(X).reshape(-1)
        elif framework == TENSORFLOW:
            Y = model_object(X).numpy().reshape(-1)
        elif framework == PYTORCH:
            with torch.no_grad():
                Y = model_object(torch.Tensor(X)).numpy()

        new_cinnaroll_model = create_model(None, framework, model_save_path)
        new_cinnaroll_model.load()
        clean_path(model_save_path)

        if framework == KERAS:
            Y2 = model_object.predict(X).reshape(-1)
        elif framework == TENSORFLOW:
            Y2 = model_object(X).numpy().reshape(-1)
        elif framework == PYTORCH:
            with torch.no_grad():
                Y2 = model_object(torch.Tensor(X)).numpy()

        # verify that the results are the same
        np.testing.assert_allclose(Y, Y2, rtol=1e-6)  # type: ignore
