from ..test_comma_corrector import TestCommaCorrector


class TestIż(TestCommaCorrector):
    def test_iż(self):
        sentences = [
            "Zapomniałam, iż mieliśmy się spotkać.",
            "Obiecuję, iż zrobię to dla ciebie."
        ]

        self.assertSentences(sentences)

    def test_mimo_iż(self):
        sentences = [
            "Mimo iż wstałam dziś wcześniej niż zwykle, spóźniłam się do pracy.",
        ]

        self.assertSentences(sentences)

    def test_mimo_iż_wtr(self):
        sentences = [
            "Ta książka, mimo iż ma ciekawą fabułę, nie zachwyciła mnie szczególnie."
        ]

        self.assertSentences(sentences)
