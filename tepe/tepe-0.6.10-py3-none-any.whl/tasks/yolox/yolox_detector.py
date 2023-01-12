from loguru import logger

import torch

from tepe.utils.torch_utils import select_device, time_synchronized
from tepe.utils.plots import draw_detection
from tepe.core.base_predictor import Predictor
from .data.data_augment import preproc
from .utils import postprocess


class YOLOXPredictor(Predictor):
    def __init__(self,
                 input_size,
                 classes,
                 model=None,
                 weights=None,
                 preprocess=None,
                 postprecess=None,
                 device=0,
                 conf_thres=0.3,
                 iou_thres=0.5,
                 half=False,
                 save_dir=None):
        super().__init__(save_dir)
        self.device = select_device(device)
        self.classes = classes
        self.half = half
        self.model = model
        self.input_size = input_size
        self.conf_thrs = conf_thres
        self.iou_thrs = iou_thres

        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, *input_size).to(self.device).type_as(
                next(self.model.parameters())))  # run once

        self.preprocess = preprocess
        self.postprocess = postprecess

    def __call__(self, img_meta):
        results = self.run(img_meta)
        result_image = self.draw(img_meta, results)
        return result_image

    def run(self, img_meta):
        img = img_meta['img']
        img_info = {"id": 0}

        height, width = img.shape[:2]
        img_info["height"] = height
        img_info["width"] = width
        img_info["raw_img"] = img

        ratio = min(self.input_size[0] / img.shape[0], self.input_size[1] / img.shape[1])
        img_info["ratio"] = ratio

        img, _ = self.preprocess(img, None, self.input_size)

        img = torch.from_numpy(img).unsqueeze(0)
        img = img.float()

        if self.device.type == "cuda":
            img = img.cuda()
            if self.half:
                img = img.half()  # to FP16

        with torch.no_grad():
            t0 = time_synchronized()
            outputs = self.model(img)
            outputs = postprocess(
                outputs, num_classes=len(self.classes),
                conf_thre=self.conf_thrs, nms_thre=self.iou_thrs
            )
            # if self.postprocess is not None:
                # outputs = self.postprocess(outputs)
            logger.info("Infer time: {:.4f}s".format(time_synchronized() - t0))

        # [x0, y0, x1, y1, obj, conf, cls]
        output = outputs[0].cpu()
        bboxes = output[:, 0:4]

        # preprocessing: resize
        bboxes /= ratio

        cls = output[:, 6]
        scores = output[:, 4] * output[:, 5]

        return dict(
            bboxes=bboxes,
            cls=cls,
            scores=scores
        )

    def draw(self, img_meta, results):
        img = img_meta["img"]

        bboxes, scores, cls = results['bboxes'], results['scores'], results['cls']
        vis_res = draw_detection(img, bboxes, scores, cls, class_names=self.classes)
        return vis_res


