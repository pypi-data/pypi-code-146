from ..test_comma_corrector import TestCommaCorrector


class TestNiż(TestCommaCorrector):
    def test_niż_podrz(self):
        sentences = [
            "Jest gorzej, niż sądziłem.",
            "Dał nam więcej, niż wcześniej obiecywał.",
            "To kosztowało mniej, niż się spodziewałam."
        ]

        self.assertSentences(sentences)

    def test_niż_bezok(self):
        sentences = [
            "Wolę poczekać, niż stracić tę szansę.",
            "Łatwiej jest powiedzieć, niż zrobić."
        ]

        self.assertSentences(sentences)

    def test_niż_porown(self):
        sentences = [
            "Małgosia jest ładniejsza niż jej siostra.",
            "Lepszy wróbel w garści niż gołąb na dachu."
        ]

        self.assertSentences(sentences)
