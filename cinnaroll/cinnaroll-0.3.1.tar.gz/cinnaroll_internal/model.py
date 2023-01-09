import abc
import importlib
from pathlib import Path
from typing import Any, Callable, Dict, Tuple, Optional

from cinnaroll_internal import utils
from cinnaroll_internal.constants import (
    KERAS,
    KERAS_PACKAGE_NAME,
    TENSORFLOW,
    TENSORFLOW_PACKAGE_NAME,
    PYTORCH,
    PYTORCH_PACKAGE_NAME,
    UNKNOWN_FRAMEWORK,
)


class ModelLoadingError(Exception):
    ...


class ModelSavingError(Exception):
    ...


class ModelInputSampleError(Exception):
    ...


# container for framework-specific logic for saving and loading model and for running model's prediction method
class CinnarollModel(abc.ABC):
    def __init__(self, model_object: Any, framework_package_name: str, model_save_path: Path):
        self.model_object = model_object
        self.framework_package = importlib.import_module(framework_package_name)
        self.model_save_path = model_save_path

    @abc.abstractmethod
    def save(self) -> None:
        """
        throws a ModelSavingError if something fails
        """
        pass

    @abc.abstractmethod
    def load(self) -> None:
        """
        throws a ModelLoadingError if something fails
        """

    @abc.abstractmethod
    def find_model_input_sample_error(self, input_sample: Any) -> Optional[Exception]:
        """
        test if passing model_input_sample to model_object's prediction function
        (eg. model_object.predict(input) in Keras or model_object(input) in PyTorch
        doesn't raise any errors
        return if everything is ok, raise ModelInputSampleError otherwise
        """
        pass

    @abc.abstractmethod
    def get_metadata(self) -> Any:
        pass

    @abc.abstractmethod
    def is_equal_to_cached(self) -> bool:
        """when both of these are true:
        1. there’s a saved model on disk
        2. saved model’s metadata are the same as model_object’s
        """
        pass


# https://www.tensorflow.org/guide/keras/save_and_serialize
class CinnarollKerasModel(CinnarollModel):
    def save(self) -> None:
        try:
            self.model_object.save(self.model_save_path)
        except Exception as e:
            raise ModelSavingError(f"Could not save model: {repr(e)}")

    def load(self) -> None:
        try:
            self.model_object = self.framework_package.keras.models.load_model(
                self.model_save_path
            )
        except Exception as e:
            raise ModelLoadingError(f"Could not load model: {repr(e)}")

    def find_model_input_sample_error(self, input_sample: Any) -> Optional[Exception]:
        try:
            self.model_object.predict(input_sample, verbose=2)
        except ValueError as e:
            return ModelInputSampleError(
                f"Provided input_sample is not a valid input to the model.\n{repr(e)}"
            )

        return None

    def is_equal_to_cached(self) -> bool:
        if self.model_save_path.exists():
            try:
                saved_model = self.framework_package.keras.models.load_model(
                    self.model_save_path
                )
            except Exception as e:
                raise ModelLoadingError(
                    f"Error occurred while trying to load model from {self.model_save_path}: {repr(e)}"
                )
            return bool(saved_model.to_json() == self.model_object.to_json())
        else:
            return False

    def get_metadata(self) -> Any:
        pass


# https://www.tensorflow.org/guide/saved_model
class CinnarollTensorflowModel(CinnarollModel):
    def save(self) -> None:
        try:
            self.framework_package.saved_model.save(
                self.model_object,
                self.model_save_path,
                signatures=self.model_object.__call__.get_concrete_function(
                    self.framework_package.TensorSpec(
                        None, self.framework_package.float64
                    )
                ),
            )
        except Exception as e:
            raise ModelSavingError(f"Could not save model: {repr(e)}")

    def load(self) -> None:
        try:
            self.model_object = self.framework_package.saved_model.load(self.model_save_path)
        except Exception as e:
            raise ModelLoadingError(f"Could not load model: {repr(e)}")

    def find_model_input_sample_error(self, input_sample: Any) -> Optional[Exception]:
        try:
            self.model_object(input_sample)
        except ValueError as e:
            return ModelInputSampleError(
                f"Provided input_sample is not a valid input to the model.\n{repr(e)}"
            )

        return None

    def is_equal_to_cached(self) -> bool:
        def _model_to_dict(model_object: Any) -> Dict[str, Tuple[Any, Any]]:
            """Converts a model into a dictionary where keys are labels of layers and values contain shape and type."""
            return {x.name: (x.shape, x.dtype) for x in model_object.variables}

        if self.model_save_path.exists():
            try:
                saved_model = self.framework_package.saved_model.load(self.model_save_path)
            except Exception as e:
                raise ModelLoadingError(
                    f"Error occurred while trying to load model from {self.model_save_path}: {repr(e)}"
                )
            return _model_to_dict(
                saved_model.signatures["serving_default"]
            ) == _model_to_dict(self.model_object)
        else:
            return False

    def get_metadata(self) -> Any:
        pass


# https://pytorch.org/tutorials/beginner/saving_loading_models.html
class CinnarollPyTorchModel(CinnarollModel):
    def save(self) -> None:
        try:
            model_scripted = self.framework_package.jit.script(self.model_object)
            model_scripted.save(self.model_save_path)
        except Exception as e:
            raise ModelSavingError(f"Could not save model: {repr(e)}")

    def load(self) -> None:
        try:
            self.model_object = self.framework_package.jit.load(self.model_save_path)
            self.model_object.eval()
        except Exception as e:
            raise ModelLoadingError(f"Could not load model: {repr(e)}")

    def find_model_input_sample_error(self, input_sample: Any) -> Optional[Exception]:
        try:
            self.model_object(input_sample)
        except RuntimeError as e:
            return ModelInputSampleError(
                f"Provided input_sample is not a valid input to the model.\n{repr(e)}"
            )

        return None

    def is_equal_to_cached(self) -> bool:
        def _model_to_dict(model_object: Any) -> Dict[str, Any]:
            """Converts a model into a dictionary where keys are labels of layers and values are shapes."""
            return {k: v.size() for k, v in model_object.state_dict().items()}

        if self.model_save_path.exists():
            try:
                saved_model = self.framework_package.jit.load(self.model_save_path)
                saved_model.eval()
            except Exception as e:
                raise ModelLoadingError(
                    f"Error occurred while trying to load model from {self.model_save_path}: {repr(e)}"
                )
            return _model_to_dict(saved_model) == _model_to_dict(self.model_object)
        else:
            return False

    def get_metadata(self) -> Any:
        pass


# when train func contains actual code and not just pass or ...
def is_trained_in_script(train_func: Callable[[Any], Optional[Dict[str, Any]]]) -> bool:
    return utils.is_function_implemented(train_func)


# todo: unit test
def infer_framework(model_object: Any) -> str:
    def find_framework_in_class_hierarchy(cls: type) -> Optional[str]:
        if cls is object:
            return None
        if KERAS in cls.__module__:  # tf.Keras.Model or subclass
            return KERAS
        elif TENSORFLOW in cls.__module__:  # tensorflow.Module or subclass
            return TENSORFLOW
        elif PYTORCH_PACKAGE_NAME in cls.__module__:  # subclass of torch.nn.Module
            return PYTORCH
        base_classes = cls.__bases__
        for base_class in base_classes:
            _framework = find_framework_in_class_hierarchy(base_class)
            if _framework:
                return _framework
        return None

    framework = find_framework_in_class_hierarchy(model_object.__class__)
    return framework if framework else UNKNOWN_FRAMEWORK


def create_model(model_object: Any, framework: str, model_save_path: Path) -> CinnarollModel:
    if framework == KERAS:
        return CinnarollKerasModel(model_object, KERAS_PACKAGE_NAME, model_save_path)
    elif framework == TENSORFLOW:
        return CinnarollTensorflowModel(
            model_object, TENSORFLOW_PACKAGE_NAME, model_save_path
        )
    elif framework == PYTORCH:
        return CinnarollPyTorchModel(
            model_object, PYTORCH_PACKAGE_NAME, model_save_path
        )
    else:
        raise NotImplementedError("Unknown machine learning library used.")
