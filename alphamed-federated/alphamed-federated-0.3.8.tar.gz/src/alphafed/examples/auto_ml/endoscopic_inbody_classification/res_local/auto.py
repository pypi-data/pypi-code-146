# Copyright 2022 Alphamed

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Pretraining endoscopic_inbody_classification models and schedulers."""

import json
import os
from copy import deepcopy
from dataclasses import InitVar, asdict, dataclass
from typing import Dict, Optional, Tuple, overload

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from senet.cv.senet import SEResNet50
from torch import nn, optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from alphafed import get_result_dir, logger
from alphafed.auto_ml.auto_model import (AutoFedAvgModel, AutoFedAvgScheduler,
                                         AutoModel, DatasetMode,
                                         MandatoryConfig, Preprocessor)
from alphafed.auto_ml.cvat.annotation import ImageAnnotationUtils
from alphafed.auto_ml.exceptions import AutoModelError, ConfigError
from alphafed.scheduler import register_metrics


@dataclass
class PreprocessorConfig:

    size: int
    do_rotation: bool
    do_scale_intensity: bool
    do_shift_intensity: bool
    do_gaussian_noised: bool
    do_horizontal_flip: bool
    do_vertical_flip: bool
    do_channel_wise_normalize: bool

    prob_rotation: float = 0.0
    degrees: float = 0.0
    prob_scale_intensity: float = 0.0
    prob_shift_intensity: float = 0.0
    prob_gaussian_noised: float = 0.0

    def __post_init__(self):
        if self.do_rotation and (self.prob_rotation < 0 or self.prob_rotation > 1):
            raise ConfigError(f'Invalid prob_rotation: `{self.prob_rotation}`.')
        if (
            self.do_scale_intensity
            and (self.prob_scale_intensity < 0 or self.prob_scale_intensity > 1)
        ):
            raise ConfigError(f'Invalid prob_scale_intensity: `{self.prob_scale_intensity}`.')
        if (
            self.do_shift_intensity
            and (self.prob_shift_intensity < 0 or self.prob_shift_intensity > 1)
        ):
            raise ConfigError(f'Invalid prob_shift_intensity: `{self.prob_shift_intensity}`.')
        if (
            self.do_gaussian_noised
            and (self.prob_gaussian_noised < 0 or self.prob_gaussian_noised > 1)
        ):
            raise ConfigError(f'Invalid prob_gaussian_noised: `{self.prob_gaussian_noised}`.')


class SEResNetPreprocessor(Preprocessor):

    class ScaleIntensity(nn.Module):

        def __init__(self) -> None:
            super().__init__()

        def forward(self, image: torch.Tensor, factor: float = 0.3) -> torch.Tensor:
            return image * (1 + factor)

    def __init__(self, mode: DatasetMode, config: PreprocessorConfig) -> None:
        super().__init__()
        self.R = np.random.RandomState()
        layers = [transforms.Resize((config.size, config.size))]
        if mode == DatasetMode.TRAINING:
            if config.do_rotation:
                layers.append(transforms.RandomApply(
                    nn.Sequential(
                        transforms.RandomRotation(
                            degrees=config.degrees,
                            interpolation=transforms.InterpolationMode.BILINEAR
                        )
                    ),
                    p=config.prob_rotation
                ))
        layers.append(transforms.ToTensor())
        if mode == DatasetMode.TRAINING:
            if config.do_scale_intensity:
                layers.append(transforms.RandomApply([self._scale_intensity],
                                                     p=config.prob_scale_intensity))
            if config.do_shift_intensity:
                layers.append(transforms.RandomApply([self._shift_intensity],
                                                     p=config.prob_shift_intensity))
            if config.do_gaussian_noised:
                layers.append(transforms.RandomApply([self._gaussian_noised],
                                                     p=config.prob_gaussian_noised))
            if config.do_horizontal_flip:
                layers.append(transforms.RandomHorizontalFlip())
            if config.do_vertical_flip:
                layers.append(transforms.RandomVerticalFlip())
        layers.append(transforms.Lambda(lambda image: self._channel_wise_normalize(image=image)))
        self._transformer = transforms.Compose(layers)

    def _channel_wise_normalize(self, image: torch.Tensor) -> torch.Tensor:
        for i, _chn in enumerate(image):
            slices = _chn != 0
            _mean = torch.mean(_chn[slices])
            _std = torch.std(_chn[slices], unbiased=False)
            _chn = (_chn - _mean) / _std
            image[i] = _chn
        return image

    def _scale_intensity(self, image: torch.Tensor, factor: float = 0.3) -> torch.Tensor:
        return image * (1 + factor)

    def _shift_intensity(self, image: torch.Tensor, offset: float = 0.1) -> torch.Tensor:
        return image + offset

    def _gaussian_noised(self,
                         image: torch.Tensor,
                         mean: float = 0.0,
                         std: float = 0.01) -> torch.Tensor:
        rand_std = self.R.uniform(0, std)
        noise = self.R.normal(mean, rand_std, size=image.shape)
        return image + noise.astype(np.float32)

    def transform(self, image_file: str) -> torch.Tensor:
        """Transform an image object into an input tensor."""
        image = Image.open(image_file).convert('RGB')
        image = self._transformer(image)
        return image


class SEResNetDataset(Dataset):

    def __init__(self,
                 image_dir: str,
                 annotation_file: str,
                 mode: DatasetMode,
                 config: PreprocessorConfig) -> None:
        """Init a dataset instance for ResNet auto model families.

        Args:
            image_dir:
                The directory including image files.
            annotation_file:
                The file including annotation information.
            mode:
                One of training or validation or testing.
            config:
                The configuration for the preprocessor.
        """
        super().__init__()
        if not image_dir or not isinstance(image_dir, str):
            raise ConfigError(f'Invalid image directory: {image_dir}.')
        if not annotation_file or not isinstance(annotation_file, str):
            raise ConfigError(f'Invalid annotation file path: {annotation_file}.')
        assert mode and isinstance(mode, DatasetMode), f'Invalid dataset mode: {mode}.'
        if not os.path.exists(image_dir) or not os.path.isdir(image_dir):
            raise ConfigError(f'{image_dir} does not exist or is not a directory.')
        if not os.path.exists(annotation_file) or not os.path.isfile(annotation_file):
            raise ConfigError(f'{annotation_file} does not exist or is not a file.')

        self.image_dir = image_dir
        self.annotation_file = annotation_file
        self.transformer = SEResNetPreprocessor(mode=mode, config=config)

        self.images, self.labels = ImageAnnotationUtils.parse_single_category_annotation(
            annotation_file=self.annotation_file, resource_dir=image_dir, mode=mode
        )

    def __getitem__(self, index: int):
        _item = self.images[index]
        return self.transformer(_item.image_file), _item.class_label

    def __len__(self):
        return len(self.images)


@dataclass
class ModelConfig(MandatoryConfig):

    id2label: dict
    label2id: dict
    learning_rate: int
    batch_size: int
    epochs: int
    image_size: int = 256
    torch_dtype: InitVar[str] = 'float32'

    def __post_init__(self, torch_dtype: str):
        super().__post_init__()

        for _label in self.id2label.values():
            if _label not in self.label2id:
                raise TypeError(f'Label `{_label}` lost its ID in label2id map.')
        for _id in self.label2id.values():
            if str(_id) not in self.id2label:
                raise TypeError(f'ID `{_id}` lost its label in id2label map.')

        if self.learning_rate <= 0:
            raise TypeError(f'Invalid learning_rate: `{self.learning_rate}`.')
        if self.batch_size <= 0:
            raise TypeError(f'Invalid batch_size: `{self.batch_size}`.')
        if self.epochs <= 0:
            raise TypeError(f'Invalid epochs: `{self.epochs}`.')

        if self.image_size <= 0:
            raise TypeError(f'Invalid image_size: `{self.image_size}`.')

        if torch_dtype == 'float32' or torch_dtype == 'float':
            self.torch_dtype = torch.float32
        elif torch_dtype == 'float64':
            self.torch_dtype = torch.float64
        elif torch == 'float16':
            self.torch_dtype = torch.float16
        else:
            raise TypeError(f'Invalid torch_dtype: `{torch_dtype}`.')


class AutoSEResNet(AutoModel):

    def __init__(self, resource_dir: str, **kwargs) -> None:
        super().__init__(resource_dir=resource_dir)

        self.config, self.preprocessor_config = self._load_config()
        self.epochs = self.config.epochs
        self.batch_size = self.config.batch_size
        self.lr = self.config.learning_rate
        self._epoch = 0
        self.is_cuda = torch.cuda.is_available()

        self.dataset_dir = None
        self.labels = None

        self._best_result = 0
        self._best_state = None
        self._overfit_index = 0
        self._is_dataset_initialized = False
        self._save_root = '.cache'

    def _load_config(self) -> Tuple[ModelConfig, PreprocessorConfig]:
        config_file = os.path.join(self.resource_dir, 'config.json')
        if not os.path.isfile(config_file):
            raise ConfigError('Config file missing.')
        try:
            with open(config_file, 'r') as f:
                config_json = json.load(f)
        except json.JSONDecodeError:
            raise ConfigError('Failed to parse config file.')
        model_config = ModelConfig(**config_json)

        preprocessor_config_file = os.path.join(self.resource_dir, 'preprocessor_config.json')
        if not os.path.isfile(preprocessor_config_file):
            raise ConfigError('Preprocessor config file missing.')
        try:
            with open(preprocessor_config_file, 'r') as f:
                preprocessor_config_json = json.load(f)
        except json.JSONDecodeError:
            raise ConfigError('Failed to parse preprocessor config file.')
        preprocessor_config = PreprocessorConfig(**preprocessor_config_json)

        return model_config, preprocessor_config

    @property
    def annotation_file(self):
        return os.path.join(self.dataset_dir, 'annotation.json') if self.dataset_dir else None

    def init_dataset(self, dataset_dir: str) -> Tuple[bool, str]:
        self.dataset_dir = dataset_dir
        try:
            if not self._is_dataset_initialized:
                self.training_loader
                self.validation_loader
                self.testing_loader
                if not self.training_loader or not self.testing_loader:
                    logger.error('Both training data and testing data are missing.')
                    return False, 'Must provide train dataset and test dataset to fine tune.'
                self.labels = (self.training_loader.dataset.labels
                               if self.training_loader
                               else self.testing_loader.dataset.labels)
                self._is_dataset_initialized = True
            return True, 'Initializing dataset complete.'
        except Exception:
            logger.exception('Failed to initialize dataset.')
            return False, '初始化数据失败，请联系模型作者排查原因。'

    @property
    def training_loader(self) -> DataLoader:
        """Return a dataloader instance of training data.

        Data augmentation is used to improve performance, so we need to generate a new dataset
        every epoch in case of training on a same dataset over and over again.
        """
        if not hasattr(self, "_training_loader"):
            self._training_loader = self._build_training_data_loader()
        return self._training_loader

    def _build_training_data_loader(self) -> Optional[DataLoader]:
        dataset = SEResNetDataset(image_dir=self.dataset_dir,
                                  annotation_file=self.annotation_file,
                                  mode=DatasetMode.TRAINING,
                                  config=self.preprocessor_config)
        if len(dataset) == 0:
            return None
        return DataLoader(dataset=dataset,
                          batch_size=self.batch_size,
                          shuffle=True)

    @property
    def validation_loader(self) -> DataLoader:
        """Return a dataloader instance of validation data."""
        if not hasattr(self, "_validation_loader"):
            self._validation_loader = self._build_validation_data_loader()
        return self._validation_loader

    def _build_validation_data_loader(self) -> DataLoader:
        dataset = SEResNetDataset(image_dir=self.dataset_dir,
                                  annotation_file=self.annotation_file,
                                  mode=DatasetMode.VALIDATION,
                                  config=self.preprocessor_config)
        if len(dataset) == 0:
            return None
        return DataLoader(dataset=dataset, batch_size=self.batch_size)

    @property
    def testing_loader(self) -> DataLoader:
        """Return a dataloader instance of testing data."""
        if not hasattr(self, "_testing_loader"):
            self._testing_loader = self._build_testing_data_loader()
        return self._testing_loader

    def _build_testing_data_loader(self) -> DataLoader:
        dataset = SEResNetDataset(image_dir=self.dataset_dir,
                                  annotation_file=self.annotation_file,
                                  mode=DatasetMode.TESTING,
                                  config=self.preprocessor_config)
        if len(dataset) == 0:
            return None
        return DataLoader(dataset=dataset, batch_size=self.batch_size)

    def _build_model(self):
        self._model: nn.Module = SEResNet50(spatial_dims=2, in_channels=3)

        self.labels = list(self.config.id2label.values())
        self._replace_fc_if_diff(len(self.labels))

        param_file = os.path.join(self.resource_dir, self.config.param_file)
        with open(param_file, 'rb') as f:
            state_dict = torch.load(f)
            model_num_classes = self._model.get_parameter('last_linear.weight').shape[0]
            param_num_classes = state_dict['last_linear.weight'].shape[0]
            if model_num_classes != param_num_classes:
                raise AutoModelError('The fine tuned labels dismatched the parameters.')
            self._model.load_state_dict(state_dict)

        return self._model.cuda() if self.is_cuda else self._model

    def _replace_fc_if_diff(self, num_classes: int):
        """Replace the classify layer with new number of classes."""
        assert (
            num_classes and isinstance(num_classes, int) and num_classes > 0
        ), f'Invalid number of classes: {num_classes} .'
        if num_classes != self.num_classes:
            self.model.last_linear = nn.Linear(2048, num_classes)

    @property
    def num_classes(self) -> int:
        """Return the number of classes of the classification layer of the model."""
        return self.model.get_parameter('last_linear.weight').shape[0]

    @property
    def model(self) -> nn.Module:
        if not hasattr(self, '_model'):
            self._model = self._build_model()
        return self._model

    @property
    def optimizer(self) -> optim.Optimizer:
        if not hasattr(self, '_optimizer'):
            self._optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        return self._optimizer

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()

    @overload
    def forward(self, input: torch.Tensor) -> str:
        """Predict an image's tensor and give its label."""

    @overload
    def forward(self, input: str) -> str:
        """Predict an image defined by a file path and give its label."""

    @torch.no_grad()
    def forward(self, input):
        if not input or not isinstance(input, (str, torch.Tensor)):
            raise AutoModelError(f'Invalid input data: {input}.')
        if isinstance(input, str):
            if not os.path.isfile(input):
                raise AutoModelError(f'Cannot find or access the image file {input}.')
            preprocessor = SEResNetPreprocessor(mode=DatasetMode.PREDICTING,
                                                config=self.preprocessor_config)
            input = preprocessor.transform(input)
            input.unsqueeze_(0)
        self.model.eval()
        output: torch.Tensor = self.model(input)
        predict = output.argmax(1)[0].item()
        if not self.labels:
            if not os.path.isfile(os.path.join(self.resource_dir, 'fine_tuned.meta')):
                raise AutoModel('The `fine_tuned.meta` file is required to make prediction.')
            with open(os.path.join(self.resource_dir, 'fine_tuned.meta')) as f:
                fine_tuned_json: dict = json.loads(f)
                self.labels = fine_tuned_json.get('labels')
        return self.labels[predict]

    def _train_an_epoch(self):
        self.train()
        for images, targets in self.training_loader:
            if self.is_cuda:
                images, targets = images.cuda(), targets.cuda()
            output = self.model(images)
            loss = F.cross_entropy(output, targets)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    @torch.no_grad()
    def _run_test(self) -> Tuple[float, float]:
        """Run a round of test and report the result.

        Return:
            avg_loss, correct_rate
        """
        self.push_log(f'Begin testing of epoch {self._epoch}.')
        self.eval()
        total_loss = 0
        total_correct = 0
        for images, targets in self.testing_loader:
            if self.is_cuda:
                images, targets = images.cuda(), targets.cuda()
            output = self.model(images)
            loss = F.cross_entropy(output, targets, reduction='sum').item()
            total_loss += loss
            pred = output.max(1, keepdim=True)[1]
            total_correct += pred.eq(targets.view_as(pred)).sum().item()

        avg_loss = total_loss / len(self.testing_loader.dataset)
        correct_rate = total_correct / len(self.testing_loader.dataset) * 100
        logger.info(f'Testing Average Loss: {avg_loss:.4f}')
        logger.info(f'Testing Correct Rate: {correct_rate:.2f}')

        return avg_loss, correct_rate

    @torch.no_grad()
    def _run_validation(self) -> Tuple[float, float]:
        """Run a round of validation and report the result.

        Return:
            avg_loss, correct_rate
        """
        self.eval()
        total_loss = 0
        total_correct = 0
        for images, targets in self.validation_loader:
            if self.is_cuda:
                images, targets = images.cuda(), targets.cuda()
            output = self.model(images)
            loss = F.cross_entropy(output, targets, reduction='sum').item()
            total_loss += loss
            pred = output.max(1, keepdim=True)[1]
            total_correct += pred.eq(targets.view_as(pred)).sum().item()

        avg_loss = total_loss / len(self.validation_loader.dataset)
        correct_rate = total_correct / len(self.validation_loader.dataset) * 100
        logger.info(f'Validation Average Loss: {avg_loss:.4f}')
        logger.info(f'Validation Correct Rate: {correct_rate:.2f}')
        return avg_loss, correct_rate

    @torch.no_grad()
    def _is_finished(self) -> bool:
        """Decide if stop training.

        If there are validation dataset, decide depending on validatation results. If
        the validation result of current epoch is below the best record for 10 continuous
        times, then stop training.
        If there are no validation dataset, run for `epochs` times.
        """
        if not self.validation_loader or len(self.validation_loader) == 0:
            if self._epoch >= self.epochs:
                self._best_state = deepcopy(self.model.state_dict())
            return self._epoch >= self.epochs
        # make a validation
        self.push_log(f'Begin validation of epoch {self._epoch}.')
        avg_loss, correct_rate = self._run_validation()
        self.push_log('\n'.join(('Validation result:',
                                 f'avg_loss={avg_loss:.4f}',
                                 f'correct_rate={correct_rate:.2f}')))

        if correct_rate > self._best_result:
            self._overfit_index = 0
            self._best_result = correct_rate
            self._best_state = deepcopy(self.model.state_dict())
            self.push_log('Validation result is better than last epoch.')
            return False
        else:
            self._overfit_index += 1
            msg = f'Validation result gets worse for {self._overfit_index} consecutive times.'
            self.push_log(msg)
            return self._overfit_index >= 10 or self._epoch >= self.epochs

    def fine_tune(self,
                  id: str,
                  task_id: str,
                  dataset_dir: str,
                  is_initiator: bool = False,
                  is_debug_script: bool = False):
        self.id = id
        self.task_id = task_id
        self.is_initiator = is_initiator
        self.is_debug_script = is_debug_script

        is_succ, err_msg = self.init_dataset(dataset_dir)
        if not is_succ:
            raise AutoModelError(f'Failed to initialize dataset. {err_msg}')
        num_classes = (len(self.training_loader.dataset.labels)
                       if self.training_loader
                       else len(self.testing_loader.dataset.labels))
        self._replace_fc_if_diff(num_classes)

        self.config.id2label = {str(_idx): _label for _idx, _label in enumerate(self.labels)}
        self.config.label2id = {_label: _idx for _idx, _label in enumerate(self.labels)}
        self.config.label2id = dict(sorted(self.config.label2id.items()))

        is_finished = False
        while not is_finished:
            self._epoch += 1
            self.push_log(f'Begin training of epoch {self._epoch}.')
            self._train_an_epoch()
            self.push_log(f'Complete training of epoch {self._epoch}.')
            is_finished = self._is_finished()

        self._save_fine_tuned()
        avg_loss, correct_rate = self._run_test()
        self.push_log('\n'.join(('Testing result:',
                                 f'avg_loss={avg_loss:.4f}',
                                 f'correct_rate={correct_rate:.2f}')))

    def _save_fine_tuned(self):
        """Save the best or final state of fine tuning."""
        result_dir = get_result_dir(self.task_id)
        os.makedirs(result_dir, exist_ok=True)
        with open(os.path.join(result_dir, self.config.param_file), 'wb') as f:
            torch.save(self._best_state, f)
        with open(os.path.join(result_dir, 'config.json'), 'w') as f:
            f.write(json.dumps(asdict(self.config), ensure_ascii=False))


class AutoSEResNetFedAvg(AutoSEResNet, AutoFedAvgModel):

    @property
    def param_file(self) -> str:
        return self.config.param_file

    @property
    def init_args_for_fine_tuned(self) -> Optional[str]:
        return json.dumps({'labels': self.labels}, ensure_ascii=False)

    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self.model.state_dict()

    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        return self.model.load_state_dict(state_dict)

    def train_an_epoch(self):
        self._epoch += 1
        self._train_an_epoch()

    def run_test(self) -> Tuple[float, float]:
        """Run a test and report the result.

        Return:
            avg_loss, correct_rate
        """
        return self._run_test()

    def run_validation(self):
        """Run a test and report the result.

        Return:
            avg_loss, correct_rate
        """
        return self._run_validation()

    def init_dataset(self, dataset_dir: str) -> Tuple[bool, str]:
        self.dataset_dir = dataset_dir
        try:
            if not self._is_dataset_initialized:
                self.training_loader
                self.validation_loader
                self.testing_loader
                if not self.training_loader and not self.testing_loader:
                    logger.error('Both training data and testing data are missing.')
                    err_msg = ' '.join((
                        'The initiator must provide test dataset.',
                        'The collaborator must provide train dataset.'
                    ))
                    return False, err_msg
                self.labels = (self.training_loader.dataset.labels
                               if self.training_loader
                               else self.testing_loader.dataset.labels)
                self._is_dataset_initialized = True
            return True, 'Initializing dataset complete.'
        except Exception:
            logger.exception('Failed to initialize dataset.')
            return False, '初始化数据失败，请联系模型作者排查原因。'

    def fine_tune(self,
                  id: str,
                  task_id: str,
                  dataset_dir: str,
                  is_initiator: bool = False):
        is_succ, err_msg = self.init_dataset(dataset_dir)
        if not is_succ:
            raise AutoModelError(f'Failed to initialize dataset. {err_msg}')
        num_classes = (len(self.training_loader.dataset.labels)
                       if self.training_loader
                       else len(self.testing_loader.dataset.labels))
        self._replace_fc_if_diff(num_classes)

        self._fine_tune_impl(id=id,
                             task_id=task_id,
                             dataset_dir=dataset_dir,
                             scheduler_impl=SEResNetFedAvgScheduler,
                             is_initiator=is_initiator,
                             max_rounds=self.config.epochs,
                             log_rounds=1)


class SEResNetFedAvgScheduler(AutoFedAvgScheduler):

    def __init__(self,
                 auto_proxy: AutoSEResNetFedAvg,
                 min_clients: int,
                 max_clients: int,
                 max_rounds: int = 0,
                 merge_epochs: int = 1,
                 calculation_timeout: int = 300,
                 schedule_timeout: int = 30,
                 log_rounds: int = 0,
                 involve_aggregator: bool = False):
        super().__init__(auto_proxy=auto_proxy,
                         min_clients=min_clients,
                         max_clients=max_clients,
                         max_rounds=max_rounds,
                         merge_epochs=merge_epochs,
                         calculation_timeout=calculation_timeout,
                         schedule_timeout=schedule_timeout,
                         log_rounds=log_rounds,
                         involve_aggregator=involve_aggregator)
        self._best_state = None
        self._best_result = 0
        self._overfit_index = 0

    @property
    def best_state_dict(self) -> Dict[str, torch.Tensor]:
        return self._best_state

    def validate_context(self):
        super().validate_context()
        if self.is_initiator:
            assert self.test_loader and len(self.test_loader) > 0, 'failed to load test data'
            self.push_log(f'There are {len(self.test_loader.dataset)} samples for testing.')
        else:
            assert self.train_loader and len(self.train_loader) > 0, 'failed to load train data'
            self.push_log(f'There are {len(self.train_loader.dataset)} samples for training.')

    def train_an_epoch(self):
        self.auto_proxy.train_an_epoch()

    @register_metrics(name='test_results', keys=['average_loss', 'correct_rate'])
    def test(self):
        avg_loss, correct_rate = self.auto_proxy.run_test()
        self.get_metrics('test_results').append_metrics_item({
            'average_loss': avg_loss,
            'correct_rate': correct_rate
        })

    def is_task_finished(self) -> bool:
        """Decide if stop training.

        If there are validation dataset, decide depending on validatation results. If
        the validation result of current epoch is below the best record for 10 continuous
        times, then stop training.
        If there are no validation dataset, run for `max_rounds` times.
        """
        if not self.validation_loader or len(self.validation_loader) == 0:
            self._best_state = deepcopy(self.state_dict())
            return self._is_reach_max_rounds()

        # make a validation
        self.push_log(f'Begin validation of round {self.current_round}.')
        avg_loss, correct_rate = self.auto_proxy.run_validation()
        self.push_log('\n'.join(('Validation result:',
                                 f'avg_loss={avg_loss:.4f}',
                                 f'correct_rate={correct_rate:.2f}')))

        if correct_rate > self._best_result:
            self._overfit_index = 0
            self._best_result = correct_rate
            self._best_state = deepcopy(self.state_dict())
            self.push_log('Validation result is better than last epoch.')
            return False
        else:
            self._overfit_index += 1
            msg = f'Validation result gets worse for {self._overfit_index} consecutive times.'
            self.push_log(msg)
            return self._overfit_index >= 10 or self._is_reach_max_rounds()
