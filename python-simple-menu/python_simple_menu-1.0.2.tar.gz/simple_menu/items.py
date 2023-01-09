from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Dict
from typing import List


class BaseItem(ABC):
    """
    All menu items should inherit from this
    """

    def __init__(self, label: str = ""):
        self.label = label

    @abstractmethod
    def exec(self):
        print(self.label)


class MenuItem(BaseItem):
    """
    Displays a sub-menu until the user chooses to go back or quit the app

    Attributes:
        label(str): the option text
        menu(Menu): the menu to execute
    """

    from .menu import Menu

    def __init__(self, label: str, menu: Menu):
        super().__init__(label)
        self.menu = menu

    def exec(self):
        self.menu.run()


class FunctionItem(BaseItem):
    """
    Executes a function when the item is chosen

    Attributes:
        label(str): the option text
        function(Callable): the function to execute
        args(List): positional arguments for the function
        kwargs(Dict): keyword arguments for the function
    """

    def __init__(
        self,
        label,
        function: Callable,
        args: List | None = [],
        kwargs: Dict | None = {},
    ):
        super().__init__(label)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def exec(self):
        self.function(*self.args, **self.kwargs)
