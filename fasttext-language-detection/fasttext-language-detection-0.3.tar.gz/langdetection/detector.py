import os
import fasttext
from functools import lru_cache
from .log import logger
import urllib.request

# delete warnings
fasttext.FastText.eprint = lambda x: None


@lru_cache()
def load_model(low_memory=True):
    if low_memory:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'lid.176.ftz')
    else:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'lid.176.bin')
    model = fasttext.load_model(model_path)
    return model


def check_or_download_high_memory_model():
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'lid.176.bin')
    if not os.path.isfile(model_path):
        logger.info('Downloading lid.176.bin model ...')
        url = 'https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin'
        urllib.request.urlretrieve(url, model_path)


class LanguageDetector:
    """This class detects the language of text with fasttext pretrained model."""

    def __init__(self, low_memory=True):
        if not low_memory:
            check_or_download_high_memory_model()
        self.model = load_model(low_memory=low_memory)

    def detect(self, text: str):
        """Detect language and probability of text
        """
        prediction = self.model.predict(text)
        if not prediction:
            return {}
        languages, probs = prediction
        lang = languages[0].replace('__label__', '')
        prob = float(probs[0])
        return {'lang': lang, 'prob': prob}
