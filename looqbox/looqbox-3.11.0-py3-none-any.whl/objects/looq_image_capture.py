from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjImageCapture(LooqObject):
    """
    Creates a looqbox image object from a webcam picture.

    Attributes:
    --------
        :param str filepath: Path for the script to which the image is returned.
        :param str title: Title of the image box.
        :param dict content: Format that the captured image data will be sent to the interface.

    Example:
    --------
    >>> image = ObjImageCapture(filepath="filePath", title="Captura de Imagem")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, filepath, title=None, content=None, value=None):
        """
        Creates a looqbox image object from a webcam picture.

        Parameters:
        --------
            :param str filepath: Path for the script to which the image is returned.
            :param str title: Title of the image box.
            :param dict content: Format that the captured image data will be sent to the interface.

        Example:
        --------
        >>> image <- ObjImageCapture(filepath="filePath", title="Captura de Imagem")
        """
        super().__init__()
        if content is None:
            content = []
        if title is None:
            title = ""
        self.filepath = filepath
        self.title = title
        self.content = content
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.image_capture_render(self)
