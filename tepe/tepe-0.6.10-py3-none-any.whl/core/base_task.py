import os
import pprint
import re
import time
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple, Any, Optional, Literal, Union, Callable

import addict
import torch
from loguru import logger
from tabulate import tabulate
from tepe.utils.general import ROOT, show_runtime_info, init_seeds, setup_logger
from tepe.utils.torch_utils import load_ckpt


class BaseTask(metaclass=ABCMeta):
    """Basic class for any task."""

    def __init__(self) -> None:
        super().__init__()
        setup_logger()
        show_runtime_info()

        self.seed: int = 42
        self.data_root: str
        self.input_size: int or tuple or list
        self.cache: bool = False

        # train
        self.max_epoch: int = 100
        self.pretrained: bool = False
        self.weights = None
        self.resume = False
        self.resume_ckpt = None  # ckpt for resume

        self.batch_size = 1
        self.basic_lr_per_img = 0.01
        self.__learning_rate = None
        self.fp16 = False

        self.device = 0
        self.ema = True
        self.early_stop = True
        self.print_interval = 10  # iter

        # eval
        self.eval_interval = 1  # epoch

        # predict

        # export
        self.out_file: str = None
        self.input_name = 'images'
        self.output_name = 'output'
        self.trt_version = ['7']
        self.suffix: str = ''
        self.opset: int = 12
        self.dynamic: bool = False
        self.no_onnxsim: bool = False
        self.export_nms: bool = False
        self.include: list = ['onnx']
        self.precision: str = 'fp16'  # ["fp32", "fp16", "int8"]
        self.workspace: int = 1
        self.calib_input: str = None
        self.calib_cache: str = './calibration.cache'
        self.calib_num_images: int = 5000
        self.calib_batch_size: int = 1

        self.task_name = self.__name__
        self.__output_dir = None

        self._post_dict = {}  # info dict for http post
        self.opts = {}

    @property
    def output_dir(self) -> str:
        if self.__output_dir is None:
            if self.weights:
                self.__output_dir = os.path.abspath(os.path.dirname(self.weights))
            else:
                root = str(ROOT)
                self.__output_dir = os.path.join(root, 'outputs',
                                    '_'.join([self.task_name, time.strftime("%y%m%d")]))
        return self.__output_dir

    @output_dir.setter
    def output_dir(self, path):
        self.__output_dir = path

    @property
    def learning_rate(self) -> float:
        if self.__learning_rate:
            return self.__learning_rate
        else:
            return self.basic_lr_per_img * self.batch_size

    @learning_rate.setter
    def learning_rate(self, value):
        self.__learning_rate = value

    @abstractmethod
    def get_model(self, train=True):
        pass

    @abstractmethod
    def get_train_loader(self):
        pass

    def get_eval_loader(self):
        pass

    def get_transform(
            self,
            mode: Literal['train', 'val', 'test'] = 'train'
    ) -> Union[None, Union[Callable, Tuple[Callable, ...]]]:
        return None

    def get_optimizer(self, **kwargs):
        pass

    def get_lr_scheduler(self, **kwargs) -> Union[None, Callable]:
        return None

    def get_loss(self):
        return None

    def get_metrics(self) -> Union[None, Callable]:
        return None

    def get_trainer(self) -> Union[None, Callable]:
        return None

    def get_evaluator(self, train: bool=False) -> Union[None, Callable]:
        return None

    def get_predictor(self) -> Union[None, Callable]:
        return None

    def train(self):
        init_seeds(self.seed)
        trainer = self.get_trainer()
        if trainer is None:
            raise NotImplementedError(f'{self.__class__.__name__} does not'
                                      f'implement get_trainer or train function')
        trainer.train()

    def eval(self):
        assert self.weights is not None, "model weight path is None"
        evaluator = self.get_evaluator(train=False)
        if evaluator is None:
            raise NotImplementedError(f'{self.__class__.__name__} does not '
                                      f'implement get_evaluator or eval function')
        evaluator.evaluate()

    def predict(self, source, view_img=False, save_img=True, **kwargs):
        assert self.weights is not None, "model weight path is None"
        if "predictor" not in self.__dict__:
            self.predictor = self.get_predictor()
        if self.predictor is None: 
            raise NotImplementedError(f'{self.__class__.__name__} does not '
                                      f'implement get_predictor or predict function')
        self.predictor.predict(source, view_img, save_img, **kwargs)

    def export(self):
        assert self.weights is not None, "model weight path is None"
        from tepe.core.exporter import Exporter

        self.batch_size = 1
        model = getattr(self, 'model', None)
        exporter = Exporter(self, model=model)
        exporter.export()

    def run(self, *args) -> Any:
        """
        workflow
        Args:
            *args: [train, eval, predict, export]

        Returns:

        """
        #TODO
        for stage in args:
            func = getattr(self, stage)
            func()

    @property
    def __name__(self):
        name = self.__class__.__name__
        # print(name)
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower().replace('_config', '')

    def __repr__(self):
        table_header = ["keys", "values"]
        task_table = [
            (str(k), pprint.pformat(v))
            for k, v in self.get_args().items()
        ]
        return tabulate(task_table, headers=table_header, tablefmt="fancy_grid")

    def get_args(self):
        args_dict = {k: v for k, v in vars(self).items() if not k.startswith("_")}
        # addict.Dict to Dict
        for k, v in args_dict.items():
            if isinstance(v, addict.Dict):
                args_dict[k] = v.to_dict()
            if isinstance(v, torch.device):
                args_dict[k] = str(v)
        args_dict.update(
            {"output_dir": self.output_dir, "learning_rate": self.learning_rate}
        )
        return args_dict

    def set_post_info(self, **kwargs):
        self._post_dict.update(kwargs)

    def get_post_info(self) -> Dict:
        return self._post_dict

    def merge(self, args: Dict, exclude: List = ()):
        for k, v in args.items():
            # opts=['attr1', 'value1', 'attr2', 'value2', ...]
            if k == 'opts':
                assert len(v) % 2 == 0
                opts_args = {v[i].replace('-', '_'): v[i+1] for i in range(0, len(v), 2)}
                self.merge(opts_args)
                continue
            if k in exclude or v is None:
                continue
            # only update value with same key
            if hasattr(self, k):
                src_value = getattr(self, k)
                if src_value == v:
                    continue
                if src_value is not None:
                    src_type = type(src_value)
                    if src_type is not None and src_type != type(v):
                        arg_type = type(v)
                        try:
                            v = src_type(v)
                        except Exception:
                            pass
                        if src_value == v:
                            continue
                        logger.warning(f"default args {k}'s type is {src_type}, "
                                       f"now it will be {arg_type}")
            setattr(self, k, v)
            logger.info(f"set task's attr '{k}' from args, its value is {v}")

    @staticmethod
    def load_ckpt(model, weights, device=0, is_state_dict=True, load_keys=None):

        """
        load ckpt to model
        Args:
            model: torch model
            weights (str): weights path
            device (int): device num
            is_stat_dict (bool): False: model.load_state_dict(ckpt.state_dict())
                                 True : model.load_state_dict(ckpt)
            load_keys (dict key): weights to be loaded
        Returns:
            model
        """
        if not os.path.exists(weights):
            logger.warning("!!!weights path is not existe")
            return

        load_ckpt(
            model, weights,
            device=device,
            is_state_dict=is_state_dict,
            load_keys=load_keys
        )