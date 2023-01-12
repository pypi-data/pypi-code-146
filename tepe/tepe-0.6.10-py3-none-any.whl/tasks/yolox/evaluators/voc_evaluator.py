import time
from collections import ChainMap
from loguru import logger

import numpy as np

import torch

from tepe.utils.torch_utils import time_synchronized
from tepe.utils.general import colorstr, get_bar
from tepe.core.base_evaluator import Evaluator
from ..utils import postprocess, gather


class VOCEvaluator(Evaluator):
    """
    VOC AP Evaluation class.
    """
    def __init__(self, dataloader, training, conf_thr, nms_thr, **kwargs):
        super().__init__(dataloader, training, **kwargs)
        self.conf_thr = conf_thr
        self.nms_thr = nms_thr

    def evaluate(self, model=None):
        """
        VOC average precision (AP) Evaluation. Iterate inference on the test dataset
        and the results are evaluated by COCO API.

        NOTE: This function will change training mode to False, please save states if needed.

        Args:
            model : model to evaluate.

        Returns:
            ap50_95 (float) : COCO style AP of IoU=50:95
            ap50 (float) : VOC 2007 metric AP of IoU=50
            summary (sr): summary info of evaluation.
        """
        if model is not None:
            self.model = model

        # TODO half to amp_test
        tensor_type = torch.cuda.HalfTensor if self.half else torch.cuda.FloatTensor
        self.model.eval()
        if self.half:
            self.model = self.model.half()

        data_dict = {}

        inference_time = 0
        nms_time = 0
        n_samples = max(len(self.dataloader) - 1, 1)

        self.bar = get_bar(self.dataloader, desc='val')
        with torch.no_grad():
            for cur_iter, (imgs, _, info_imgs, ids) in enumerate(self.bar):
                imgs = imgs.type(tensor_type)

                # skip the the last iters since batchsize might be not enough for batch inference
                is_time_record = cur_iter < len(self.dataloader) - 1
                if is_time_record:
                    start = time.time()

                outputs = self.model(imgs)

                if is_time_record:
                    infer_end = time_synchronized()
                    inference_time += infer_end - start

                outputs = postprocess(
                    outputs, self.num_classes, self.conf_thr, self.nms_thr
                )
                if is_time_record:
                    nms_end = time_synchronized()
                    nms_time += nms_end - infer_end

                data_dict.update(self._convert_to_voc_format(outputs, info_imgs, ids))

        statistics = torch.cuda.FloatTensor([inference_time, nms_time, n_samples])
        if self.distributed:
            data_dict = gather(data_dict, dst=0)
            data_dict = ChainMap(*data_dict)
            torch.distributed.reduce(statistics, dst=0)

        mAP50_95, mAP50, info = self._evaluate_prediction(data_dict, statistics)

        eval_results = dict(ap50=mAP50,
                            ap=mAP50_95,
                            summary=info)
        return eval_results

    def _convert_to_voc_format(self, outputs, info_imgs, ids):
        predictions = {}
        for (output, img_h, img_w, img_id) in zip(
            outputs, info_imgs[0], info_imgs[1], ids
        ):
            if output is None:
                predictions[int(img_id)] = (None, None, None)
                continue
            output = output.cpu()

            bboxes = output[:, 0:4]

            # preprocessing: resize
            scale = min(
                self.img_size[0] / float(img_h), self.img_size[1] / float(img_w)
            )
            bboxes /= scale

            cls = output[:, 6]
            scores = output[:, 4] * output[:, 5]

            predictions[int(img_id)] = (bboxes, cls, scores)
        return predictions

    def _evaluate_prediction(self, data_dict, statistics):

        inference_time = statistics[0].item()
        nms_time = statistics[1].item()
        n_samples = statistics[2].item()

        a_infer_time = 1000 * inference_time / (n_samples * self.dataloader.batch_size)
        a_nms_time = 1000 * nms_time / (n_samples * self.dataloader.batch_size)

        info = ", ".join(
            [
                "Average {} time: {:.2f} ms".format(k, v)
                for k, v in zip(
                    ["forward", "NMS", "inference"],
                    [a_infer_time, a_nms_time, (a_infer_time + a_nms_time)],
                )
            ]
        )
        logger.info(info)

        all_boxes = [
            [[] for _ in range(self.num_images)] for _ in range(self.num_classes)
        ]
        for img_num in range(self.num_images):
            bboxes, cls, scores = data_dict[img_num]
            if bboxes is None:
                for j in range(self.num_classes):
                    all_boxes[j][img_num] = np.empty([0, 5], dtype=np.float32)
                continue
            for j in range(self.num_classes):
                mask_c = cls == j
                if sum(mask_c) == 0:
                    all_boxes[j][img_num] = np.empty([0, 5], dtype=np.float32)
                    continue

                c_dets = torch.cat((bboxes, scores.unsqueeze(1)), dim=1)
                all_boxes[j][img_num] = c_dets[mask_c].numpy()

            # sys.stdout.write(
            #     "im_eval: {:d}/{:d} \r".format(img_num + 1, self.num_images)
            # )
            # sys.stdout.flush()

        ap, ap50 = self.dataloader.dataset.evaluate_detections(
            all_boxes, write_result=self.save_result, output_dir=self.save_dir
        )
        # ap, ap50 = self.dataloader.dataset.evaluate_detections(
        #     all_boxes, output_dir=self.save_dir
        # )
        return ap, ap50, info
