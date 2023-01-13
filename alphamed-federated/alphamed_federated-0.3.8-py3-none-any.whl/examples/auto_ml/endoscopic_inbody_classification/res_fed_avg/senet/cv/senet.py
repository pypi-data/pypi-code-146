"""Pretraining SeNet models and schedulers.

Reference: https://arxiv.org/abs/1709.01507
"""

import math
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type, Union

import torch
from torch import nn

from ..convolutions import Convolution
from ..layer_factories import Act, Conv, Dropout, Norm, Pool, split_args


class ChannelSELayer(nn.Module):
    """Re-implementation of the Squeeze-and-Excitation block.

    Based on:
    "Hu et al., Squeeze-and-Excitation Networks, https://arxiv.org/abs/1709.01507".
    """

    def __init__(
        self,
        spatial_dims: int,
        in_channels: int,
        r: int = 2,
        acti_type_1: Union[Tuple[str, Dict], str] = ("relu", {"inplace": True}),
        acti_type_2: Union[Tuple[str, Dict], str] = "sigmoid",
        add_residual: bool = False,
    ) -> None:
        """.

        Args:
            spatial_dims: number of spatial dimensions, could be 1, 2, or 3.
            in_channels: number of input channels.
            r: the reduction ratio r in the paper. Defaults to 2.
            acti_type_1: activation type of the hidden squeeze layer. Defaults to ``("relu", {"inplace": True})``.
            acti_type_2: activation type of the output squeeze layer. Defaults to "sigmoid".

        Raises:
            ValueError: When ``r`` is nonpositive or larger than ``in_channels``.
        """
        super().__init__()

        self.add_residual = add_residual

        pool_type = Pool[Pool.ADAPTIVEAVG, spatial_dims]
        self.avg_pool = pool_type(1)  # spatial size (1, 1, ...)

        channels = int(in_channels // r)
        if channels <= 0:
            raise ValueError(f"r must be positive and smaller than in_channels, got r={r} in_channels={in_channels}.")

        act_1, act_1_args = split_args(acti_type_1)
        act_2, act_2_args = split_args(acti_type_2)
        self.fc = nn.Sequential(
            nn.Linear(in_channels, channels, bias=True),
            Act[act_1](**act_1_args),
            nn.Linear(channels, in_channels, bias=True),
            Act[act_2](**act_2_args),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """.

        Args:
            x: in shape (batch, in_channels, spatial_1[, spatial_2, ...]).
        """
        b, c = x.shape[:2]
        y: torch.Tensor = self.avg_pool(x).view(b, c)
        y = self.fc(y).view([b, c] + [1] * (x.ndim - 2))
        result = x * y

        # Residual connection is moved here instead of providing an override of forward in ResidualSELayer since
        # Torchscript has an issue with using super().
        if self.add_residual:
            result += x

        return result


class SEBlock(nn.Module):
    """Residual module enhanced with Squeeze-and-Excitation.

        ----+- conv1 --  conv2 -- conv3 -- SE -o---
            |                                  |
            +---(channel project if needed)----+

    Re-implementation of the SE-Resnet block based on:
    "Hu et al., Squeeze-and-Excitation Networks, https://arxiv.org/abs/1709.01507".
    """

    def __init__(
        self,
        spatial_dims: int,
        in_channels: int,
        n_chns_1: int,
        n_chns_2: int,
        n_chns_3: int,
        conv_param_1: Optional[Dict] = None,
        conv_param_2: Optional[Dict] = None,
        conv_param_3: Optional[Dict] = None,
        project: Optional[Convolution] = None,
        r: int = 2,
        acti_type_1: Union[Tuple[str, Dict], str] = ("relu", {"inplace": True}),
        acti_type_2: Union[Tuple[str, Dict], str] = "sigmoid",
        acti_type_final: Optional[Union[Tuple[str, Dict], str]] = ("relu", {"inplace": True}),
    ):
        """.

        Args:
            spatial_dims: number of spatial dimensions, could be 1, 2, or 3.
            in_channels: number of input channels.
            n_chns_1: number of output channels in the 1st convolution.
            n_chns_2: number of output channels in the 2nd convolution.
            n_chns_3: number of output channels in the 3rd convolution.
            conv_param_1: additional parameters to the 1st convolution.
                Defaults to ``{"kernel_size": 1, "norm": Norm.BATCH, "act": ("relu", {"inplace": True})}``
            conv_param_2: additional parameters to the 2nd convolution.
                Defaults to ``{"kernel_size": 3, "norm": Norm.BATCH, "act": ("relu", {"inplace": True})}``
            conv_param_3: additional parameters to the 3rd convolution.
                Defaults to ``{"kernel_size": 1, "norm": Norm.BATCH, "act": None}``
            project: in the case of residual chns and output chns doesn't match, a project
                (Conv) layer/block is used to adjust the number of chns. In SENET, it is
                consisted with a Conv layer as well as a Norm layer.
                Defaults to None (chns are matchable) or a Conv layer with kernel size 1.
            r: the reduction ratio r in the paper. Defaults to 2.
            acti_type_1: activation type of the hidden squeeze layer. Defaults to "relu".
            acti_type_2: activation type of the output squeeze layer. Defaults to "sigmoid".
            acti_type_final: activation type of the end of the block. Defaults to "relu".
        """
        super().__init__()

        if not conv_param_1:
            conv_param_1 = {"kernel_size": 1, "norm": Norm.BATCH, "act": ("relu", {"inplace": True})}
        self.conv1 = Convolution(
            spatial_dims=spatial_dims, in_channels=in_channels, out_channels=n_chns_1, **conv_param_1
        )

        if not conv_param_2:
            conv_param_2 = {"kernel_size": 3, "norm": Norm.BATCH, "act": ("relu", {"inplace": True})}
        self.conv2 = Convolution(spatial_dims=spatial_dims, in_channels=n_chns_1, out_channels=n_chns_2, **conv_param_2)

        if not conv_param_3:
            conv_param_3 = {"kernel_size": 1, "norm": Norm.BATCH, "act": None}
        self.conv3 = Convolution(spatial_dims=spatial_dims, in_channels=n_chns_2, out_channels=n_chns_3, **conv_param_3)

        self.se_layer = ChannelSELayer(
            spatial_dims=spatial_dims, in_channels=n_chns_3, r=r, acti_type_1=acti_type_1, acti_type_2=acti_type_2
        )

        if project is None and in_channels != n_chns_3:
            self.project = Conv[Conv.CONV, spatial_dims](in_channels, n_chns_3, kernel_size=1)
        elif project is None:
            self.project = nn.Identity()
        else:
            self.project = project

        if acti_type_final is not None:
            act_final, act_final_args = split_args(acti_type_final)
            self.act = Act[act_final](**act_final_args)
        else:
            self.act = nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """.

        Args:
            x: in shape (batch, in_channels, spatial_1[, spatial_2, ...]).
        """
        residual = self.project(x)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.se_layer(x)
        x += residual
        x = self.act(x)
        return x


class SEBottleneck(SEBlock):
    """Bottleneck for SENet."""

    expansion = 4

    def __init__(
        self,
        spatial_dims: int,
        inplanes: int,
        planes: int,
        groups: int,
        reduction: int,
        stride: int = 1,
        downsample: Optional[Convolution] = None,
    ) -> None:

        conv_param_1 = {
            "strides": 1,
            "kernel_size": 1,
            "act": ("relu", {"inplace": True}),
            "norm": Norm.BATCH,
            "bias": False,
        }
        conv_param_2 = {
            "strides": stride,
            "kernel_size": 3,
            "act": ("relu", {"inplace": True}),
            "norm": Norm.BATCH,
            "groups": groups,
            "bias": False,
        }
        conv_param_3 = {"strides": 1, "kernel_size": 1, "act": None, "norm": Norm.BATCH, "bias": False}

        super().__init__(
            spatial_dims=spatial_dims,
            in_channels=inplanes,
            n_chns_1=planes * 2,
            n_chns_2=planes * 4,
            n_chns_3=planes * 4,
            conv_param_1=conv_param_1,
            conv_param_2=conv_param_2,
            conv_param_3=conv_param_3,
            project=downsample,
            r=reduction,
        )


class SEResNetBottleneck(SEBlock):
    """ResNet bottleneck with a Squeeze-and-Excitation module.

    It follows Caffe implementation and uses `strides=stride` in `conv1` and not in `conv2`
    (the latter is used in the torchvision implementation of ResNet).
    """

    expansion = 4

    def __init__(
        self,
        spatial_dims: int,
        inplanes: int,
        planes: int,
        groups: int,
        reduction: int,
        stride: int = 1,
        downsample: Optional[Convolution] = None,
    ) -> None:

        conv_param_1 = {
            "strides": stride,
            "kernel_size": 1,
            "act": ("relu", {"inplace": True}),
            "norm": Norm.BATCH,
            "bias": False,
        }
        conv_param_2 = {
            "strides": 1,
            "kernel_size": 3,
            "act": ("relu", {"inplace": True}),
            "norm": Norm.BATCH,
            "groups": groups,
            "bias": False,
        }
        conv_param_3 = {"strides": 1, "kernel_size": 1, "act": None, "norm": Norm.BATCH, "bias": False}

        super().__init__(
            spatial_dims=spatial_dims,
            in_channels=inplanes,
            n_chns_1=planes,
            n_chns_2=planes,
            n_chns_3=planes * 4,
            conv_param_1=conv_param_1,
            conv_param_2=conv_param_2,
            conv_param_3=conv_param_3,
            project=downsample,
            r=reduction,
        )


class SEResNeXtBottleneck(SEBlock):
    """ResNeXt bottleneck type C with a Squeeze-and-Excitation module."""

    expansion = 4

    def __init__(
        self,
        spatial_dims: int,
        inplanes: int,
        planes: int,
        groups: int,
        reduction: int,
        stride: int = 1,
        downsample: Optional[Convolution] = None,
        base_width: int = 4,
    ) -> None:

        conv_param_1 = {
            "strides": 1,
            "kernel_size": 1,
            "act": ("relu", {"inplace": True}),
            "norm": Norm.BATCH,
            "bias": False,
        }
        conv_param_2 = {
            "strides": stride,
            "kernel_size": 3,
            "act": ("relu", {"inplace": True}),
            "norm": Norm.BATCH,
            "groups": groups,
            "bias": False,
        }
        conv_param_3 = {"strides": 1, "kernel_size": 1, "act": None, "norm": Norm.BATCH, "bias": False}
        width = math.floor(planes * (base_width / 64)) * groups

        super().__init__(
            spatial_dims=spatial_dims,
            in_channels=inplanes,
            n_chns_1=width,
            n_chns_2=width,
            n_chns_3=planes * 4,
            conv_param_1=conv_param_1,
            conv_param_2=conv_param_2,
            conv_param_3=conv_param_3,
            project=downsample,
            r=reduction,
        )


class SENet(nn.Module):
    """SENet based on `Squeeze-and-Excitation Networks <https://arxiv.org/pdf/1709.01507.pdf>`_.

    Adapted from `Cadene Hub 2D version
    <https://github.com/Cadene/pretrained-models.pytorch/blob/master/pretrainedmodels/models/senet.py>`_.

    Args:
        spatial_dims: spatial dimension of the input data.
        in_channels: channel number of the input data.
        block: SEBlock class or str.
            for SENet154: SEBottleneck or 'se_bottleneck'
            for SE-ResNet models: SEResNetBottleneck or 'se_resnet_bottleneck'
            for SE-ResNeXt models:  SEResNeXtBottleneck or 'se_resnetxt_bottleneck'
        layers: number of residual blocks for 4 layers of the network (layer1...layer4).
        groups: number of groups for the 3x3 convolution in each bottleneck block.
            for SENet154: 64
            for SE-ResNet models: 1
            for SE-ResNeXt models:  32
        reduction: reduction ratio for Squeeze-and-Excitation modules.
            for all models: 16
        dropout_prob: drop probability for the Dropout layer.
            if `None` the Dropout layer is not used.
            for SENet154: 0.2
            for SE-ResNet models: None
            for SE-ResNeXt models: None
        dropout_dim: determine the dimensions of dropout. Defaults to 1.
            When dropout_dim = 1, randomly zeroes some of the elements for each channel.
            When dropout_dim = 2, Randomly zeroes out entire channels (a channel is a 2D feature map).
            When dropout_dim = 3, Randomly zeroes out entire channels (a channel is a 3D feature map).
        inplanes:  number of input channels for layer1.
            for SENet154: 128
            for SE-ResNet models: 64
            for SE-ResNeXt models: 64
        downsample_kernel_size: kernel size for downsampling convolutions in layer2, layer3 and layer4.
            for SENet154: 3
            for SE-ResNet models: 1
            for SE-ResNeXt models: 1
        input_3x3: If `True`, use three 3x3 convolutions instead of
            a single 7x7 convolution in layer0.
            - For SENet154: True
            - For SE-ResNet models: False
            - For SE-ResNeXt models: False
        num_classes: number of outputs in `last_linear` layer.
            for all models: 1000
    """

    def __init__(
        self,
        spatial_dims: int,
        in_channels: int,
        block: Union[Type[Union[SEBottleneck, SEResNetBottleneck, SEResNeXtBottleneck]], str],
        layers: Sequence[int],
        groups: int,
        reduction: int,
        dropout_prob: Optional[float] = 0.2,
        dropout_dim: int = 1,
        inplanes: int = 128,
        downsample_kernel_size: int = 3,
        input_3x3: bool = True,
        num_classes: int = 1000,
    ) -> None:

        super().__init__()

        if isinstance(block, str):
            if block == "se_bottleneck":
                block = SEBottleneck
            elif block == "se_resnet_bottleneck":
                block = SEResNetBottleneck
            elif block == "se_resnetxt_bottleneck":
                block = SEResNeXtBottleneck
            else:
                raise ValueError(
                    "Unknown block '%s', use se_bottleneck, se_resnet_bottleneck or se_resnetxt_bottleneck" % block
                )

        relu_type: Type[nn.ReLU]
        relu_type = Act[Act.RELU]
        conv_type: Type[Union[nn.Conv1d, nn.Conv2d, nn.Conv3d]]
        conv_type = Conv[Conv.CONV, spatial_dims]
        pool_type: Type[Union[nn.MaxPool1d, nn.MaxPool2d, nn.MaxPool3d]]
        pool_type = Pool[Pool.MAX, spatial_dims]
        norm_type: Type[Union[nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d]]
        norm_type = Norm[Norm.BATCH, spatial_dims]
        dropout_type: Type[Union[nn.Dropout, nn.Dropout2d, nn.Dropout3d]]
        dropout_type = Dropout[Dropout.DROPOUT, dropout_dim]
        avg_pool_type: Type[Union[nn.AdaptiveAvgPool1d, nn.AdaptiveAvgPool2d, nn.AdaptiveAvgPool3d]]
        avg_pool_type = Pool[Pool.ADAPTIVEAVG, spatial_dims]

        self.inplanes = inplanes
        self.spatial_dims = spatial_dims

        layer0_modules: List[Tuple[str, Any]]

        if input_3x3:
            layer0_modules = [
                ("conv1", conv_type(in_channels=in_channels,
                                    out_channels=64,
                                    kernel_size=3,
                                    stride=2,
                                    padding=1,
                                    bias=False)),
                ("bn1", norm_type(num_features=64)),
                ("relu1", relu_type(inplace=True)),
                ("conv2", conv_type(in_channels=64,
                                    out_channels=64,
                                    kernel_size=3,
                                    stride=1,
                                    padding=1,
                                    bias=False)),
                ("bn2", norm_type(num_features=64)),
                ("relu2", relu_type(inplace=True)),
                ("conv3", conv_type(in_channels=64,
                                    out_channels=inplanes,
                                    kernel_size=3,
                                    stride=1,
                                    padding=1,
                                    bias=False)),
                ("bn3", norm_type(num_features=inplanes)),
                ("relu3", relu_type(inplace=True)),
            ]
        else:
            layer0_modules = [
                ("conv1", conv_type(in_channels=in_channels,
                                    out_channels=inplanes,
                                    kernel_size=7,
                                    stride=2,
                                    padding=3,
                                    bias=False)),
                ("bn1", norm_type(num_features=inplanes)),
                ("relu1", relu_type(inplace=True)),
            ]

        layer0_modules.append(("pool", pool_type(kernel_size=3, stride=2, ceil_mode=True)))
        self.layer0 = nn.Sequential(OrderedDict(layer0_modules))
        self.layer1 = self._make_layer(block,
                                       planes=64,
                                       blocks=layers[0],
                                       groups=groups,
                                       reduction=reduction,
                                       downsample_kernel_size=1)
        self.layer2 = self._make_layer(block,
                                       planes=128,
                                       blocks=layers[1],
                                       stride=2,
                                       groups=groups,
                                       reduction=reduction,
                                       downsample_kernel_size=downsample_kernel_size)
        self.layer3 = self._make_layer(block,
                                       planes=256,
                                       blocks=layers[2],
                                       stride=2,
                                       groups=groups,
                                       reduction=reduction,
                                       downsample_kernel_size=downsample_kernel_size)
        self.layer4 = self._make_layer(block,
                                       planes=512,
                                       blocks=layers[3],
                                       stride=2,
                                       groups=groups,
                                       reduction=reduction,
                                       downsample_kernel_size=downsample_kernel_size)
        self.adaptive_avg_pool = avg_pool_type(1)
        self.dropout = dropout_type(dropout_prob) if dropout_prob is not None else None
        self.last_linear = nn.Linear(512 * block.expansion, num_classes)

        for m in self.modules():
            if isinstance(m, conv_type):
                nn.init.kaiming_normal_(torch.as_tensor(m.weight))
            elif isinstance(m, norm_type):
                nn.init.constant_(torch.as_tensor(m.weight), 1)
                nn.init.constant_(torch.as_tensor(m.bias), 0)
            elif isinstance(m, nn.Linear):
                nn.init.constant_(torch.as_tensor(m.bias), 0)

    def _make_layer(
        self,
        block: Type[Union[SEBottleneck, SEResNetBottleneck, SEResNeXtBottleneck]],
        planes: int,
        blocks: int,
        groups: int,
        reduction: int,
        stride: int = 1,
        downsample_kernel_size: int = 1,
    ) -> nn.Sequential:

        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = Convolution(
                spatial_dims=self.spatial_dims,
                in_channels=self.inplanes,
                out_channels=planes * block.expansion,
                strides=stride,
                kernel_size=downsample_kernel_size,
                act=None,
                norm=Norm.BATCH,
                bias=False,
            )

        layers = []
        layers.append(
            block(
                spatial_dims=self.spatial_dims,
                inplanes=self.inplanes,
                planes=planes,
                groups=groups,
                reduction=reduction,
                stride=stride,
                downsample=downsample,
            )
        )
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(
                block(
                    spatial_dims=self.spatial_dims,
                    inplanes=self.inplanes,
                    planes=planes,
                    groups=groups,
                    reduction=reduction,
                )
            )

        return nn.Sequential(*layers)

    def features(self, x: torch.Tensor):
        x = self.layer0(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        return x

    def logits(self, x: torch.Tensor):
        x = self.adaptive_avg_pool(x)
        if self.dropout is not None:
            x = self.dropout(x)
        x = torch.flatten(x, 1)
        x = self.last_linear(x)
        return x

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.logits(x)
        return x


class SEResNet50(SENet):
    """SEResNet50.

    Based on `Squeeze-and-Excitation Networks` with optional pretrained support
    when spatial_dims is 2.
    """

    def __init__(
        self,
        spatial_dims: int,
        in_channels: int,
        num_classes: int = 2,
        layers: Sequence[int] = (3, 4, 6, 3),
        groups: int = 1,
        reduction: int = 16,
        dropout_prob: Optional[float] = None,
        inplanes: int = 64,
        downsample_kernel_size: int = 1,
        input_3x3: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(
            spatial_dims=spatial_dims,
            in_channels=in_channels,
            num_classes=num_classes,
            block=SEResNetBottleneck,
            layers=layers,
            groups=groups,
            reduction=reduction,
            dropout_prob=dropout_prob,
            inplanes=inplanes,
            downsample_kernel_size=downsample_kernel_size,
            input_3x3=input_3x3,
            **kwargs,
        )
