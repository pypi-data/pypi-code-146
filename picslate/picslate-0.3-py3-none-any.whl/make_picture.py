import json
import logging
import os
import time

import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFont

path_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)


class Img:
    """Img."""

    def __init__(self, image: object) -> None:
        """__init__. Image and its numpy matrix

        :param image:
        :type image: object
        :rtype: None
        """
        self.image = Image.open(image).convert("RGB")

        self.matrix = np.array(self.image)

    def background_color(
        self, pos: (int, int, int, int), pmax: int = 10
    ) -> (int, int, int):
        """background_color. find background color

        :param pos: position to search
        :type pos: (int, int, int, int)
        :param pmax: max pixel to evaluate
        :type pmax: int
        :rtype: (int, int, int)
        """
        i = 0
        pos1 = pos[1]
        while 0 <= pos1 and i < pmax:
            i += 1
            pos1 -= 1
        pos2 = pos[3]
        i = 0
        while self.matrix.shape[0] > pos2 and i < pmax:
            pos2 += 1
            i += 1
        matrix = np.concatenate(
            (
                self.matrix[pos1 : pos[1], pos[0] : pos[2], :],
                self.matrix[pos[3] : pos2, pos[0] : pos[2], :],
            )
        )
        colors = find_main_color(matrix)
        return colors[0]

    def remove_text(
        self, pos: (int, int, int, int), color: (int, int, int) = None
    ) -> None:
        """remove_text. Remove object inside position

        :param pos: position to be replaces
        :type pos: (int, int, int, int)
        :param color: color to replace
        :type color: None | (int, int, int)
        :rtype: None
        """

        if color is None:
            color = self.background_color(pos)

        self.matrix[pos[1] : pos[3], pos[0] : pos[2]] = color

    def font_color(self, pos: (int, int, int, int)) -> (int, int, int):
        """font_color. find color font

        :param pos: position to search
        :type pos: (int, int, int, int)
        :rtype: (int, int, int)
        """
        bg_color = self.background_color(pos)
        colors = find_main_color(
            self.matrix[pos[1] : pos[3], pos[0] : pos[2], :], bgcol=bg_color
        )
        return colors[0]


def find_main_color(
    matrix: np.ndarray, bgcol: (int, int, int) = None
) -> list[(int, int, int)]:
    """find_main_color. find best color match

    :param matrix: image matrix
    :type matrix: np.ndarray
    :param bgcol: background color
    :type bgcol: None | (int, int, int)
    :rtype: list[(int, int, int)]
    """
    icolor = {}
    arrays = [None] * 3
    for c in range(3):
        array = matrix[:, :, c].flatten()
        value, index, count = np.unique(
            array,
            return_counts=True,
            return_index=True,
        )
        arrays[c] = array
        for i, ind in enumerate(index):
            if ind not in icolor:
                icolor[ind] = 0
            icolor[ind] += count[i]
    if bgcol is not None:

        for i in icolor:
            color = [arrays[0][i], arrays[1][i], arrays[2][i]]
            ratio = sum([abs(int(bgcol[c]) - int(color[c])) for c in range(3)]) / (
                255 * 3
            )
            icolor[i] = ratio * icolor[i]
    icolor = dict(sorted(icolor.items(), key=lambda item: item[1], reverse=True))
    colors = [tuple([arrays[c][i] for c in range(3)]) for i in icolor]
    return colors


class Piconv:
    """Piconv."""

    map_font = json.load(open(os.path.join(path_dir, "font", "map.json")))

    def __init__(
        self, image: object, paragraphs: list[object], debug: bool = False
    ) -> bool:
        """__init__. convert an image into its translation

        :param image: image to be analyzed
        :type image: object
        :param paragraphs: paragraphs to be translated
        :type paragraphs: list[object]
        :param debug: display tesseract paragraphs / character bounding box
        :type debug: bool
        :rtype: bool
        """
        self.image = Img(image)
        self.image_raw = Img(image)
        self.paragraphs = paragraphs
        self.pimg = None  # self.image.image.convert("RGBA")
        self.draw = None  # ImageDraw.Draw(self.pimg)
        self.debug = debug

    def convert(
        self,
        font: str | None = None,
        fontsize: int | None = None,
        background_color: str | None = None,
        fontcolor: (int, int, int) = None,
    ) -> object:
        """convert. translate the picture

        :param font: font to replace the text into
        :type font: str | None
        :param fontsize: size font, default calculate an approximate font size
        :type fontsize: int | None
        :param background_color: background to replaces, default attempt to find the best background color
        :type background_color: str | None
        :param fontcolor: font color, default, attempt to find the best font color
        :type fontcolor: (int, int, int) | None
        :rtype: object
        """
        for para in self.paragraphs:
            symbol_pos = [child.bbox for word in para.words for child in word.children]

            for pos in symbol_pos:
                self.image.remove_text(pos, background_color)

        self.pimg = Image.fromarray(self.image.matrix).convert("RGBA")
        self.draw = ImageDraw.Draw(self.pimg)

        for ip, para in enumerate(self.paragraphs):
            if font is None:
                if para.to_lang in self.map_font:
                    lang = para.to_lang
                else:
                    lang = "en"
                path_font = os.path.join(path_dir, "font", self.map_font[lang])
                font = os.path.join(path_font, os.listdir(path_font)[0])

            if len(para.text_translated) == 0:
                continue
            symbol_pos = [child.bbox for word in para.words for child in word.children]
            if self.debug:
                for pos in symbol_pos:
                    self.draw.rectangle(pos, outline=(255, 0, 0, 255))
                self.draw.rectangle(para.pos, outline=(0, 255, 0, 255))
            length = para.pos[2] - para.pos[0]
            width = para.pos[3] - para.pos[1]
            if width > 5 * length:
                text = vertical_text(para.text_translated)

            elif width > length:
                text = para.text_translated.replace(" ", "\n")
            else:
                text = para.text_translated

            if fontsize is None:
                size = font_size_calc(font, text, length, width, draw=self.draw)
            else:
                size = fontsize
            fnt = ImageFont.truetype(font, size=size)
            para_img = Image.new(
                "RGBA",
                (length, width),
                (255, 255, 255, 0),
            )

            if fontcolor is None:
                fcol = get_colors(self.image_raw, symbol_pos, mod="font")
                if len(fcol) == 0:
                    fntcolor = [((255, 255, 255), 1)]
                else:
                    fntcolor = choose_colors(fcol)
            else:
                fntcolor = [[fontcolor, 1]]
            para_draw = ImageDraw.Draw(para_img)
            para_draw.multiline_text(
                (0, 0),
                text,
                font=fnt,
                fill=tuple(fntcolor[0][0]),
            )
            self.pimg.paste(para_img, (para.pos[0], para.pos[1]), para_img)

        return self.pimg


def font_size_calc(
    font: str, txt: str, length: int, width: int, draw: object | None = None
) -> int:
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
    fnt = ImageFont.truetype(font, fontsize)
    if draw is None:
        fntsize = fnt.getsize(txt)
    else:
        fntsize = draw.textsize(txt, fnt)
    while fntsize[0] < length and fntsize[1] < width:
        fontsize += 1
        fnt = ImageFont.truetype(font, fontsize)
        if draw is None:
            fntsize = fnt.getsize(txt)
        else:

            fntsize = draw.textsize(txt, fnt)
    logger.debug(str(time.time() - t) + " sec to calculate font size")
    return fontsize - 1


def vertical_text(text: str) -> str:
    """vertical_text. transform a text into a
    v
    e
    r
    t
    i
    c
    a
    l

    one

    :param text:
    :type text: str
    :rtype: str
    """

    texts = text.split("\n")
    max_len = max(len(txt) for txt in texts)
    new_text = [""] * max_len
    for i in range(max_len):
        new_text[i] += " ".join([txt[i] for txt in texts if len(txt) > i])
    return "\n".join(new_text)


def replace_bg(
    image: object, positions: list[(int, int, int, int)], color: (int, int, int)
) -> np.ndarray:
    """replace_bg. replce background color

    :param image:
    :type image: object
    :param positions:
    :type positions: list[(int, int, int, int)]
    :param color:
    :type color: (int, int, int)
    :rtype: np.ndarray
    """
    for pos in positions:
        image.matrix[pos[1] : pos[3], pos[0] : pos[2]] = color
    return image.matrix


def choose_colors(colors: list[(int, int, int)]) -> ((int, int, int), int):
    """choose_colors. attemtp to choose the best color

    :param colors:
    :type colors: list[(int, int, int)]
    :rtype: ((int, int, int), int) color and its ratio
    """
    value, index, count = np.unique(
        [str(color) for color in colors],
        return_counts=True,
        return_index=True,
    )

    count, value = zip(*sorted(zip(count, value), reverse=True))
    total = sum(count)
    colors_ratio = [(eval(value[i]), count[i] / total) for i in range(len(value))]
    return colors_ratio


def get_colors(
    image: object, positions: list[(int, int, int, int)], mod: str = "font"
) -> list[(int, int, int)]:
    """get_colors. attempt to find the main color from position

    :param image:
    :type image: object
    :param positions:
    :type positions: list[(int, int, int, int)]
    :param mod:
    :type mod: str
    :rtype: list[(int, int, int)]
    """
    colors = []
    for pos in positions:
        if mod == "font":
            color = get_font_color(image, pos)
        else:
            color = get_background_color(image, pos)
        colors += [color]
    return colors


def get_font_color(image: object, pos: (int, int, int, int)) -> object:
    """get_font_color.

    :param image:
    :type image: object
    :param pos:
    :type pos: (int, int, int, int)
    :rtype: object
    """
    return image.font_color(pos)


def get_background_color(image: object, pos: (int, int, int, int)) -> object:
    """get_background_color.

    :param image:
    :type image: object
    :param pos:
    :type pos: (int, int, int, int)
    :rtype: object
    """
    return image.background_color(pos)
