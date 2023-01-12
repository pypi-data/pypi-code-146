import time

import torch
from loguru import logger

from tepe.utils.general import colorstr, get_bar
from tepe.utils.torch_utils import time_synchronized
from .metrics import seg_metrics
from tepe.core.base_evaluator import Evaluator


class SegEvaluator(Evaluator):
    """
    Evaluation class.
    """
    def __init__(
        self,
        **kwargs
        ):
        """

        Args:
            dataloader:
            img_size:
            num_classes:
            device:
            metrics (str):
            save_result:
            save_dir:
        """
        super(SegEvaluator, self).__init__(**kwargs)

        self.metrics = seg_metrics.StreamSegMetrics(self.num_classes)

    def evaluate(self, model):
        """
        Args:
            model: model to evaluate.

        Returns:
            a dict contains:

        """
        self.metrics.reset()

        self.model = model
        self.model.to(self.device)
        n_samples = max(len(self.dataloader) - 1, 1)
        self.inference_time = 0.0
        bar = get_bar(self.dataloader, desc='val')
        for self.iter, data in enumerate(bar):
            output = self.evaluate_one_iter(data)

        metrics_dict = self.metrics.get_results()

        a_infer_time = 1000 * self.inference_time / (n_samples * self.dataloader.batch_size)
        info = "Average inference time: {:.2f} ms".format(a_infer_time)
        info += "\n" + "\n".join(
                ["{}: {:.5f}".format(k, v) for k, v in metrics_dict['Class IoU'].items()]
                )
        info += "\n" + self.metrics.to_str(metrics_dict)
        logger.info(colorstr('blue', info))

        return metrics_dict

    def evaluate_one_iter(self, data):
        images, labels = data
        images = images.to(self.device, dtype=torch.float32)
        labels = labels.to(self.device, dtype=torch.long)

        start = time.time()
        with torch.no_grad():
            outputs = self.model(images)
        self.inference_time += (time_synchronized() - start)
        torch.cuda.synchronize()

        preds = outputs.detach().max(dim=1)[1].cpu().numpy()
        targets = labels.cpu().numpy()

        self.metrics.update(targets, preds)