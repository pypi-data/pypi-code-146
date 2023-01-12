from ..test_comma_corrector import TestCommaCorrector


class TestJeżeli(TestCommaCorrector):
    def test_jeżeli(self):
        sentences = [
            "Pójdziemy na spacer, jeżeli będzie ładna pogoda."
        ]

        self.assertSentences(sentences)
    
    def test_jeżeli_pocz(self):
        sentences = [
            "Jeżeli nie zdam tego egzaminu, będę musiał znów się uczyć."
        ]

        self.assertSentences(sentences)