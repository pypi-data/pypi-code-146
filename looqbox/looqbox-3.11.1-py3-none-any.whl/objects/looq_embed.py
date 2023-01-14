from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjEmbed(LooqObject):
    """
    Creates a frame inside the Looqbox interface using an iframe HTML tag as source.

    Attributes:
    --------
        :param str iframe: Embedded element dimensions and source in HTML format.

    Example:
    --------
    >>> webframe0 = ObjEmbed("<iframe frameborder=\"0\" width=\"560\" height=\"315\"
    ...                      src=\"https://app.biteable.com/watch/embed/looqbox-presentation-1114895\">
    ...                      </iframe>")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, iframe, tab_label=None, value=None):
        """
        Creates a frame inside the Looqbox interface using an iframe HTML tag as source.

        Parameters:
        --------
            :param str iframe: Embedded element dimensions and source in HTML format.
            :return: A Looqbox ObjEmbed object.

        Example:
        --------
        >>> webframe0 = ObjEmbed("<iframe frameborder=\"0\" width=\"560\" height=\"315\"
        ...                      src=\"https://app.biteable.com/watch/embed/looqbox-presentation-1114895\">
        ...                      </iframe>")
        """
        super().__init__()
        self.iframe = iframe
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.embed_render(self)
