from pypattyrn.structural.composite import Composite

from local_environment.dependencies.base_async_dependency import BaseAsyncEnvironmentComponent


class BaseAsyncDirector(Composite, BaseAsyncEnvironmentComponent):
    def __init__(self):
        super(BaseAsyncDirector, self).__init__(BaseAsyncEnvironmentComponent)

    def add_component(self, component: BaseAsyncEnvironmentComponent):
        super(BaseAsyncDirector, self).add_component(component)

    def __getattribute__(self, name):
        if name in ["_delegate"]:
            return object.__getattribute__(self, name)
        if name in list(
                filter(lambda x: not x.startswith("_"), dir(BaseAsyncEnvironmentComponent))
        ):
            async def _async_delegate():
                return await self._delegate(name)

            return _async_delegate
        return object.__getattribute__(self, name)

    async def _delegate(self, func_name):
        """
        Apply a function to all child components by function name.

        @param func_name: The name of the function to call with all child components.
        @type func_name: str
        @raise AttributeError: If a child component does not have a callable function with the given name.
        """
        components = sorted(
            list(self.components), key=lambda component: component.PRIORITY
        )
        for component in components:
            attribute = getattr(component, func_name)
            if callable(attribute):
                await attribute()
            else:
                raise AttributeError()
