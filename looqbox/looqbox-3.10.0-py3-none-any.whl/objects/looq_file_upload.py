from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjFileUpload(LooqObject):
    """
    Creates a view to drag and drop a file that will be read and used in other script of the response.

    Attributes:
    --------
        :param str filepath: Path where file will be upload to.
        :param str title: Title of the dropzone.
        :param str content: Content that will be send to the other script.

    Example:
    --------
    >>> upload = ObjFileUpload(filepath="secondScript", title="Looq File Upload")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, filepath, title=None, content=None, tab_label=None, value=None):
        """
        Creates a view to drag and drop a file that will be read and used in other script of the response.

        Parameters:
        --------
            :param str filepath: Path where file will be upload to.
            :param str title: Title of the dropzone.
            :param str content: Content that will be send to the other script.

        Example:
        --------
        >>> upload = ObjUpload(filepath="secondScript", title="Looq File Upload")
        """
        super().__init__()
        if title is None:
            title = []
        if content is None:
            content = []
        self.filepath = filepath
        self.title = title
        self.content = content
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.file_upload_render(self)
