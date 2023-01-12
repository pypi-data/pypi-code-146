import numpy as np
import tensorflow as tf
from PIL import Image

from .tools import ModelNotImplementedError, open_img


def preprocess(image: object) -> object:
    """preprocess.

    :param image:
    :type image: object
    :rtype: object
    """
    return image


def decode(result: object, num: int) -> object:
    """decode.

    :param result:
    :type result: object
    :param num:
    :type num: int
    :rtype: object
    """
    return result


class Wrapper:
    """Wrapper. tensorflow wrapper"""

    def __init__(
        self,
        weight: str = None,
        model_type: str = "MobileNetV2",
        image_size: int = 300,
        model: object = None,
        preprocess: callable = preprocess,
        decode: callable = decode,
        num_class: int = 0,
        model_mod: str = "use",
    ) -> None:
        """__init__.

        :param weight: tensorflow weight
        :type weight: str
        :param model_type: model type, can be MobileNetV2, resnet50,densenet121,inceptionv3
        :type model_type: str
        :param image_size:
        :type image_size: int
        :param model:
        :type model: object
        :param preprocess:
        :type preprocess: callable
        :param decode:
        :type decode: callable
        :param num_class:
        :type num_class: int
        :param model_mod:
        :type model_mod: str
        :rtype: None
        """
        self.weight = weight
        self.model_type = model_type
        self.image_size = image_size
        self.preprocess = preprocess
        self.decode = decode
        self.num_class = num_class
        self.model_mod = model_mod
        if model is None:
            self._get_model(model_type)
        else:
            self.model = model

    def _get_model(self, model_type: str) -> object:
        """_get_model. get tensorflow model

        :param model_type:
        :type model_type: str
        :rtype: object
        """
        kwargs = {"input_shape": (self.image_size, self.image_size, 3)}
        if self.model_mod == "use":
            wargs = {"weights": self.weight}
        elif self.model_mod == "new":
            wargs = {
                "weights": None,
                "inculde_top": True,
                "classes": self.num_class,
                "pooling": "avg",
            }
        elif self.model_mod == "resume":
            wargs = {"weights": self.weight}
        elif self.model_mod == "add":
            wargs = {"weights": self.weight, "include_top": False, "pooling": "avg"}
        kwargs.update(wargs)
        if model_type.lower() == "MobileNetV2".lower():
            self.model = tf.keras.applications.MobileNetV2(**kwargs)
            self.preprocess = tf.keras.applications.mobilenet_v2.preprocess_input
            self.decode = tf.keras.applications.mobilenet_v2.decode_prediction
        elif model_type.lower() == "resnet50":
            self.model = tf.keras.applications.ResNet50(**kwargs)
            self.decode = tf.keras.applications.resnet50.decode_predictions
        elif model_type.lower() == "densenet121":
            self.model = tf.keras.applications.DenseNet121(**kwargs)
            self.preprocess = tf.keras.applications.densenet.preprocess_input
            self.decode = tf.keras.applications.inception_v3.decode_predictions
        elif model_type.lower() == "inceptionv3":
            self.model = tf.keras.applications.InceptionV3(**kwargs)
            self.preprocess = tf.keras.applications.inception_v3.preprocess_input
            self.decode = tf.keras.applications.densenet.decode_predictions
        else:
            raise ModelNotImplementedError
        return self.model

    def norm_input(self, image: object) -> np.ndarray:
        """norm_input. normalize input

        :param image:
        :type image: object
        :rtype: np.ndarray
        """
        to_predict = open_img(image)
        to_predict = to_predict.resize((self.image_size, self.image_size, 3))
        to_predict = np.expand_dims(to_predict, axis=0)
        to_predict = np.asarray(to_predict, dtype=np.float64)
        return to_predict
