from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjVideo(LooqObject):
    """
    Creates a looqbox video object from a video file in the same directory of the script or from a https web link.

    Attributes:
    --------
        :param str src: Source of the audio to be displayed.
        :param bool auto_play: Defines if the video starts as soon as the board is opened.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> video = ObjVideo("videoFile")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, src, auto_play=False, tab_label=None, value=None):
        """
        Creates a looqbox video object from a video file in the same directory of the script or from a https web link.

        Parameters:
        --------
            :param str src: Source of the audio to be displayed.
            :param bool auto_play: Defines if the video starts as soon as the board is opened.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
        >>> video = ObjVideo("videoFile")
        """
        super().__init__()
        self.source = src
        self.auto_play = auto_play
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.video_render(self)
