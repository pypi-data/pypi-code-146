from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjImage(LooqObject):
    """
    Creates a looqbox image object.

    Attributes:
    --------
        :param str src: Image source.
        :param int width: Image width.
        :param int height: Image height.
        :param dict style: A dict of CSS styles to change the frame.
        :param str tooltip: Text in pop-up message.
        :param str link: Add link to image.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> img = ObjImage(src="http://www.velior.ru/wp-content/uploads/2009/05/Test-Computer-Key-by-Stuart-Miles.jpg",
    ...                width=100, height=100, style={"border-radius": "8px"}, tooltip="test", link="https://www.looqbox.com/")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, src, width=None, height=None, style=None, tooltip=None, link=None, tab_label=None, value=None):
        """
        Creates a looqbox image object.

        Parameters:
        --------
            :param str src: Image source.
            :param int width: Image width.
            :param int height: Image height.
            :param dict style: A dict of CSS styles to change the frame.
            :param str tooltip: Text in pop-up message.
            :param str link: Add link to image.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
        >>> img = ObjImage(src="http://www.velior.ru/wp-content/uploads/2009/05/Test-Computer-Key-by-Stuart-Miles.jpg",
        ...                width=100, height=100, style={"border-radius": "8px"}, tooltip="test", link="https://www.looqbox.com/")

        """
        super().__init__()
        if link is None:
            link = {}
        if tooltip is None:
            tooltip = {}
        if style is None:
            style = []
        self.source = src
        self.width = width
        self.height = height
        self.style = style
        self.tooltip = tooltip
        self.link = link
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.image_render(self)
