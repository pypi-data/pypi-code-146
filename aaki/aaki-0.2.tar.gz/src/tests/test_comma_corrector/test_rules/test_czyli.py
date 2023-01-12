from ..test_comma_corrector import TestCommaCorrector


class TestCzyli(TestCommaCorrector):
    def test_czyli(self):
        sentences = [
            "Przyjdę do ciebie po lekcjach, czyli około piętnastej.",
            "Osobom niepełnosprawnym zaleca się felinoterapię, czyli metodę terapii polegającą na kontakcie z kotem."
        ]

        self.assertSentences(sentences)
    
    def test_czyli_wtr(self):
        sentences = [
            "Wiek pary i elektryczności, czyli wiek XIX, oznaczał wielką rewolucję przemysłową.",
            "FE, czyli żelazo, to pierwiastek chemiczny o liczbie atomowej 26."
        ]

        self.assertSentences(sentences)