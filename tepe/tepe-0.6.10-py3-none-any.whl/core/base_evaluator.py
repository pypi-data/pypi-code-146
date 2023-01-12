import os
import time

import torch
from loguru import logger

from ..utils.general import increment_path, colorstr, get_bar
from ..utils.meter import MeterBuffer
from ..utils.torch_utils import time_synchronized, select_device


class Evaluator(object):
    """
    Evaluation base class.
    """
    def __init__(
        self,
        dataloader,
        training,
        model=None,
        save_dir=None,
        img_size=None,
        num_classes=None,
        device=0,
        preprocess=None,
        postprocess=None,
        metrics=None,
        half=False,
        distributed=False,
        save_result=False,
        **kwargs
    ):
        """

        Args:
            dataloader:
            img_size:
            num_classes:
            device:
            metrics:
            save_result:
            save_dir:
        """
        self.dataloader = dataloader
        self.img_size = [img_size, img_size] if isinstance(img_size, int) else img_size
        self.num_classes = num_classes
        self.num_images = len(dataloader.dataset)
        self.model = model
        self.preprocess = preprocess
        self.postprocess = postprocess
        self.half = half
        self.distributed = distributed
        self.data_type = torch.cuda.HalfTensor if half else torch.cuda.FloatTensor
        self.save_result = save_result
        self.training = training
        if self.training and model is not None:
            self.device = next(model.parameters()).device
        else:
            self.device = select_device(device)
        if save_result and not training:
            if save_dir is None:
                save_dir = 'outputs'
            self.save_dir = increment_path(
                os.path.join(save_dir, 'eval'), mkdir=True, increment=False
            )
        else:
            self.save_dir = None
        self.metrics = metrics

    def evaluate(self, model=None):
        """
        Args:
            model: model to evaluate.

        Returns:
            a dict contains:

        """
        if model is not None:
            self.model = model
        n_samples = max(len(self.dataloader) - 1, 1)
        self.inference_time = 0.0
        eval_meter = MeterBuffer(len(self.dataloader) + 10)
        self.model.eval()
        self.model.to(self.device)

        self.bar = get_bar(self.dataloader, desc='val')
        for self.iter, data in enumerate(self.bar):
            output = self.evaluate_one_iter(data)

            eval_meter.update(**output)

        metrics_dict = {k: v.avg for k, v in eval_meter.get_avg_meter().items()}

        a_infer_time = 1000 * self.inference_time / (n_samples * self.dataloader.batch_size)
        info = "Average inference time: {:.2f} ms".format(a_infer_time)
        info += ", " + ", ".join(
            ["{}: {:.3f}".format(k, v) for k, v in metrics_dict.items()])
        logger.info(colorstr('blue', info))

        return metrics_dict

    def evaluate_one_iter(self, data):
        """

        Args:
            data: outputs of your Dataset

        Returns:
            Dict of evaluate outputs
        """
        imgs, target, info_imgs, path = data
        imgs = imgs.type(self.data_type).cuda(non_blocking=True)
        target = target.to(torch.long).cuda(non_blocking=True)

        # skip the the last iters since batchsize might be not enough for batch inference
        is_time_record = self.iter < len(self.dataloader) - 1

        start = time.time()
        with torch.no_grad():
            output = self.model(imgs)

        if is_time_record:
            infer_end = time_synchronized()
            self.inference_time += (infer_end - start)
            torch.cuda.synchronize()

        acc1, acc5 = self.metrics(output, target, topk=(1, 5))

        return {'acc1': acc1,
                'acc5': acc5}