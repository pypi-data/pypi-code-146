import logging

from .make_picture import Piconv
from .paragraphs import makeParagraphs

logger = logging.getLogger(__name__)


def convert(
    image: object,
    lang: str,
    to_lang: str,
    corrector: str = "False",
    translator: str = "auto",
    path_save: str = "",
    debug: bool = False,
    show: bool = False,
) -> object:
    """convert. translate a picture

    :param image: image to be translated
    :type image: object
    :param lang: image's language
    :type lang: str
    :param to_lang: language to be translated
    :type to_lang: str
    :param corrector: corrector to used, can be "False" or a dictionnary to be used from enchant library
    :type corrector: str
    :param translator: translator to be used, can be a callable, "auto", "translate" ,"argos"
    :type translator: str
    :param path_save: path to save the picture created
    :type path_save: str
    :param debug:
    :type debug: bool
    :param show: show the picture
    :type show: bool
    :rtype: object
    """
    if corrector.lower() == "false":
        corrector = False
    if translator == "":
        translator = None
    paragraphs = makeParagraphs(
        image, lang, to_lang, corrector=corrector, translator=translator
    )
    picture = Piconv(image, paragraphs, debug=debug)
    pics = picture.convert()
    if show:
        pics.show()
    if path_save != "":
        pics.save(path_save)
    return pics
