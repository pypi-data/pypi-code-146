from typing import Type, Any, Optional, Generic, TypeVar

B = TypeVar("B")


class BuilderParam(Generic[B]):
    _parent: B = None
    _param_name: str = None

    def __call__(self, *args, **kwargs) -> B:
        """
        Call the builder param
        Args:
            *args: The arguments
            **kwargs: The keyword arguments

        Returns: The builder param
        """
        return self._parent._set_param_value(self._param_name, *args, **kwargs)

    def __init__(
            self,
            param_type: Type,
            required: Optional[bool] = False,
            randomize: Optional[bool] = True,
            default: Optional[Any] = None,
            virtual: Optional[bool] = False,
    ):
        """
        Builder param constructor
        Args:
            param_type: The type of the parameter
            required: Whether this parameter is required when creating a builder instance
            randomize: Whether this parameter should be randomized in the case there is no default value and it is not set
            default: The default value of the parameter
            virtual: Whether this parameter exists on the constructed object or not
        """
        self.is_required = required
        self.randomize = randomize
        self.default_value = default
        self._param_type = param_type
        self.virtual = virtual
