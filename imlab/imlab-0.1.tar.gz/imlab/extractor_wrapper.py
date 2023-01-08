import numpy as np
import torch
import torchvision
from PIL import Image

from .tools import ModelNotImplementedError, open_img


def preprocess(image: np.ndarray, device: str = "cpu") -> torch.FloatTensor:
    """preprocess. Pre process the input image: transform to float and normalize

    :param image: image to be preprocessed
    :type image: np.ndarray
    :param device: device to be used
    :type image: str
    :rtype: torch.FloatTensor
    """
    img = torch.from_numpy(image).to(device)
    img = img.float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    return img


def decode(
    result: [torch.FloatTensor], conf_thresh: float = 0.25, iou: float = 0.45
) -> list[tuple]:
    """decode. Decode the output into (bounding_boxes,classe) pair

    :param result:
    :type result: [torch.FloatTensor]
    :param conf_thresh:
    :type conf_thresh: float
    :param iou:
    :type iou: float
    :rtype: list[tuple]
    """
    result = result[0]
    num_classes = result.shape[2] - 5
    mask_obj_conf = result[:, :, 4] > conf_thresh
    boxcla = [None] * result.shape[0]
    for i, res in enumerate(result):

        x = res[mask_obj_conf[i, :]]
        if num_classes == 1:
            x[:, 5:] = x[:, 4:5]
        else:
            x[:, 5:] *= x[:, 4:5]
        mask_conf, valid_classes = (x[:, 5:] > conf_thresh).nonzero(as_tuple=True)
        mat = x[mask_conf, :]
        box = xywh2xyxy(mat[:, :4])
        score = mat[:, 4]
        index_nms = torchvision.ops.nms(box, score, iou)
        boxes = []
        classes = []
        for ind in index_nms:
            boxes += [box[ind, 0:4]]
            classes += [torch.sort(mat[ind, 5:], descending=True)]
        boxcla[i] = (boxes, classes)
    return boxcla


class Wrapper:
    """Wrapper. Pytorch wrapper"""

    def __init__(
        self,
        weight: str = None,
        model_type: str = "yoloV7",
        image_size: int = 640,
        model: object = None,
        preprocess: callable = preprocess,
        decode: callable = decode,
        classes: list = [],
        model_mod: str = "use",
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
        :param model_mod:
        :type model_mod: str
        :rtype: None
        """
        self.weight = weight
        self.model_type = model_type
        self.image_size = image_size
        self.preprocess = preprocess
        self.decode = decode
        self.num_class = len(classes)
        self.classes = classes
        self.model_mod = model_mod
        if model is None:
            self._get_model(model_type)
        else:
            self.model = model

    def _get_model(self, model_type: str) -> object:
        """_get_model.

        :param model_type:
        :type model_type: str
        :rtype: object
        """
        if model_type.lower() == "yolov7":
            if self.model_mod == "use":
                self.model = torch.load(self.weight, map_location=torch.device("cpu"))
            elif self.model == "new":
                raise ModelNotImplementedError
            elif self.model == "resume":
                raise ModelNotImplementedError
            elif self.model == "add":
                raise ModelNotImplementedError

        else:
            raise ModelNotImplementedError
        return self.model

    def norm_input(self, image: object) -> torch.FloatTensor:
        """norm_input.

        :param image:
        :type image: object
        :rtype: torch.FloatTensor
        """
        to_predict = open_img(image)
        to_predict = letterbox(to_predict, img_size=self.image_size)
        to_predict = np.array(to_predict)[:, :, ::-1].transpose(2, 0, 1)
        to_predict = np.ascontiguousarray(to_predict)
        return to_predict

    def open_img(self, image: object) -> np.ndarray:
        """open_img.

        :param image:
        :type image: object
        :rtype: np.ndarray
        """
        return np.array(open_img(image))


def letterbox(
    img: Image, img_size: int = 640, color: (int, int, int) = (114, 114, 144)
) -> Image:
    """letterbox. resize image and pad it to be of (img_size,img_size) size

    :param img:
    :type img: Image
    :param img_size:
    :type img_size: int
    :param color:
    :type color: (int, int, int)
    :rtype: Image
    """
    img.thumbnail((img_size, img_size))
    imsize = img.size
    left = (img_size - imsize[0]) // 2
    top = (img_size - imsize[1]) // 2
    image_pad = Image.new(img.mode, (img_size, img_size), color)
    image_pad.paste(img, (left, top))
    return image_pad


def xywh2xyxy(box: object) -> object:
    """xywh2xyxy. transform x,y,w,h bouding box into x1,y2,x2,y2

    :param box:
    :type box: object
    :rtype: object
    """
    box_ = box.clone() if isinstance(box, torch.Tensor) else np.copy(box)
    box_[:, 0] = box[:, 0] - box[:, 2] / 2
    box_[:, 1] = box[:, 1] - box[:, 3] / 2
    box_[:, 2] = box[:, 0] + box[:, 2] / 2
    box_[:, 3] = box[:, 1] + box[:, 3] / 2
    return box_
