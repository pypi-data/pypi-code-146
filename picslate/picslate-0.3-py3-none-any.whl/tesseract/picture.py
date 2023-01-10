import json
import logging
import os
import re
import time

from PIL import Image
from tesserocr import RIL, PyTessBaseAPI, get_languages, iterate_level

path_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)


class TessObject:
    """TessObject. Object which comport words meta information from tesseract"""

    def __init__(self, children: list = []) -> None:
        """__init__. Text image object with position and meta information

        :param children: character of words
        :type children: list
        :rtype: None
        """
        self.text = ""
        self.conf = 0
        self.bbox = (0, 0, 0, 0)  # x0,y0,x1,y1
        self.children = children
        self.new_line = False
        self.block = None
        self.para = None

    def __str__(self) -> str:
        """__str__.

        :rtype: str
        """
        return str((self.text, self.bbox, self.new_line, self.block, self.para))

    def __repr__(self) -> str:
        """__repr__.

        :rtype: str
        """
        return str(self)


class Pics:
    """Pics."""

    languages = json.load(open(os.path.join(path_dir, "lang.json")))
    available_languages = get_languages()[1]

    def __init__(self, image: object, lang: str) -> None:
        """__init__. Picture class to be ocrized

        :param image: image to be ocrized
        :type image: object
        :param lang: language to be ocrized
        :type lang: str
        :rtype: None
        """
        self.image = Image.open(image)
        if self.languages.get(lang, None) in self.available_languages:
            self.lang = self.languages[lang]
        else:
            logger.warning(
                str(lang)
                + " not found, available languages are "
                + ", ".join(self.available_languages)
                + ".\nEnglish will be used."
            )
            self.lang = "eng"

    def extract(self) -> list[object]:
        """extract. extract words from image

        :rtype: list[object]
        """
        words = None
        with PyTessBaseAPI(lang=self.lang) as api:

            words = ocrizer(self.image, api)

        return words

    def make_para(self) -> list[tuple]:
        """make_para. make paragraphs from picture

        :rtype: list[tuple]
        """
        words = self.extract()
        pos_paras = make_paragraphs(words)
        paragraphs = []
        for para in pos_paras:
            paragraphs.append((fill_word_para(words, para), para))
        return paragraphs


def ocrizer(image: object, api: PyTessBaseAPI) -> list[object]:
    """ocrizer. Ocrize text

    :param image: image to be ocrized
    :type image: object
    :param api: api to be used
    :type api: PyTessBaseAPI
    :rtype: list[object]
    """

    t = time.time()
    api.SetImage(image)
    api.Recognize()
    ri = api.GetIterator()
    words = get_words_bbox(ri, api=api)

    logger.debug("OCR  ending at " + str(time.time() - t))
    return words


def get_words_bbox(
    ri: object, level: list[object] = [RIL.TEXTLINE, RIL.WORD, RIL.SYMBOL], api=None
) -> list[TessObject]:
    """get_words_bbox. Get words bouding box

    :param ri:
    :type ri: object
    :param level:
    :type level: list[object]
    :param api:
    :rtype: list[TessObject]
    """
    lines = []
    for r in iterate_level(ri, level[1]):

        bbox = r.BoundingBoxInternal(level[1])
        # left, top, right, bottom x,y,w,h
        if bbox is not None:
            text = r.GetUTF8Text(level[1])

            if len(re.sub("\s*", "", text)) > 0:  # text != "" or text != "\n":
                if api is None:
                    children = []
                else:
                    children = []
                    ri_children = api.GetIterator()
                    for rc in iterate_level(ri_children, level[2]):
                        bbox_c = rc.BoundingBoxInternal(level[2])
                        if bbox_c is not None and boxinbox(bbox_c, bbox):
                            child = TessObject()
                            child.text = rc.GetUTF8Text(level[2])
                            child.bbox = bbox_c
                            children.append(child)
                line = TessObject(children=children)
                line.text = text
                line.bbox = [
                    round(bbox[0]),
                    round(bbox[1]),
                    round(bbox[2]),
                    round(bbox[3]),
                ]

                line.conf = r.Confidence(level[1])
                line.new_line = r.IsAtBeginningOf(level[0])
                line.block = r.IsAtBeginningOf(RIL.BLOCK)
                line.para = r.IsAtBeginningOf(RIL.PARA)
                lines.append(line)

    return lines


def make_paragraphs(words: list[TessObject]) -> list[(int, int, int, int)]:
    """make_paragraphs. make paragraphs from ocr result

    :param words:
    :type words: list[TessObject]
    :rtype: list[(int, int, int, int)]
    """
    pos_para = None
    pos_paras = []
    for word in words:
        bbox = word.bbox
        if not word.para:
            if pos_para is None:
                pos_para = bbox
            else:
                pos_para = (
                    min(pos_para[0], bbox[0]),
                    min(pos_para[1], bbox[1]),
                    max(pos_para[2], bbox[2]),
                    max(pos_para[3], bbox[3]),
                )
        else:
            if pos_para is not None:
                pos_paras += [pos_para]
            pos_para = bbox
    return pos_paras


def fill_word_para(
    words: list[object], pos_para: (int, int, int, int)
) -> (str, list[object]):
    """fill_word_para. fill words into paragraphs

    :param words:
    :type words: list[object]
    :param pos_para:
    :type pos_para: (int, int, int, int)
    :rtype: (str, list[object])
    """
    text = ""
    words_para = []
    for word in words:
        if boxinbox(word.bbox, pos_para):
            words_para += [word]
            if word.new_line and text != "":
                text += "\n"
            elif text != "":
                text += " "
            text += word.text
    return text, words_para


def boxinbox(box1: (int, int, int, int), box2: (int, int, int, int)) -> bool:
    """boxinbox. check if a box is inside another bounding box

    :param box1: box to be inside
    :type box1: (int, int, int, int)
    :param box2:
    :type box2: (int, int, int, int)
    :rtype: bool
    """
    x, y, x1, y1 = box1
    x2, y2, x3, y3 = box2
    if x2 <= x <= x3 and y2 <= y <= y3 and x2 <= x1 <= x3 and y2 <= y1 <= y3:
        return True
    else:
        return False
