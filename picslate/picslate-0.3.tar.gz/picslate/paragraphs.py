import logging

from .corrector import correct
from .tesseract.picture import Pics
from .translate import translate

logger = logging.getLogger(__name__)


class NoTranslatorFound(Exception):
    """NoTranslatorFound."""

    pass


class NoCorrectorFound(Exception):
    """NoCorrectorFound."""

    pass


class Paragraphs:
    """Paragraphs."""

    def __init__(
        self,
        text: str,
        pos: (int, int, int, int),
        from_lang: str,
        to_lang: str,
        words: list[object] | None = None,
        corrector: bool | str = False,
        translator: str = "auto",
    ) -> None:
        """__init__. Object which comport paragraphs text and meta data

        :param text: paragraph text
        :type text: str
        :param pos: paragraph position
        :type pos: (int, int, int, int)
        :param from_lang: lang of the paragraph
        :type from_lang: str
        :param to_lang: lang to be translated
        :type to_lang: str
        :param words: words inside paragraph
        :type words: list[object] | None
        :param corrector: corrector to be used
        :type corrector: bool | str | callable
        :param translator: translator to be used
        :type translator: str | callable
        :rtype: None
        """
        if callable(corrector):
            self.text = corrector(text, from_lang)
        elif corrector is False:
            self.text = text
        else:
            corrector = correct(corrector)
            if corrector is None:
                raise NoCorrectorFound
            self.text = corrector(text, from_lang)
        self.pos = pos
        self.words = words
        self.from_lang = from_lang
        self.to_lang = to_lang
        self._text_translated = None
        self.translator = translator

    @property
    def text_translated(self) -> str:
        """text_translated.

        :rtype: str
        """
        if self._text_translated is None:
            if callable(self.translator):
                translator = self.translator
            else:
                translator = translate(self.translator)
                if translator is None:
                    raise NoTranslatorFound
            self._text_translated = translator(self.text, self.from_lang, self.to_lang)

        return self._text_translated


def makeParagraphs(
    image: object,
    lang: str,
    to_lang: str,
    corrector: object = False,
    translator: object = "auto",
) -> list[Paragraphs]:
    """makeParagraphs.

    :param image:
    :type image: object
    :param lang:
    :type lang: str
    :param to_lang:
    :type to_lang: str
    :param corrector:
    :type corrector: object
    :param translator:
    :type translator: object
    :rtype: list[Paragraphs]
    """
    picture = Pics(image, lang)
    paragraphs = picture.make_para()
    paras = []
    for (text, words), pos in paragraphs:
        paras += [
            Paragraphs(
                text,
                pos,
                lang[:2],
                to_lang,
                words=words,
                corrector=corrector,
                translator=translator,
            )
        ]
    return paras
