import pickle

from PIL import Image

from .classifier_wrapper import Wrapper, decode, preprocess


class Classifier(Wrapper):
    """Classifier."""

    def __init__(
        self,
        weight: str = None,
        model_type: str = "MobileNetV2",
        image_size: int = 300,
        model: object = None,
        preprocess: callable = preprocess,
        decode: callable = decode,
        num_class: int = 0,
    ):
        """__init__.

        :param weight:
        :type weight: str
        :param model_type:
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
        """
        Wrapper.__init__(
            self,
            weight=weight,
            model_type=model_type,
            image_size=image_size,
            preprocess=preprocess,
            model=model,
            decode=decode,
            model_mod="use",
        )
        self.num_class = num_class

    def predict(self, image: object, num: int = 1) -> (str, float):
        """predict. predict image classe

        :param image:
        :type image: object
        :param num: number of result, if num==0, return a generator
        :type num: int
        :rtype: (str, float)
        """
        to_predict = self.norm_input(image)
        to_predict = self.preprocess(to_predict)
        res = self.model.predict(to_predict)

        if num == 0:
            res = self.decode(res, top=self.num_class)
            for name, desc, score in res[0]:
                yield name, score
        else:
            res = self.decode(res, top=num)
            if num == 1:
                return (res[0][0], res[0][1])
            else:
                return [(name, score) for name, desc, score in res[0]]

    def dump(self, file_handler) -> None:
        """dump.

        :param file_handler:
        :rtype: None
        """
        pickle.dump(self, file_handler)
