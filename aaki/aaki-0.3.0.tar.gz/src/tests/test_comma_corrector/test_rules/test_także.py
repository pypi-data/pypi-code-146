from ..test_comma_corrector import TestCommaCorrector


class TestTakże(TestCommaCorrector):
    def test_także(self):
        sentences = [
            "Ona także się boi.",
            "W naszym sklepie sprzedajemy także wyroby innych producentów."
        ]

        self.assertSentences(sentences)

    def test_także_dop(self):
        sentences = [
            "Nie tylko nauczyciele, także uczniowie mają swoje prawa i obowiązki.",
            "Szyła ubrania, zajmowała się także ich sprzedażą."
        ]

        self.assertSentences(sentences)
