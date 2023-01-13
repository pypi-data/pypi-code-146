import logging
import os
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .tools import open_img

path_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)


class Picture:
    """Picture. Transform a Picture to one with bouding box and its classes"""

    def __init__(
        self, image: object, box_cla: [((float, float, float, float), str)]
    ) -> None:
        """__init__.

        :param image: image to transform
        :type image: object
        :param box_cla: bouding box and classes
        :type box_cla: [((float, float, float, float), str)]
        :rtype: None
        """
        self.image = open_img(image)
        self.img_size = self.image.size
        self.box_cla = box_cla

    def draw(
        self,
        conf_prec: int = 2,
        font: str = os.path.join(path_dir, "font", "FUTURAM.ttf"),
    ) -> Image:
        """draw. draw the bouding box, classes and conf

        :param conf_prec: decimals of conf score to draw, 0 = no conf drawn
        :type conf_prec: int
        :param font: font to be used
        :type font: str
        :rtype: Image
        """
        draw = ImageDraw.Draw(self.image)
        classes = self.get_all_classes()
        colors = [random_color() for i in range(len(classes))]
        for box, cla in self.box_cla:
            box = [int(b) for b in box]
            if not isinstance(cla, list):
                cla = [cla]
            color_cla = []
            texts = []
            for conf, cl in cla:
                color_cla += [colors[classes.index(cl)]]
                if conf_prec > 0:
                    conf_text = ": " + format(conf, "." + str(conf_prec) + "f")
                else:
                    conf_text = ""
                texts += [str(cl) + conf_text]
            text = ", ".join(texts)
            color = tuple(np.mean(color_cla, axis=0, dtype=int))
            length = box[2] - box[0]
            width = int(self.img_size[1] / 500) + 1
            width_text = width * 10
            text_box = Image.new(
                "RGBA",
                (length, width_text),
                (*color, 255),
            )
            text_draw = ImageDraw.Draw(text_box)
            size = font_size_calc(font, text, length, width_text, text_draw)
            fnt = ImageFont.truetype(font=font, size=size)
            text_draw.multiline_text((0, 0), text, font=fnt, fill=inv_color(color))
            self.image.paste(text_box, (box[0], box[3]), text_box)
            draw.rectangle(box, fill=None, outline=color, width=width)
        return self.image

    def get_all_classes(self) -> list[str]:
        """get_all_classes. get all classes to draw

        :rtype: list[str]
        """
        classes = set()
        for box, cla in self.box_cla:
            if not isinstance(cla, list):
                cla = [cla]
            for conf, cl in cla:
                classes.add(cl)
        return list(classes)


def inv_color(color: (int, int, int)) -> (int, int, int):
    """inv_color. Attempt to choose the best color to read according to the another color

    :param color: background color
    :type color: (int, int, int)
    :rtype: (int, int, int)
    """
    col = [0] * len(color)
    for i in range(len(color)):
        col[i] = abs(color[i] - 255)
        col[i] = 0 if col[i] <= 125 else 255
    return tuple(col)


def random_color() -> (int, int, int):
    """random_color. create a random color

    :rtype: (int, int, int)
    """
    color = tuple(np.random.choice(range(256), size=3))
    return color


def font_size_calc(font: str, txt: str, length: int, width: int, draw: object) -> int:
    """font_size_calc. Calculate font size based on width and length

    :param font:
    :type font: str
    :param txt:
    :type txt: str
    :param length:
    :type length: int
    :param width:
    :type width: int
    :param draw:
    :type draw: object | None
    :rtype: int
    """
    t = time.time()
    logger.debug(repr(txt) + " width:" + str(width) + " length: " + str(length))
    fontsize = 1
    fnt = ImageFont.truetype(font=font, size=fontsize)
    if draw is None:
        fntsize = fnt.getsize(txt)
    else:
        fntsize = draw.textsize(txt, fnt)
    while fntsize[0] < length and fntsize[1] < width:
        fontsize += 1
        fnt = ImageFont.truetype(font=font, size=fontsize)
        if draw is None:
            fntsize = fnt.getsize(txt)
        else:

            fntsize = draw.textsize(txt, fnt)
    logger.debug(str(time.time() - t) + " sec to calculate font size")
    return fontsize - 1
