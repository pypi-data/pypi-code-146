from typing import TypeVar

from local_environment.core.base_builder import BaseBuilder

from local_environment.core.builder_param import BuilderParam

T = TypeVar("T")


class BaseAsyncBuilder(BaseBuilder[T]):
    """
    Base builder class for all builders in the system
    """

    async def _post_build(self, constructed_object: T, *args, **kwargs) -> T:
        """
        Build the object
        Returns: The built object
        """
        return constructed_object

    async def _pre_build(self, constructed_object: T, *args, **kwargs) -> T:
        """
        Build the object
        Returns: The built object
        """
        return constructed_object

    async def build(self, *args, **kwargs) -> T:
        """
        Build the object
        Returns: The built object
        """
        await self._pre_build(self.constructed_object, *args, **kwargs)

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
        return await self._post_build(self.constructed_object, *args, **kwargs)
