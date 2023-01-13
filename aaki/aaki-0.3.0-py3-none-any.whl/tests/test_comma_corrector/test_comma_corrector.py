import unittest

from aaki.comma_corrector.comma_corrector import CommaCorrector

class TestCommaCorrector(unittest.TestCase):
    def setUp(self) -> None:
        self.corrector = CommaCorrector()

    def assertSentences(self, sentences: list[str]) -> None:
        no_commas_sentences = [sentence.replace(',', '') for sentence in sentences]

        corrected_sentences = self.corrector.correct(no_commas_sentences)

        for sentence, corrected_sentence in zip(sentences, corrected_sentences):
            with self.subTest(sentence=sentence, corrected_sentence=corrected_sentence):
                self.assertEqual(corrected_sentence, sentence)
