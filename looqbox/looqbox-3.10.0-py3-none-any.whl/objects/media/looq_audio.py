from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjAudio(LooqObject):
    """
    Creates a Looqbox audio object from an audio file which is in the same directory of the script or from a https
    web link.

    Attributes:
    --------
        :param str src: Source of the audio to be displayed (filepath or https link).
        :param bool auto_play: Defines if the audio starts as soon as the board is opened.

    Example:
    --------
    >>> audio = ObjAudio("/Users/looqbox/Downloads/armstrong.mp3")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """

    def __init__(self, src, auto_play=False, tab_label=None, value=None):
        """
        Creates a Looqbox audio object from an audio file which is in the same directory of the script or from a https
        web link.

        Parameters:
        --------
            :param str src: Source of the audio to be displayed (filepath or https link).
            :param bool auto_play: Defines if the audio starts as soon as the board is opened.
            :param str tab_label: Set the name of the tab in the frame.
            :return: A Looqbox ObjAudio object.

        Example:
        --------
        >>> audio = ObjAudio("/Users/looqbox/Downloads/armstrong.mp3")
        """
        super().__init__()
        self.source = src
        self.auto_play = auto_play
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.video_render(self)

