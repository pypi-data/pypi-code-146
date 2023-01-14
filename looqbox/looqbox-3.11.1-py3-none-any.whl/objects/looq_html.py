from looqbox.render.chatbot.components.text import _remove_html_tags
from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
import json


class ObjHTML(LooqObject):
    """
    Wraps an HTML code in a Looqbox object to be used in the interface.

    Attributes:
    --------
        :param str html: Html code that will be wrapped.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> HTML = ObjHTML("<div> Hello Worlds </div>")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, html, tab_label=None, value=None):
        """
        Wraps a HTML code in a Looqbox object to be used in the interface.

        Parameters:
        --------
            :param str html: Html code that will be wrapped.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
            HTML = ObjHTML("<div> Hello Worlds </div>)
        """
        super().__init__()
        self.html = html
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.html_render(self)

    def __repr__(self):
        return _remove_html_tags(self.html) + self.value
