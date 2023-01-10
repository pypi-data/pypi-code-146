import logging

try:
    from translate import Translator

    _translate = True
except ImportError:
    _translate = False

try:
    import argostranslate.translate

    _argos = True
except ImportError:
    _argos = False

logger = logging.getLogger(__name__)


def translate(mod: str) -> callable:
    """translate. Translator to use

    :param mod: can be "translate" to use translate package, "argos" to use argostranslate package or "auto" to use the one available if any
    :type mod: str
    :rtype: callable | None
    """
    if mod == "translate" or (mod == "auto" and _translate is True):
        return tslt
    elif mod == "argos" or (mod == "auto" and _argos is True):
        return argostranslate.translate.translate
    else:
        return None


def tslt(text: str, from_lang: str, to_lang: str) -> str:
    """tslt. translate a text using "translate" package

    :param text: text to be translated
    :type text: str
    :param from_lang: language to be translated from in 2 letters
    :type from_lang: str
    :param to_lang:  language to translate in 2 letters
    :type to_lang: str
    :rtype: str
    """
    try:
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        return translator.translate(text)
    except Exception as e:
        logger.error(str(e))
        return text
