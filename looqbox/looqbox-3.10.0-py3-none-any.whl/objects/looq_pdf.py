from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjPDF(LooqObject):
    """
    Renders a PDF in the Looqbox's board using a PDF from the same directory of
    the response or from an external link (only works with HTTPS links).

    Attributes:
    --------
        :param str src: PDF's source.
        :param int initial_page: Page that the PDF will open.
        :param int height: Element height in the frame.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> pdf = ObjPDF(src="cartaoCNPJLooqbox.pdf")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, src, initial_page=1, height=None, tab_label=None, value=None):
        """
        Renders a PDF in the Looqbox's board using a PDF from the same directory of
        the response or from an external link (only works with HTTPS links).

        Parameters:
        --------
            :param str src: PDF's source.
            :param int initial_page: Page that the PDF will open.
            :param int height: Element height in the frame.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
        >>> pdf = ObjPDF(src="cartaoCNPJLooqbox.pdf")
        """
        super().__init__()
        self.source = src
        self.initial_page = initial_page
        self.height = height
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.pdf_render(self)
