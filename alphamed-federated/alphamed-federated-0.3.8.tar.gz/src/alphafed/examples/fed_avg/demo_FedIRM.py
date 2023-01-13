import os
import re
from collections import OrderedDict
from typing import Dict

import numpy as np
import pandas as pd
import torch
# import torch.backends.cudnn as cudnn
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from imblearn.metrics import sensitivity_score, specificity_score
from PIL import Image
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             roc_auc_score)
from torch import Tensor, nn
from torch.optim import Adam, Optimizer
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from ... import logger
from ...fed_avg import FedAvgScheduler

__all__ = ['DemoFedIRM']


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class _DenseLayer(nn.Sequential):
    def __init__(self, num_input_features, growth_rate, bn_size, drop_rate):
        super(_DenseLayer, self).__init__()
        self.add_module('norm1', nn.BatchNorm2d(num_input_features)),
        self.add_module('relu1', nn.ReLU(inplace=True)),
        self.add_module('conv1', nn.Conv2d(num_input_features,
                                           bn_size * growth_rate,
                                           kernel_size=1,
                                           stride=1,
                                           bias=False)),
        self.add_module('norm2', nn.BatchNorm2d(bn_size * growth_rate)),
        self.add_module('relu2', nn.ReLU(inplace=True)),
        self.add_module('conv2', nn.Conv2d(bn_size * growth_rate,
                                           growth_rate,
                                           kernel_size=3,
                                           stride=1,
                                           padding=1,
                                           bias=False)),
        self.drop_rate = drop_rate
        self.drop_layer = nn.Dropout(p=drop_rate)

    def forward(self, x):
        new_features = super(_DenseLayer, self).forward(x)
        return torch.cat([x, new_features], 1)


class _DenseBlock(nn.Sequential):
    def __init__(self, num_layers, num_input_features, bn_size, growth_rate, drop_rate):
        super(_DenseBlock, self).__init__()
        for i in range(num_layers):
            layer = _DenseLayer(num_input_features + i * growth_rate,
                                growth_rate,
                                bn_size,
                                drop_rate)
            self.add_module('denselayer%d' % (i + 1), layer)


class _Transition(nn.Sequential):
    def __init__(self, num_input_features, num_output_features):
        super(_Transition, self).__init__()
        self.add_module('norm', nn.BatchNorm2d(num_input_features))
        self.add_module('relu', nn.ReLU(inplace=True))
        self.add_module('conv', nn.Conv2d(num_input_features,
                                          num_output_features,
                                          kernel_size=1,
                                          stride=1,
                                          bias=False))
        self.add_module('pool', nn.AvgPool2d(kernel_size=2, stride=2))


class _DenseNet(nn.Module):
    """Densenet-BC model class.

    Based on `"Densely Connected Convolutional Networks" <https://arxiv.org/pdf/1608.06993.pdf>`

    :Args
        :growth_rate (int)
            how many filters to add each layer (`k` in paper)
        :block_config (list of 4 ints)
            how many layers in each pooling block
        :num_init_features (int)
            the number of filters to learn in the first convolution layer
        :bn_size (int)
            multiplicative factor for number of bottle neck layers (i.e.
            bn_size * k features in the bottleneck layer)
        :drop_rate (float)
            dropout rate after each dense layer
        :num_classes (int)
            number of classification classes
    """

    def __init__(self,
                 growth_rate=32,
                 block_config=(6, 12, 24, 16),
                 num_init_features=64,
                 bn_size=4,
                 drop_rate=0,
                 num_classes=1000):
        super(_DenseNet, self).__init__()

        # First convolution
        self.features = nn.Sequential(
            OrderedDict([
                ('conv0', nn.Conv2d(3,
                                    num_init_features,
                                    kernel_size=7,
                                    stride=2,
                                    padding=3,
                                    bias=False)),
                ('norm0', nn.BatchNorm2d(num_init_features)),
                ('relu0', nn.ReLU(inplace=True)),
                ('pool0', nn.MaxPool2d(kernel_size=3, stride=2, padding=1)),
            ])
        )

        # Each denseblock
        num_features = num_init_features
        for i, num_layers in enumerate(block_config):
            block = _DenseBlock(num_layers=num_layers,
                                num_input_features=num_features,
                                bn_size=bn_size,
                                growth_rate=growth_rate,
                                drop_rate=drop_rate)
            self.features.add_module('denseblock%d' % (i + 1), block)
            num_features = num_features + num_layers * growth_rate
            if i != len(block_config) - 1:
                trans = _Transition(num_input_features=num_features,
                                    num_output_features=num_features // 2)
                self.features.add_module('transition%d' % (i + 1), trans)
                num_features = num_features // 2

        # Final batch norm
        self.features.add_module('norm5', nn.BatchNorm2d(num_features))

        # Linear layer
        self.classifier = nn.Linear(num_features, num_classes)

        # Official init from torch repo.
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        features = self.features(x)
        out = F.relu(features, inplace=True)
        logger.info(out.size())
        out = F.adaptive_avg_pool2d(out, (1, 1)).view(features.size(0), -1)
        logger.info(out.size())
        out = self.classifier(out)
        return out


def densenet121(pretrained=False, **kwargs):
    """Densenet-121 model.

    From `"Densely Connected Convolutional Networks" <https://arxiv.org/pdf/1608.06993.pdf>`

    Args:
        :pretrained (bool)
            If True, returns a model pre-trained on ImageNet
    """
    model = _DenseNet(num_init_features=64,
                      growth_rate=32,
                      block_config=(6, 12, 24, 16),
                      **kwargs)
    if pretrained:
        # '.'s are no longer allowed in module names, but pervious _DenseLayer
        # has keys 'norm.1', 'relu.1', 'conv.1', 'norm.2', 'relu.2', 'conv.2'.
        # They are also in the checkpoints in model_urls. This pattern is used
        # to find such keys.
        pattern = re.compile(
            r'^(.*denselayer\d+\.(?:norm|relu|conv))\.((?:[12])\.(?:weight|bias|running_mean|running_var))$')
        state_dict = model_zoo.load_url('https://download.pytorch.org/models/densenet121-a639ec97.pth')
        for key in list(state_dict.keys()):
            res = pattern.match(key)
            if res:
                new_key = res.group(1) + res.group(2)
                state_dict[new_key] = state_dict[key]
                del state_dict[key]
        model.load_state_dict(state_dict)
    return model


class _DenseNet121(nn.Module):
    """Model modified.

    The architecture of our model is the same as standard DenseNet121
    except the classifier layer which has an additional sigmoid function.
    """

    def __init__(self, out_size, mode, drop_rate=0):
        super(_DenseNet121, self).__init__()
        assert mode in ('U-Ones', 'U-Zeros', 'U-MultiClass')
        self.densenet121 = densenet121(pretrained=True, drop_rate=drop_rate)
        num_ftrs = self.densenet121.classifier.in_features
        if mode in ('U-Ones', 'U-Zeros'):
            self.densenet121.classifier = nn.Sequential(
                nn.Linear(num_ftrs, out_size)
            )
        elif mode in ('U-MultiClass', ):
            self.densenet121.classifier = None
            self.densenet121.Linear_0 = nn.Linear(num_ftrs, out_size)
            self.densenet121.Linear_1 = nn.Linear(num_ftrs, out_size)
            self.densenet121.Linear_u = nn.Linear(num_ftrs, out_size)

        self.mode = mode

        # Official init from torch repo.
        for m in self.densenet121.modules():
            if isinstance(m, nn.Linear):
                nn.init.constant_(m.bias, 0)

        self.drop_rate = drop_rate
        self.drop_layer = nn.Dropout(p=drop_rate)

    def forward(self, x):
        features = self.densenet121.features(x)
        out = F.relu(features, inplace=True)

        out = F.adaptive_avg_pool2d(out, (1, 1)).view(features.size(0), -1)

        if self.drop_rate > 0:
            out = self.drop_layer(out)
        self.activations = out
        if self.mode in ('U-Ones', 'U-Zeros'):
            out = self.densenet121.classifier(out)
        elif self.mode in ('U-MultiClass', ):
            n_batch = x.size(0)
            out_0 = self.densenet121.Linear_0(out).view(n_batch, 1, -1)
            out_1 = self.densenet121.Linear_1(out).view(n_batch, 1, -1)
            out_u = self.densenet121.Linear_u(out).view(n_batch, 1, -1)
            out = torch.cat((out_0, out_1, out_u), dim=1)

        return self.activations, out


class _CheXpertDataset(Dataset):

    def __init__(self, root_dir, csv_file, transform=None):
        """.

        Args:
            data_dir: path to image directory.
            csv_file: path to the file containing images
                with corresponding labels.
            transform: optional transform to be applied on a sample.
        """
        super(_CheXpertDataset, self).__init__()
        file = pd.read_csv(csv_file)

        self.root_dir = root_dir
        self.images = file['ImageID'].values
        self.labels = file.iloc[:, 1:].values.astype(int)
        self.transform = transform

        logger.info('Total # images:{}, labels:{}'.format(
            len(self.images), len(self.labels)))

    def __getitem__(self, index):
        """.

        Args:
            index: the index of item
        Returns:
            image and its labels
        """
        items = self.images[index]  # .split('/')
        # study = items[2] + '/' + items[3]
        image_name = os.path.join(self.root_dir, self.images[index]) + '.jpg'
        image = Image.open(image_name).convert('RGB')
        label = self.labels[index]
        # logger.info(label)
        if self.transform is not None:
            image = self.transform(image)
        return items, index, image, torch.FloatTensor(label)

    def __len__(self):
        return len(self.images)


class _TransformTwice:
    def __init__(self, transform):
        self.transform = transform

    def __call__(self, inp):
        out1 = self.transform(inp)
        out2 = self.transform(inp)
        return out1, out2


class _LabelSmoothingCrossEntropy(object):
    def __init__(self, epsilon: float = 0.1, reduction: str = 'mean'):
        self.epsilon = epsilon
        self.reduction = reduction

        class_num = [141, 927, 679, 1125, 2136]
        class_weight = torch.Tensor([5000/i for i in class_num])
        if torch.cuda.is_available():
            class_weight = class_weight.cuda()
        self.base_loss = torch.nn.CrossEntropyLoss(reduction='mean', weight=class_weight)

    def _reduce_loss(self, loss: Tensor, reduction: str = 'mean'):
        if reduction == 'mean':
            return loss.mean()
        elif reduction == 'sum':
            return loss.sum()
        else:
            return loss

    def _linear_combination(self, x, y, epsilon):
        return epsilon * x + (1 - epsilon) * y

    def __call__(self, preds, target) -> Tensor:
        target = torch.argmax(target, dim=1)
        n = preds.size()[-1]
        log_preds = F.log_softmax(preds, dim=-1)
        loss = self._reduce_loss(-log_preds.sum(dim=-1), self.reduction)
        nll = F.nll_loss(log_preds, target.long(), reduction=self.reduction)
        return self._linear_combination(loss / n, nll, self.epsilon)


class DemoFedIRM(FedAvgScheduler):

    def __init__(self,
                 min_clients: int,
                 max_clients: int,
                 root_path: str,
                 csv_file_train: str,
                 csv_file_test: str,
                 name: str = None,
                 max_rounds: int = 0,
                 merge_epochs: int = 1,
                 calculation_timeout: int = 300,
                 perf_bench_timeout: int = 30,
                 schedule_timeout: int = 30,
                 log_rounds: int = 0,
                 is_centralized: bool = True,
                 is_deterministic: bool = True,
                 seed: int = 1337,
                 label_uncertainty: str = 'U-Ones',
                 drop_rate: float = 0.2,
                 batch_size: int = 16,
                 base_lr: float = 2e-4,
                 involve_aggregator: bool = False):
        super().__init__(min_clients=min_clients,
                         max_clients=max_clients,
                         name=name,
                         max_rounds=max_rounds,
                         merge_epochs=merge_epochs,
                         calculation_timeout=calculation_timeout,
                         perf_bench_timeout=perf_bench_timeout,
                         schedule_timeout=schedule_timeout,
                         log_rounds=log_rounds,
                         is_centralized=is_centralized,
                         involve_aggregator=involve_aggregator)
        self.is_deterministic = is_deterministic
        self.seed = seed
        self.label_uncertainty = label_uncertainty
        self.drop_rate = drop_rate
        self.root_path = root_path
        self.csv_file_train = csv_file_train
        self.csv_file_test = csv_file_test
        self.batch_size = batch_size
        self.base_lr = base_lr

        self.is_cuda = torch.cuda.is_available()
        # torch.backends.cudnn.enabled = self.is_cuda
        # if self.is_cuda and self.is_deterministic:
        #     cudnn.benchmark = False
        #     cudnn.deterministic = True
        #     torch.cuda.manual_seed(self.seed)

        self.epochs = 1

    def build_model(self) -> nn.Module:
        model = _DenseNet121(out_size=7,
                             mode=self.label_uncertainty,
                             drop_rate=self.drop_rate)
        model = model.cuda() if self.is_cuda else model
        return model

    def build_optimizer(self, model: nn.Module) -> Optimizer:
        assert self.model, 'must initialize model first'
        return Adam(self.model.parameters(),
                    lr=self.base_lr,
                    betas=(0.9, 0.999),
                    weight_decay=5e-4)

    def build_train_dataloader(self) -> DataLoader:
        normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        train_dataset = _CheXpertDataset(
            root_dir=self.root_path,
            csv_file=self.csv_file_train,
            transform=_TransformTwice(transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.RandomAffine(degrees=10, translate=(0.02, 0.02)),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                normalize,
            ]))
        )
        train_loader = DataLoader(dataset=train_dataset,
                                  batch_size=self.batch_size,
                                  shuffle=True)
        return train_loader

    def build_test_dataloader(self) -> DataLoader:
        normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        test_dataset = _CheXpertDataset(
            root_dir=self.root_path,
            csv_file=self.csv_file_test,
            transform=transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                normalize,
            ])
        )
        test_dataloader = DataLoader(dataset=test_dataset,
                                     batch_size=self.batch_size,
                                     shuffle=False,
                                     num_workers=4,
                                     pin_memory=True)
        return test_dataloader

    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self.model.state_dict()

    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        self.model.load_state_dict(state_dict)

    def train_an_epoch(self):
        self.model.train()

        lr = 3e-4 if self.epochs > 20 else self.base_lr
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr

        loss_fn = _LabelSmoothingCrossEntropy()

        for _, _, (image_batch, ema_image_batch), label_batch in self.train_loader:
            if self.is_cuda:
                image_batch = image_batch.cuda()
                ema_image_batch = ema_image_batch.cuda()
                label_batch = label_batch.cuda()
            _, outputs = self.model(image_batch)
            _, aug_outputs = self.model(ema_image_batch)
            loss = loss_fn(outputs, label_batch.long()) + loss_fn(aug_outputs, label_batch.long())
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        self.epochs += 1

    def _compute_metrics_test(self, gt, pred, thresh):
        """Compute accuracy, precision, recall and F1-score from prediction scores.

        Args:
            gt:
                Pytorch tensor on GPU, shape = [n_samples, n_classes] true binary labels.
            pred:
                Pytorch tensor on GPU, shape = [n_samples, n_classes]
                can either be probability estimates of the positive class,
                confidence values, or binary decisions.
        Returns:
            List of AUROCs of all classes.
        """
        AUROCs, Accus, Senss, Specs, Pre, F1 = [], [], [], [], [], []
        gt_np = gt.cpu().detach().numpy()
        pred_np = pred.cpu().detach().numpy()

        class_names = [
            'Melanoma',
            'Melanocytic nevus',
            'Basal cell carcinoma',
            'Actinic keratosis',
            'Benign keratosis',
            'Dermatofibroma',
            'Vascular lesion'
        ]

        for i, cls in enumerate(class_names):
            try:
                AUROCs.append(roc_auc_score(gt_np[:, i], pred_np[:, i]))
            except ValueError as error:
                logger.info('Error in computing accuracy for {}.\n Error msg:{}'.format(i, error))
                AUROCs.append(0)

            try:
                Accus.append(accuracy_score(gt_np[:, i], (pred_np[:, i] >= thresh)))
            except ValueError as error:
                logger.info('Error in computing accuracy for {}.\n Error msg:{}'.format(i, error))
                Accus.append(0)

            try:
                Senss.append(sensitivity_score(gt_np[:, i], (pred_np[:, i] >= thresh)))
            except ValueError:
                logger.info('Error in computing precision for {}.'.format(i))
                Senss.append(0)

            try:
                Specs.append(specificity_score(gt_np[:, i], (pred_np[:, i] >= thresh)))
            except ValueError:
                logger.info('Error in computing F1-score for {}.'.format(i))
                Specs.append(0)

            try:
                Pre.append(precision_score(gt_np[:, i], (pred_np[:, i] >= thresh)))
            except ValueError:
                logger.info('Error in computing F1-score for {}.'.format(i))
                Pre.append(0)

            try:
                F1.append(f1_score(gt_np[:, i], (pred_np[:, i] >= thresh)))
            except ValueError:
                logger.info('Error in computing F1-score for {}.'.format(i))
                F1.append(0)

        return AUROCs, Accus, Senss, Specs, Pre, F1

    def _epochVal_metrics_test(self, data_loader: DataLoader, thresh: float):
        training = self.model.training
        self.model.eval()

        gt = torch.FloatTensor()
        pred = torch.FloatTensor()
        if self.is_cuda:
            gt, pred = gt.cuda(), pred.cuda()

        gt_study = {}
        pred_study = {}
        studies = []

        with torch.no_grad():
            for i, (study, _, image, label) in enumerate(data_loader):
                if self.is_cuda:
                    image, label = image.cuda(), label.cuda()
                _, output = self.model(image)

                output = F.softmax(output, dim=1)

                for i in range(len(study)):
                    if study[i] in pred_study:
                        assert torch.equal(gt_study[study[i]], label[i])
                        pred_study[study[i]] = torch.max(
                            pred_study[study[i]], output[i])
                    else:
                        gt_study[study[i]] = label[i]
                        pred_study[study[i]] = output[i]
                        studies.append(study[i])

            for study in studies:
                gt = torch.cat((gt, gt_study[study].view(1, -1)), 0)
                pred = torch.cat((pred, pred_study[study].view(1, -1)), 0)

            AUROCs, Accus, Senss, Specs, pre, F1 = self._compute_metrics_test(
                gt, pred, thresh=thresh)

        self.model.train(training)

        return AUROCs, Accus, Senss, Specs, pre, F1

    def test(self):
        normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        test_dataset = _CheXpertDataset(
            root_dir=self.root_path,
            csv_file=self.csv_file_test,
            transform=transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                normalize,
            ])
        )
        test_dataloader = DataLoader(dataset=test_dataset,
                                     batch_size=self.batch_size,
                                     shuffle=False,
                                     num_workers=4,
                                     pin_memory=True)
        AUROCs, Accus, Senss, Specs, pre, F1 = self._epochVal_metrics_test(
            data_loader=test_dataloader, thresh=0.4
        )
        AUROC_avg = np.array(AUROCs).mean()
        Accus_avg = np.array(Accus).mean()
        Senss_avg = np.array(Senss).mean()
        Specs_avg = np.array(Specs).mean()

        result_str = ', '.join((f'AUROC: {AUROC_avg:6f}',
                                f'TEST Accus: {Accus_avg:6f}',
                                f'TEST Senss: {Senss_avg:6f}',
                                f'TEST Specs: {Specs_avg:6f}',
                                f'pre: {pre}',
                                f'F1: {F1}'))
        logger.info(f'Test after training: {result_str}')

        self.tb_writer.add_scalar('test_results/AUROC', AUROC_avg, self.current_round)
        self.tb_writer.add_scalar('test_results/Accus', Accus_avg, self.current_round)
        self.tb_writer.add_scalar('test_results/Senss', Senss_avg, self.current_round)
        self.tb_writer.add_scalar('test_results/Specs', Specs_avg, self.current_round)
        self.tb_writer.add_scalar('test_results/pre', pre, self.current_round)
        self.tb_writer.add_scalar('test_results/F1', F1, self.current_round)

    def validate_context(self):
        super().validate_context()
        assert self.train_loader and len(self.train_loader) > 0
        assert self.test_loader and len(self.test_loader) > 0
