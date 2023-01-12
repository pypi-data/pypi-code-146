from ..test_comma_corrector import TestCommaCorrector


class TestLecz(TestCommaCorrector):
    def test_lecz(self):
        sentences = [
            "Zawsze byłam optymistką, lecz ostatnio mam czarne myśli.",
            "Nie jestem strachliwy, lecz rozsądny.",
            "Chciałam iść na spacer, lecz pogoda nie sprzyjała przechadzkom."
        ]

        self.assertSentences(sentences)