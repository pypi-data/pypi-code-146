from looqbox.render.abstract_render import BaseRender
from abc import ABC, abstractmethod
from typing import List

from looqbox.objects.component_utility.css_option import CssOption


class LooqObject(ABC):

    def __init__(
            self,
            value: str = "",
            render_condition: bool = True,
            tab_label: str = "",
            css_options: List[CssOption] = None,
            obj_class: List[str] = None
    ):
        """
        :param value: ...
        :param render_condition: Boolean variable to determine if component should be rendered.
        :param tab_label: Text description to tab to show when frame tab view is set to True.
        :param css_options: CssOptions to add to parent container.
        :param css_options: CSS class for overriding styles.
        """
        self.value = value
        self.render_condition = render_condition
        self.tab_label = tab_label
        self.css_options = css_options
        self.obj_class = obj_class

    @abstractmethod
    def to_json_structure(self, visitor: BaseRender):
        """
        Convert python objects into json to Front-End render
        """
