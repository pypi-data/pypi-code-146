import logging
import re

try:
    import enchant
    from enchant.checker import SpellChecker
    from enchant.tokenize import EmailFilter, Filter, URLFilter, WikiWordFilter

    _enchant = True
except ImportError:
    _enchant = False
from functools import partial

logger = logging.getLogger(__name__)

escape_char = re.compile(r"\\x[0123456789abcdef]+")
break_space = re.compile(r"\u00a0")
word_ocr_correction = {r"(^|[\n(])¢": r"\1c", r"(^|[\n(])@": r"\1a", "™": r"”"}


def correct(mod: str) -> callable:
    """correct. corrector to be used

    :param mod: which dictionnary to be used, default = aspell
    :type mod: str
    :rtype: callable
    """
    if _enchant is True:
        return partial(corr, mod=mod)
    else:
        return None


def corr(text: str, lang: str, mod: str = "aspell") -> str:
    """corr. words corrector

    :param text: text te be corrected
    :type text: str
    :param lang: text's language
    :type lang: str
    :param mod: dictionnary to be used, default aspell
    :type mod: str
    :rtype: str
    """
    chkr = enchant_corrector(lang, mod=mod)
    return correction(chkr, text)


def enchant_corrector(lang: str, mod: str = "aspell") -> object:
    """enchant_corrector. enchant spell checker

    :param lang:
    :type lang: str
    :param mod: dictionnary to be used, default aspell
    :type mod: str
    :rtype: object
    """
    b = enchant.Broker()

    b.set_ordering("*", mod)
    dict_ = b.request_dict(lang)

    chkr = SpellChecker(
        dict_,
        filters=[
            EmailFilter,
            URLFilter,
            WikiWordFilter,
            UpperCaseFilter,
            CapitalizeFilter,
        ],
    )

    return chkr


class CapitalizeFilter(Filter):
    """Filter skipping over UpperCase word.
    This filter skips any words matching the following regular expression:

           ^([A-Z]\w+[A-Z]+\w+)

    That is, any words that are WikiWords.
    """

    _pattern = re.compile(r"^([A-Z]\w+)")

    def _skip(self, word):
        """_skip.

        :param word:
        """
        if self._pattern.match(word):
            return True
        return False


class UpperCaseFilter(Filter):
    """Filter skipping over UpperCase word.
    This filter skips any words matching the following regular expression:

           ^([A-Z]\w+[A-Z]+\w+)

    That is, any words that are WikiWords.
    """

    _pattern = re.compile(r"^([A-Z]+)")

    def _skip(self, word):
        """_skip.

        :param word:
        """
        if self._pattern.match(word):
            return True
        return False


def correction(chkr: object, txt: str) -> str:
    """correction. enchant words corrector

    :param chkr:
    :type chkr: object
    :param txt:
    :type txt: str
    :rtype: str
    """
    txt = re.sub(escape_char, "", txt)
    txt = re.sub(break_space, " ", txt)
    for key, value in word_ocr_correction.items():
        txt = re.sub(key, value, txt)
    chkr.set_text(txt)
    for err in chkr:
        if len(err.suggest()) > 0:
            sug = err.suggest()[0]
        else:
            sug = ""
        err.replace(sug)

    txt = chkr.get_text()
    return txt
