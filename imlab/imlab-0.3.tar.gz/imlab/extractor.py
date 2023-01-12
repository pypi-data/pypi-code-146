import pickle

import torch

from .extractor_wrapper import Wrapper, decode, preprocess


class Extractor(Wrapper):
    """Extractor. Class to detect entities from picture"""

    def __init__(
        self,
        weight: str = None,
        model_type: str = "yoloV7",
        image_size: int = 640,
        model: object = None,
        preprocess: callable = preprocess,
        decode: callable = decode,
        classes: list = [],
    ) -> None:
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
        :param classes:
        :type classes: list
        :rtype: None
        """
        Wrapper.__init__(
            self,
            weight=weight,
            model_type=model_type,
            image_size=image_size,
            preprocess=preprocess,
            decode=decode,
            model_mod="use",
            model=model,
            classes=classes,
        )

    def predict(self, images: object | list, num: int = 1) -> list[tuple]:
        """predict. find entities from entities

        :param images:
        :type images: object | list
        :param num: number of result per bouding box
        :type num: int
        :rtype: list[tuple]
        """
        if not isinstance(images, list):
            images = [images]
            return_notlist = True
        else:
            return_notlist = False
        boxclas = []
        for image in images:
            img_size = self.open_img(image).shape
            to_predict = self.norm_input(image)
            to_predict = self.preprocess(to_predict)
            predict_size = to_predict.shape
            gain, pad = self.get_ratio(img_size[:2], predict_size[2:])
            res = self.model(to_predict)

            res = self.decode(res)
            box_cla = []
            for i, (boxes, classes) in enumerate(res):
                if len(boxes) > 0:
                    boxes = self.rescale(boxes, gain, pad, img_size)
                    boxcla = []
                    for j, box in enumerate(boxes):
                        score, index = classes[j]
                        cla = [
                            (float(score[k]), self.classes[int(index[k])])
                            for k in range(len(score))
                        ][:num]
                        if num == 1:
                            cla = cla[0]
                        boxcla += [
                            (
                                box.tolist(),
                                cla,
                            )
                        ]

                    box_cla += [boxcla]
            boxclas += [box_cla]
        if len(images) == 1 and return_notlist is True:
            boxclas = boxclas[0]

        return boxcla

    def dump(self, file_handler: object) -> None:
        """dump. dump the model

        :param file_handler:
        :type file_handler: object
        :rtype: None
        """
        pickle.dump(self, file_handler)

    def get_ratio(self, img1: (int, int), img2: (int, int)) -> (float, (float, float)):
        """get_ratio.

        :param img1:
        :type img1: (int, int)
        :param img2:
        :type img2: (int, int)
        :rtype: (float, (float, float))
        """
        gain = min(img2[0] / img1[0], img2[1] / img1[1])
        pad = (img2[1] - img1[1] * gain) / 2, (img2[0] - img1[0] * gain) / 2
        return gain, pad

    def rescale(
        self,
        boxes: [torch.FloatTensor],
        gain: float,
        pad: (float, float),
        img_size: (int, int),
    ) -> [torch.FloatTensor]:
        """rescale.

        :param boxes:
        :type boxes: [torch.FloatTensor]
        :param gain:
        :type gain: float
        :param pad:
        :type pad: (float, float)
        :param img_size:
        :type img_size: (int, int)
        :rtype: [torch.FloatTensor]
        """
        for i, box in enumerate(boxes):
            boxes[i][[0, 2]] -= pad[0]
            boxes[i][[1, 3]] -= pad[1]
            boxes[i] /= gain
            boxes[i][0].clamp_(0, img_size[1])
            boxes[i][2].clamp_(0, img_size[1])
            boxes[i][1].clamp_(0, img_size[0])
            boxes[i][3].clamp_(0, img_size[0])
        return boxes
