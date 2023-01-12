import time
import torch

from .metrics.cls_metrics import accuracy
from tepe.utils.torch_utils import time_synchronized
from tepe.core.base_evaluator import Evaluator


class ClsEvaluator(Evaluator):
    """
    Evaluation class.
    """
    def __init__(
        self,
        dataloader,
        img_size,
        num_classes,
        **kwargs):
        """
        Args:
            dataloader (Dataloader): evaluate dataloader.
            img_size (tuple): image size after preprocess. images are resized
                to squares whose shape is (img_size, img_size).
        """
        super(ClsEvaluator, self).__init__(dataloader, img_size=img_size, 
                                           num_classes=num_classes, **kwargs)
        self.num_images = len(self.dataloader.dataset)

    def evaluate_one_iter(self, data):
        """

        Args:
            model:
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

        acc1, acc5 = accuracy(output, target, topk=(1, 5))

        return {'acc1': acc1,
                'acc5': acc5}