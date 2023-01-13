from ..test_comma_corrector import TestCommaCorrector


class TestOraz(TestCommaCorrector):
    def test_oraz_conj(self):
        sentences = [
            "Zjem zupę oraz drugie danie."
        ]

        self.assertSentences(sentences)

    def test_oraz_other(self):
        sentences = [
            "Byli tam Piotrek, Agnieszka oraz Wojtek, oraz Maciej.",
            "Byli tam Piotrek oraz Agnieszka oraz Wojtek oraz Maciej."
        ]

        self.assertSentences(sentences)
