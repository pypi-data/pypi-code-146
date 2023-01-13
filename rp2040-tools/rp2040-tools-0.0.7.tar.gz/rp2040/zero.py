from rp2040.base import SimpleOut


class BoardLed(SimpleOut):
    """
    板载LED(绿色)
    """

    def __init__(self):
        super().__init__(16, 0)
