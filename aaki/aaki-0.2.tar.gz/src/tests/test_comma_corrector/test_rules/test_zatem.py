from ..test_comma_corrector import TestCommaCorrector


class TestZatem(TestCommaCorrector):
    def test_zatem(self):
        sentences = [
            "Odrobiłam lekcje, zatem teraz mogę odpocząć."
        ]

        self.assertSentences(sentences)

    def test_zatem_mid(self):
        sentences = [
            "Wszystko jest gotowe, możemy zatem zaczynać.",
            "Mam ochotę obejrzeć film, pójdę zatem do kina."
        ]

        self.assertSentences(sentences)

    def test_zatem_poprz(self):
        sentences = [
            "Musimy zatem jechać.",
            "Pójdę zatem do sklepu."
        ]

        self.assertSentences(sentences)
