import enum
from typing import (Any, Callable, Collection, Dict, Hashable, Iterable,
                    Mapping, Tuple, Type, Union, cast)

from torch import nn


def damerau_levenshtein_distance(s1: str, s2: str):
    """Calculate the Damerau–Levenshtein distance between two strings for spelling correction.

    https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance
    """
    if s1 == s2:
        return 0
    string_1_length = len(s1)
    string_2_length = len(s2)
    if not s1:
        return string_2_length
    if not s2:
        return string_1_length
    d = {(i, -1): i + 1 for i in range(-1, string_1_length + 1)}
    for j in range(-1, string_2_length + 1):
        d[(-1, j)] = j + 1

    for i, s1i in enumerate(s1):
        for j, s2j in enumerate(s2):
            cost = 0 if s1i == s2j else 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1, d[(i, j - 1)] + 1, d[(i - 1, j - 1)] + cost  # deletion  # insertion  # substitution
            )
            if i and j and s1i == s2[j - 1] and s1[i - 1] == s2j:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition

    return d[string_1_length - 1, string_2_length - 1]


def look_up_option(opt_str,
                   supported: Union[Collection, enum.EnumMeta],
                   default="no_default",
                   print_all_options=True):
    """Look up the option in the supported collection and return the matched item.

    Raise a value error possibly with a guess of the closest match.

    Args:
        opt_str: The option string or Enum to look up.
        supported: The collection of supported options, it can be list, tuple, set, dict, or Enum.
        default: If it is given, this method will return `default` when `opt_str` is not found,
            instead of raising a `ValueError`. Otherwise, it defaults to `"no_default"`,
            so that the method may raise a `ValueError`.
        print_all_options: whether to print all available options when `opt_str` is not found. Defaults to True

    Examples:
    .. code-block:: python

        from enum import Enum
        from monai.utils import look_up_option
        class Color(Enum):
            RED = "red"
            BLUE = "blue"
        look_up_option("red", Color)  # <Color.RED: 'red'>
        look_up_option(Color.RED, Color)  # <Color.RED: 'red'>
        look_up_option("read", Color)
        # ValueError: By 'read', did you mean 'red'?
        # 'read' is not a valid option.
        # Available options are {'blue', 'red'}.
        look_up_option("red", {"red", "blue"})  # "red"

    Adapted from https://github.com/NifTK/NiftyNet/blob/v0.6.0/niftynet/utilities/util_common.py#L249
    """
    if not isinstance(opt_str, Hashable):
        raise ValueError(f"Unrecognized option type: {type(opt_str)}:{opt_str}.")
    if isinstance(opt_str, str):
        opt_str = opt_str.strip()
    if isinstance(supported, enum.EnumMeta):
        if isinstance(opt_str, str) and opt_str in {item.value for item in cast(Iterable[enum.Enum], supported)}:
            # such as: "example" in MyEnum
            return supported(opt_str)
        if isinstance(opt_str, enum.Enum) and opt_str in supported:
            # such as: MyEnum.EXAMPLE in MyEnum
            return opt_str
    elif isinstance(supported, Mapping) and opt_str in supported:
        # such as: MyDict[key]
        return supported[opt_str]
    elif isinstance(supported, Collection) and opt_str in supported:
        return opt_str

    if default != "no_default":
        return default

    # find a close match
    set_to_check: set
    if isinstance(supported, enum.EnumMeta):
        set_to_check = {item.value for item in cast(Iterable[enum.Enum], supported)}
    else:
        set_to_check = set(supported) if supported is not None else set()
    if not set_to_check:
        raise ValueError(f"No options available: {supported}.")
    edit_dists = {}
    opt_str = f"{opt_str}"
    for key in set_to_check:
        edit_dist = damerau_levenshtein_distance(f"{key}", opt_str)
        if edit_dist <= 3:
            edit_dists[key] = edit_dist

    supported_msg = f"Available options are {set_to_check}.\n" if print_all_options else ""
    if edit_dists:
        guess_at_spelling = min(edit_dists, key=edit_dists.get)  # type: ignore
        raise ValueError(
            f"By '{opt_str}', did you mean '{guess_at_spelling}'?\n"
            + f"'{opt_str}' is not a valid value.\n"
            + supported_msg
        )
    raise ValueError(f"Unsupported option '{opt_str}', " + supported_msg)


def split_args(args):
    """Split arguments in a way to be suitable for using with the factory types.

    If `args` is a string it's interpreted as the type name.

    Args:
        args (str or a tuple of object name and kwarg dict): input arguments to be parsed.

    Raises:
        TypeError: When ``args`` type is not in ``Union[str, Tuple[Union[str, Callable], dict]]``.

    Examples::
        >>> act_type, args = split_args("PRELU")
        >>> monai.networks.layers.Act[act_type]
        <class 'torch.nn.modules.activation.PReLU'>

        >>> act_type, args = split_args(("PRELU", {"num_parameters": 1, "init": 0.25}))
        >>> monai.networks.layers.Act[act_type](**args)
        PReLU(num_parameters=1)
    """
    if isinstance(args, str):
        return args, {}
    name_obj, name_args = args

    if not isinstance(name_obj, (str, Callable)) or not isinstance(name_args, dict):
        msg = "Layer specifiers must be single strings or pairs of the form (name/object-types, argument dict)"
        raise TypeError(msg)

    return name_obj, name_args


class LayerFactory:
    """Factory object for creating layers.

    This uses given factory functions to actually produce the types or constructing
    callables. These functions are referred to by name and can be added at any time.
    """

    def __init__(self) -> None:
        self.factories: Dict[str, Callable] = {}

    @property
    def names(self) -> Tuple[str, ...]:
        """Produce all factory names."""
        return tuple(self.factories)

    def add_factory_callable(self, name: str, func: Callable) -> None:
        """Add the factory function to this object under the given name."""
        self.factories[name.upper()] = func
        self.__doc__ = (
            "The supported member"
            + ("s are: " if len(self.names) > 1 else " is: ")
            + ", ".join(f"``{name}``" for name in self.names)
            + ".\nPlease see :split_args` for additional args parsing."
        )

    def factory_function(self, name: str) -> Callable:
        """Decorate a factory function with the given name."""
        def _add(func: Callable) -> Callable:
            self.add_factory_callable(name, func)
            return func

        return _add

    def get_constructor(self, factory_name: str, *args) -> Any:
        """Get the constructor for the given factory name and arguments.

        Raises:
            TypeError: When ``factory_name`` is not a ``str``.
        """
        if not isinstance(factory_name, str):
            raise TypeError(f"factory_name must a str but is {type(factory_name).__name__}.")

        func = look_up_option(factory_name.upper(), self.factories)
        return func(*args)

    def __getitem__(self, args) -> Any:
        """Get the given name or name/arguments pair.

        If `args` is a callable it is assumed to be the constructor itself and is returned,
        otherwise it should be the factory name or a pair containing the name and arguments.
        """
        # `args[0]` is actually a type or constructor
        if callable(args):
            return args

        # `args` is a factory name or a name with arguments
        if isinstance(args, str):
            name_obj, args = args, ()
        else:
            name_obj, *args = args

        return self.get_constructor(name_obj, *args)

    def __getattr__(self, key):
        """If `key` is a factory name, return it, otherwise behave as inherited.

        This allows referring to factory names as if they were constants, eg. `Fact.FOO`
        for a factory Fact with factory function foo.
        """
        if key in self.factories:
            return key

        return super().__getattribute__(key)


Act = LayerFactory()


Act.add_factory_callable("elu", lambda: nn.modules.ELU)
Act.add_factory_callable("relu", lambda: nn.modules.ReLU)
Act.add_factory_callable("leakyrelu", lambda: nn.modules.LeakyReLU)
Act.add_factory_callable("prelu", lambda: nn.modules.PReLU)
Act.add_factory_callable("relu6", lambda: nn.modules.ReLU6)
Act.add_factory_callable("selu", lambda: nn.modules.SELU)
Act.add_factory_callable("celu", lambda: nn.modules.CELU)
Act.add_factory_callable("gelu", lambda: nn.modules.GELU)
Act.add_factory_callable("sigmoid", lambda: nn.modules.Sigmoid)
Act.add_factory_callable("tanh", lambda: nn.modules.Tanh)
Act.add_factory_callable("softmax", lambda: nn.modules.Softmax)
Act.add_factory_callable("logsoftmax", lambda: nn.modules.LogSoftmax)


@Act.factory_function("swish")
def swish_factory():
    from monai.networks.blocks.activation import Swish

    return Swish


@Act.factory_function("memswish")
def memswish_factory():
    from monai.networks.blocks.activation import MemoryEfficientSwish

    return MemoryEfficientSwish


@Act.factory_function("mish")
def mish_factory():
    from monai.networks.blocks.activation import Mish

    return Mish


Conv = LayerFactory()


@Conv.factory_function("conv")
def conv_factory(dim: int) -> Type[Union[nn.Conv1d, nn.Conv2d, nn.Conv3d]]:
    types = (nn.Conv1d, nn.Conv2d, nn.Conv3d)
    return types[dim - 1]


@Conv.factory_function("convtrans")
def convtrans_factory(dim: int) -> Type[Union[nn.ConvTranspose1d,
                                              nn.ConvTranspose2d,
                                              nn.ConvTranspose3d]]:
    types = (nn.ConvTranspose1d, nn.ConvTranspose2d, nn.ConvTranspose3d)
    return types[dim - 1]


Dropout = LayerFactory()


@Dropout.factory_function("dropout")
def dropout_factory(dim: int) -> Type[Union[nn.Dropout, nn.Dropout2d, nn.Dropout3d]]:
    types = (nn.Dropout, nn.Dropout2d, nn.Dropout3d)
    return types[dim - 1]


@Dropout.factory_function("alphadropout")
def alpha_dropout_factory(_dim):
    return nn.AlphaDropout


Norm = LayerFactory()


@Norm.factory_function("instance")
def instance_factory(dim: int) -> Type[Union[nn.InstanceNorm1d, nn.InstanceNorm2d, nn.InstanceNorm3d]]:
    types = (nn.InstanceNorm1d, nn.InstanceNorm2d, nn.InstanceNorm3d)
    return types[dim - 1]


@Norm.factory_function("batch")
def batch_factory(dim: int) -> Type[Union[nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d]]:
    types = (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d)
    return types[dim - 1]


@Norm.factory_function("group")
def group_factory(_dim) -> Type[nn.GroupNorm]:
    return nn.GroupNorm


@Norm.factory_function("layer")
def layer_factory(_dim) -> Type[nn.LayerNorm]:
    return nn.LayerNorm


@Norm.factory_function("localresponse")
def local_response_factory(_dim) -> Type[nn.LocalResponseNorm]:
    return nn.LocalResponseNorm


@Norm.factory_function("syncbatch")
def sync_batch_factory(_dim) -> Type[nn.SyncBatchNorm]:
    return nn.SyncBatchNorm


Pool = LayerFactory()


@Pool.factory_function("max")
def maxpooling_factory(dim: int) -> Type[Union[nn.MaxPool1d, nn.MaxPool2d, nn.MaxPool3d]]:
    types = (nn.MaxPool1d, nn.MaxPool2d, nn.MaxPool3d)
    return types[dim - 1]


@Pool.factory_function("adaptivemax")
def adaptive_maxpooling_factory(
    dim: int,
) -> Type[Union[nn.AdaptiveMaxPool1d, nn.AdaptiveMaxPool2d, nn.AdaptiveMaxPool3d]]:
    types = (nn.AdaptiveMaxPool1d, nn.AdaptiveMaxPool2d, nn.AdaptiveMaxPool3d)
    return types[dim - 1]


@Pool.factory_function("avg")
def avgpooling_factory(dim: int) -> Type[Union[nn.AvgPool1d, nn.AvgPool2d, nn.AvgPool3d]]:
    types = (nn.AvgPool1d, nn.AvgPool2d, nn.AvgPool3d)
    return types[dim - 1]


@Pool.factory_function("adaptiveavg")
def adaptive_avgpooling_factory(
    dim: int,
) -> Type[Union[nn.AdaptiveAvgPool1d, nn.AdaptiveAvgPool2d, nn.AdaptiveAvgPool3d]]:
    types = (nn.AdaptiveAvgPool1d, nn.AdaptiveAvgPool2d, nn.AdaptiveAvgPool3d)
    return types[dim - 1]
