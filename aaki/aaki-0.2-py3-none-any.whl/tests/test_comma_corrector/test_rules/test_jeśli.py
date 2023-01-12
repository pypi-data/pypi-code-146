from ..test_comma_corrector import TestCommaCorrector


class TestJeśli(TestCommaCorrector):
    def test_jeśli(self):
        sentences = [
            "Zadzwonię do ciebie, jeśli tylko będę mogła.",
            "Zrobię to, jeśli coś mi obiecasz."
        ]

        self.assertSentences(sentences)
    
    def test_jeśli_pocz(self):
        sentences = [
            "Jeśli się nie myślę, jutro masz urodziny.",
            "Jeśli opowiesz mi o wszystkim, postaram się to zrozumieć."
        ]

        self.assertSentences(sentences)