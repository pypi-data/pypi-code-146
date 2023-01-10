from langdetection.detector import LanguageDetector


def test_low_memory_language_detector():
    language_detector = LanguageDetector(low_memory=True)
    text = 'En un lugar de la Mancha, de cuyo nombre no quiero acordarme'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'es'

    text = 'Hello world!'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'en'

    text = 'Bonjour le monde!'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'fr'

    text = 'Olá mundo!'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'pt'

    text = 'ハローワールド'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'ja'

    text = '你好，世界!'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'zh'

    text = ''
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection


def test_low_memory_false_language_detector():
    language_detector = LanguageDetector(low_memory=False)
    text = 'En un lugar de la Mancha, de cuyo nombre no quiero acordarme'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'es'

    text = 'Hello world!'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'en'

    text = 'Bonjour le monde!'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'fr'

    text = 'Olá mundo!'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'pt'

    text = ''
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection

    text = 'ハローワールド'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'ja'

    text = '你好，世界!'
    detection = language_detector.detect(text)
    assert 'lang' in detection and 'prob' in detection
    assert detection['lang'] == 'zh'

    language_detector_2 = LanguageDetector(low_memory=False)
    text = ''
    detection = language_detector_2.detect(text)
    assert 'lang' in detection and 'prob' in detection
