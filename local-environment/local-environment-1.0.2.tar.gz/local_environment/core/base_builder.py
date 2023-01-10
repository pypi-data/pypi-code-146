from collections import OrderedDict
from functools import wraps
from typing import TypeVar, Generic, Dict, Any, Callable

from faker import Faker

from local_environment.core.builder_param import BuilderParam

T = TypeVar("T")
_SET_MARKER = "__SET_MARKER_VAL__"


def _default_set_param_value(self, param_name=None, value=None) -> "BaseBuilder":
    """
    Set the value of a parameter
    Args:
        cls: The class instance
        param_name: The name of the parameter
        value: The value to set

    Returns: The class instance
    """
    try:
        getattr(self.constructed_object, param_name)
    except AttributeError:
        raise NotImplementedError(
            f'Must create a set_ function for custom builder parameter "{param_name}" which is not a member of constructed '
            f"object class or set it to 'virtual=True'"
        )
    try:
        setattr(self.constructed_object, param_name, value)
    except AttributeError as exc:
        raise AttributeError(
            f'Cannot set value "{value}" for parameter "{param_name}", original error: [{exc}]'
        )
    return self


def _default_empty_set_param_value(self, param_name=None, value=None) -> "BaseBuilder":
    """
    Args:
        cls: The class instance
        param_name: The name of the parameter
        value: The value to set

    Returns: The class instance
    """
    return self


def _was_param_set_wrapper(builder: Any, param_name: str, func: Callable) -> Callable:
    """
    Check if a parameter was set
    Args:
        cls: The class instance
        param_name: The name of the parameter

    Returns: Whether the parameter was set
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        builder._param_value_markers[param_name] = args[0]
        if func.__name__ == _default_set_param_value.__name__:
            return func(param_name, *args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


class BaseBuilder(Generic[T]):
    """
    Base builder class for all builders in the system
    """

    fake: Faker = Faker(
        locale=OrderedDict(
            [
                ("en-US", 1),
            ]
        ),
    )["en_US"]

    def __getattribute__(self, name):
        if name in [
            "_collect_builder_parameters",
        ]:
            return object.__getattribute__(self, name)
        _class_parameters = self._collect_builder_parameters()
        if name in _class_parameters:
            build_param = object.__getattribute__(self, name)
            build_param._parent = self
            build_param._param_name = name
            return build_param
        attribute = object.__getattribute__(self, name)
        if isinstance(attribute, Callable) and name.startswith("set_"):
            return _was_param_set_wrapper(self, name.replace("set_", "", 1), attribute)
        return attribute

    def __init_subclass__(cls, **kwargs):
        """
        Init the class
        """
        _class_parameters = cls._collect_builder_parameters()
        for name, build_param in _class_parameters.items():
            if not build_param.is_required and build_param.randomize:
                randomize_function_name = f"_randomize_{name}"
                randomize_function = getattr(cls, randomize_function_name, None)
                if not randomize_function and build_param.default_value is None:
                    raise NotImplementedError(
                        f"Must implement randomize function for non required parameter {name}"
                    )

            # Generate the set functions
            set_parameter_function_name = f"set_{name}"
            set_parameter_function = getattr(cls, set_parameter_function_name, None)
            if not set_parameter_function:
                default_func = _default_set_param_value
                if build_param.virtual:
                    default_func = _default_empty_set_param_value
                setattr(
                    cls,
                    set_parameter_function_name,
                    default_func,
                )

    def __init__(self, constructed_object: T):
        self._param_value_markers = {}
        self.constructed_object = constructed_object

    def _set_param_value(self, param_name: str, value: Any) -> "BaseBuilder":
        """
        Set the value of a parameter
        Args:
            param_name: The name of the parameter
            value: The value to set

        Returns: The class instance

        """
        set_function_name = f"set_{param_name}"
        set_function = getattr(self, set_function_name, None)
        if set_function:
            set_function(value)
        else:
            _default_set_param_value(self, param_name, value)
        self._param_value_markers[param_name] = value
        return self

    def _get_builder_param_value(self, param_name: str) -> Any:
        randomize_function_name = f"_randomize_{param_name}"
        randomize_function = getattr(self, randomize_function_name, None)

        return (
            self._param_value_markers.get(
                param_name, getattr(self.constructed_object, param_name, None)
            )
            if self._param_value_markers.get(param_name, _SET_MARKER) != _SET_MARKER
            else (randomize_function() if randomize_function else None)
        )

    def was_builder_param_set(self, param_name: str) -> bool:
        return self._param_value_markers.get(param_name, _SET_MARKER) == _SET_MARKER

    @classmethod
    def _collect_builder_parameters(cls) -> Dict[str, BuilderParam]:
        """
        Collects all the builder parameters of the class
        Returns: A dictionary of the builder parameters of the class where the key is the parameter name and the
        value is the parameter object
        """
        params = {}
        for name, value in cls.__dict__.items():
            if isinstance(value, BuilderParam):
                params[name] = value
        for base in cls.__bases__:
            if issubclass(base, BaseBuilder):
                params.update(base._collect_builder_parameters())
        return params

    def _post_build(self, constructed_object: T, *args, **kwargs) -> T:
        """
        Build the object
        Returns: The built object
        """
        return constructed_object

    def _pre_build(self, constructed_object: T, *args, **kwargs) -> T:
        """
        Build the object
        Returns: The built object
        """
        return constructed_object

    def build(self, *args, **kwargs) -> T:
        """
        Build the object
        Returns: The built object
        """
        self._pre_build(self.constructed_object, *args, **kwargs)

        _class_parameters = self._collect_builder_parameters()
        for key in _class_parameters.keys():
            randomize_function_name = f"_randomize_{key}"
            randomize_function = getattr(self, randomize_function_name, None)
            set_function_name = f"set_{key}"
            set_function = getattr(self, set_function_name, None)
            param: BuilderParam = _class_parameters[key]
            if key not in self._param_value_markers and param.default_value is None:
                if (
                        not _class_parameters[key].is_required
                        and _class_parameters[key].randomize
                        and not randomize_function
                ):
                    raise NotImplementedError(
                        f"Must implement randomize function for non required parameter {key}"
                    )
                elif _class_parameters[key].is_required:
                    raise AttributeError(
                        f"Parameter {key} is not set and is a required parameter"
                    )
                elif _class_parameters[key].randomize:
                    set_function(randomize_function())
            elif (
                    key not in self._param_value_markers and param.default_value is not None
            ):
                if randomize_function:
                    set_function(randomize_function())
                else:
                    set_function(param.default_value)
        return self._post_build(self.constructed_object, *args, **kwargs)

    @classmethod
    def destruct(cls, constructed_object: T):
        raise NotImplementedError()
