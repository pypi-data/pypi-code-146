import inspect
from typing import Any, Iterable, Optional, Sequence, Tuple, Union

import numpy as np
import torch
from torch import nn

from .layer_factories import Act, Conv, Dropout, Norm, split_args


def same_padding(kernel_size: Union[Sequence[int], int],
                 dilation: Union[Sequence[int], int] = 1) -> Union[Tuple[int, ...], int]:
    """Return the padding sive to get an same shape output as the input.

    Return the padding value needed to ensure a convolution using the given kernel size
    produces an output of the same shape as the input for a stride of 1, otherwise ensure
    a shape of the input divided by the stride rounded down.

    Raises:
        NotImplementedError: When ``np.any((kernel_size - 1) * dilation % 2 == 1)``.
    """
    kernel_size_np = np.atleast_1d(kernel_size)
    dilation_np = np.atleast_1d(dilation)

    if np.any((kernel_size_np - 1) * dilation % 2 == 1):
        raise NotImplementedError(
            f"Same padding not available for kernel_size={kernel_size_np} and dilation={dilation_np}."
        )

    padding_np = (kernel_size_np - 1) / 2 * dilation_np
    padding = tuple(int(p) for p in padding_np)

    return padding if len(padding) > 1 else padding[0]


def stride_minus_kernel_padding(kernel_size: Union[Sequence[int], int],
                                stride: Union[Sequence[int], int]) -> Union[Tuple[int, ...], int]:
    kernel_size_np = np.atleast_1d(kernel_size)
    stride_np = np.atleast_1d(stride)

    out_padding_np = stride_np - kernel_size_np
    out_padding = tuple(int(p) for p in out_padding_np)

    return out_padding if len(out_padding) > 1 else out_padding[0]


def issequenceiterable(obj: Any) -> bool:
    """Determine if the object is an iterable sequence and is not a string."""
    try:
        if hasattr(obj, "ndim") and obj.ndim == 0:
            return False  # a 0-d tensor is not iterable
    except Exception:
        return False
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))


def ensure_tuple(vals: Any, wrap_array: bool = False) -> Tuple[Any, ...]:
    """Return a tuple of `vals`.

    Args:
        vals:
            input data to convert to a tuple.
        wrap_array:
            if `True`, treat the input numerical array (ndarray/tensor) as one item of the tuple.
            if `False`, try to convert the array with `tuple(vals)`, default to `False`.
    """
    if wrap_array and isinstance(vals, (np.ndarray, torch.Tensor)):
        return (vals,)
    return tuple(vals) if issequenceiterable(vals) else (vals,)


def has_option(obj, keywords: Union[str, Sequence[str]]) -> bool:
    """Return a boolean indicating whether the given callable `obj` has the `keywords` in its signature."""
    if not callable(obj):
        return False
    sig = inspect.signature(obj)
    return all(key in sig.parameters for key in ensure_tuple(keywords))


def get_norm_layer(name: Union[Tuple, str],
                   spatial_dims: Optional[int] = 1,
                   channels: Optional[int] = 1):
    """Create a normalization layer instance.

    For example, to create normalization layers:

    .. code-block:: python

        from monai.networks.layers import get_norm_layer

        g_layer = get_norm_layer(name=("group", {"num_groups": 1}))
        n_layer = get_norm_layer(name="instance", spatial_dims=2)

    Args:
        name: a normalization type string or a tuple of type string and parameters.
        spatial_dims: number of spatial dimensions of the input.
        channels: number of features/channels when the normalization layer requires this parameter
            but it is not specified in the norm parameters.
    """
    if name == "":
        return nn.Identity()
    norm_name, norm_args = split_args(name)
    norm_type = Norm[norm_name, spatial_dims]
    kw_args = dict(norm_args)
    if has_option(norm_type, "num_features") and "num_features" not in kw_args:
        kw_args["num_features"] = channels
    if has_option(norm_type, "num_channels") and "num_channels" not in kw_args:
        kw_args["num_channels"] = channels
    return norm_type(**kw_args)


def get_act_layer(name: Union[Tuple, str]):
    """Create an activation layer instance.

    For example, to create activation layers:

    .. code-block:: python

        from monai.networks.layers import get_act_layer

        s_layer = get_act_layer(name="swish")
        p_layer = get_act_layer(name=("prelu", {"num_parameters": 1, "init": 0.25}))

    Args:
        name: an activation type string or a tuple of type string and parameters.
    """
    if name == "":
        return torch.nn.Identity()
    act_name, act_args = split_args(name)
    act_type = Act[act_name]
    return act_type(**act_args)


def get_dropout_layer(name: Union[Tuple, str, float, int], dropout_dim: Optional[int] = 1):
    """Create a dropout layer instance.

    For example, to create dropout layers:

    .. code-block:: python

        from monai.networks.layers import get_dropout_layer

        d_layer = get_dropout_layer(name="dropout")
        a_layer = get_dropout_layer(name=("alphadropout", {"p": 0.25}))

    Args:
        name: a dropout ratio or a tuple of dropout type and parameters.
        dropout_dim: the spatial dimension of the dropout operation.
    """
    if name == "":
        return torch.nn.Identity()
    if isinstance(name, (int, float)):
        # if dropout was specified simply as a p value, use default name and make a keyword map with the value
        drop_name = Dropout.DROPOUT
        drop_args = {"p": float(name)}
    else:
        drop_name, drop_args = split_args(name)
    drop_type = Dropout[drop_name, dropout_dim]
    return drop_type(**drop_args)


class ADN(nn.Sequential):
    """Constructs an ADN Module.

    Constructs a sequential module of optional activation (A), dropout (D), and normalization
    (N) layers with an arbitrary order.

        -- (Norm) -- (Dropout) -- (Acti) --

    Args:
        ordering: a string representing the ordering of activation, dropout, and normalization. Defaults to "NDA".
        in_channels: `C` from an expected input of size (N, C, H[, W, D]).
        act: activation type and arguments. Defaults to PReLU.
        norm: feature normalization type and arguments. Defaults to instance norm.
        norm_dim: determine the spatial dimensions of the normalization layer.
            defaults to `dropout_dim` if unspecified.
        dropout: dropout ratio. Defaults to no dropout.
        dropout_dim: determine the spatial dimensions of dropout.
            defaults to `norm_dim` if unspecified.

            - When dropout_dim = 1, randomly zeroes some of the elements for each channel.
            - When dropout_dim = 2, Randomly zeroes out entire channels (a channel is a 2D feature map).
            - When dropout_dim = 3, Randomly zeroes out entire channels (a channel is a 3D feature map).

    Examples::
        # activation, group norm, dropout
        >>> norm_params = ("GROUP", {"num_groups": 1, "affine": False})
        >>> ADN(norm=norm_params, in_channels=1, dropout_dim=1, dropout=0.8, ordering="AND")
        ADN(
            (A): ReLU()
            (N): GroupNorm(1, 1, eps=1e-05, affine=False)
            (D): Dropout(p=0.8, inplace=False)
        )

        # LeakyReLU, dropout
        >>> act_params = ("leakyrelu", {"negative_slope": 0.1, "inplace": True})
        >>> ADN(act=act_params, in_channels=1, dropout_dim=1, dropout=0.8, ordering="AD")
        ADN(
            (A): LeakyReLU(negative_slope=0.1, inplace=True)
            (D): Dropout(p=0.8, inplace=False)
        )
    """

    def __init__(
        self,
        ordering: str = "NDA",
        in_channels: Optional[int] = None,
        act: Optional[Union[Tuple, str]] = "RELU",
        norm: Optional[Union[Tuple, str]] = None,
        norm_dim: Optional[int] = None,
        dropout: Optional[Union[Tuple, str, float]] = None,
        dropout_dim: Optional[int] = None,
    ) -> None:
        super().__init__()

        op_dict = {"A": None, "D": None, "N": None}
        # define the normalization type and the arguments to the constructor
        if norm is not None:
            if norm_dim is None and dropout_dim is None:
                raise ValueError("norm_dim or dropout_dim needs to be specified.")
            op_dict["N"] = get_norm_layer(name=norm, spatial_dims=norm_dim or dropout_dim, channels=in_channels)

        # define the activation type and the arguments to the constructor
        if act is not None:
            op_dict["A"] = get_act_layer(act)

        if dropout is not None:
            if norm_dim is None and dropout_dim is None:
                raise ValueError("norm_dim or dropout_dim needs to be specified.")
            op_dict["D"] = get_dropout_layer(name=dropout, dropout_dim=dropout_dim or norm_dim)

        for item in ordering.upper():
            if item not in op_dict:
                raise ValueError(f"ordering must be a string of {op_dict}, got {item} in it.")
            if op_dict[item] is not None:
                self.add_module(item, op_dict[item])


class Convolution(nn.Sequential):
    """Constructs a convolution with normalization, optional dropout, and optional activation layers.

        -- (Conv|ConvTrans) -- (Norm -- Dropout -- Acti) --

    if ``conv_only`` set to ``True``::

        -- (Conv|ConvTrans) --

    For example:
    .. code-block:: python

        from monai.networks.blocks import Convolution

        conv = Convolution(
            spatial_dims=3,
            in_channels=1,
            out_channels=1,
            adn_ordering="ADN",
            act=("prelu", {"init": 0.2}),
            dropout=0.1,
            norm=("layer", {"normalized_shape": (10, 10, 10)}),
        )
        print(conv)

    output::
        Convolution(
          (conv): Conv3d(1, 1, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=(1, 1, 1))
          (adn): ADN(
            (A): PReLU(num_parameters=1)
            (D): Dropout(p=0.1, inplace=False)
            (N): LayerNorm((10, 10, 10), eps=1e-05, elementwise_affine=True)
          )
        )

    Args:
        spatial_dims: number of spatial dimensions.
        in_channels: number of input channels.
        out_channels: number of output channels.
        strides: convolution stride. Defaults to 1.
        kernel_size: convolution kernel size. Defaults to 3.
        adn_ordering: a string representing the ordering of activation, normalization, and dropout.
            Defaults to "NDA".
        act: activation type and arguments. Defaults to PReLU.
        norm: feature normalization type and arguments. Defaults to instance norm.
        dropout: dropout ratio. Defaults to no dropout.
        dropout_dim: determine the spatial dimensions of dropout. Defaults to 1.

            - When dropout_dim = 1, randomly zeroes some of the elements for each channel.
            - When dropout_dim = 2, Randomly zeroes out entire channels (a channel is a 2D feature map).
            - When dropout_dim = 3, Randomly zeroes out entire channels (a channel is a 3D feature map).

            The value of dropout_dim should be no larger than the value of `spatial_dims`.
        dilation: dilation rate. Defaults to 1.
        groups: controls the connections between inputs and outputs. Defaults to 1.
        bias: whether to have a bias term. Defaults to True.
        conv_only: whether to use the convolutional layer only. Defaults to False.
        is_transposed: if True uses ConvTrans instead of Conv. Defaults to False.
        padding: controls the amount of implicit zero-paddings on both sides for padding number of points
            for each dimension. Defaults to None.
        output_padding: controls the additional size added to one side of the output shape.
            Defaults to None.
    """

    def __init__(
        self,
        spatial_dims: int,
        in_channels: int,
        out_channels: int,
        strides: Union[Sequence[int], int] = 1,
        kernel_size: Union[Sequence[int], int] = 3,
        adn_ordering: str = "NDA",
        act: Optional[Union[Tuple, str]] = "PRELU",
        norm: Optional[Union[Tuple, str]] = "INSTANCE",
        dropout: Optional[Union[Tuple, str, float]] = None,
        dropout_dim: Optional[int] = 1,
        dilation: Union[Sequence[int], int] = 1,
        groups: int = 1,
        bias: bool = True,
        conv_only: bool = False,
        is_transposed: bool = False,
        padding: Optional[Union[Sequence[int], int]] = None,
        output_padding: Optional[Union[Sequence[int], int]] = None,
    ) -> None:
        super().__init__()
        self.spatial_dims = spatial_dims
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.is_transposed = is_transposed
        if padding is None:
            padding = same_padding(kernel_size, dilation)
        conv_type = Conv[Conv.CONVTRANS if is_transposed else Conv.CONV, self.spatial_dims]

        conv: nn.Module
        if is_transposed:
            if output_padding is None:
                output_padding = stride_minus_kernel_padding(1, strides)
            conv = conv_type(
                in_channels,
                out_channels,
                kernel_size=kernel_size,
                stride=strides,
                padding=padding,
                output_padding=output_padding,
                groups=groups,
                bias=bias,
                dilation=dilation,
            )
        else:
            conv = conv_type(
                in_channels,
                out_channels,
                kernel_size=kernel_size,
                stride=strides,
                padding=padding,
                dilation=dilation,
                groups=groups,
                bias=bias,
            )

        self.add_module("conv", conv)

        if conv_only:
            return
        if act is None and norm is None and dropout is None:
            return
        self.add_module(
            "adn",
            ADN(
                ordering=adn_ordering,
                in_channels=out_channels,
                act=act,
                norm=norm,
                norm_dim=self.spatial_dims,
                dropout=dropout,
                dropout_dim=dropout_dim,
            ),
        )
