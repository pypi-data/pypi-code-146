from time import time
import numpy as np
import cv2
from loguru import logger

import torch
import torch.nn.functional as F
from torchvision.transforms import transforms

from tepe.utils.torch_utils import select_device, time_synchronized
from tepe.core.base_predictor import Predictor


class ClsPredictor(Predictor):
    """
    负责推理，支持不同推理后端的支持
    """
    def __init__(self,
                 input_size,
                 classes,
                 weights=None,
                 model=None,
                 device=0,
                 half=False,
                 preprocess=None,
                 save_dir=None,
                 ):
        """

        Args:
            model:
            input_size:
            classes:
            device:
            half:
        """
        super().__init__(save_dir)

        self.classes = classes
        self.input_size = input_size
        self.device = select_device(device)
        self.half = half
        
        self.onnx = model is None
        if self.onnx:
            logger.info('OpenCV DNN backend.')
            self.model = cv2.dnn.readNetFromONNX(weights)       
        else: 
            self.model = model.eval()

            if self.device.type != 'cpu':
                self.model.cuda()
                self.model(torch.zeros(1, 3, *input_size).to(self.device).type_as(
                    next(self.model.parameters())))  # run once

        self.preprocess = preprocess

    def __call__(self, img_meta):
        outputs, img_info = self.run(img_meta)
        result_image = self.draw(outputs[0], img_info)
        return result_image

    def run(self, img_meta):
        img = img_meta['img']
        img_info = {"id": 0}

        height, width = img.shape[:2]
        img_info["height"] = height
        img_info["width"] = width
        img_info["raw_img"] = img

        if self.preprocess is not None:
            img = self.preprocess(img)
            img = img.unsqueeze(0)
        if self.onnx:
            return self.run_cv(img), img_info
        else:
            return self.run_torch(img), img_info

    def run_cv(self, img):
        img = img.numpy()
        self.model.setInput(img)
        t0 = time()
        outputs = self.model.forward(img)[0]
        # logger.info("Infer time: {:.4f}s".format(time() - t0))
        return torch.from_numpy(outputs)

    def run_torch(self, img):
        
        if self.device.type == "cuda":
            img = img.cuda()
            if self.half:
                img = img.half()  # to FP16

        with torch.no_grad():
            t0 = time_synchronized()
            outputs = self.model(img)

            # logger.info("Infer time: {:.4f}s".format(time_synchronized() - t0))
        return outputs

    def draw(self, output, img_info):
        img = img_info["raw_img"]
        if output is None:
            return img

        score = F.softmax(output, dim=0)
        score = score.cpu()
        label_id = np.argmax(score)
        label = self.classes[label_id]
        conf = score[label_id].detach()

        text = f'label: {label}, conf: {conf:.3f}'
        logger.info('result: ' + text)
        vis_res = cv2.putText(img, text, (50, 50), 1, 2, (0, 0, 255))
        return vis_res

