from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjFormHTML(LooqObject):
    """
    Creates a Looqbox form HTML object.

    Attributes:
    --------
        :param html: HTML string to be executed.
        :param str filepath: Form input file path.
        :param str content: Form content.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """

    def __init__(self, filepath=None, html=None, content=[], tab_label=None, value=None):
        """
        Creates a view to drag and drop a file that will be read and used in other script of the response.

        Parameters:
        --------
            :param html: HTML string to be executed.
            :param str filepath: Form input file path.
            :param str content: Form content.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
        """
        super().__init__()
        self.html = html
        self.filepath = filepath
        self.content = content
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.form_html_render(self)
