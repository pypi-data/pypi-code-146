from ..test_comma_corrector import TestCommaCorrector


class TestBądź(TestCommaCorrector):
    def test_bądź(self):
        sentences = [
            "Przyjadę do ciebie tramwajem bądź autobusem.",
            "Latem wyjadę nad morze bądź zostanę w domu."
        ]

        self.assertSentences(sentences)

    def test_bądź_join(self):
        sentences = [
            "Dokumenty proszę dostarczyć osobiście bądź też przesłać listownie."
        ]

        self.assertSentences(sentences)

    def test_bądź_powt(self):
        sentences = [
            "Na deser podam bądź lody, bądź ciasto.",
            "Egzamin można zdawać bądź ustnie, bądź pisemnie."
        ]

        self.assertSentences(sentences)

    def test_bądź_part(self):
        sentences = [
            "Połóż to gdzie bądź.",
            "Zawołaj kogo bądź."
        ]

        self.assertSentences(sentences)

    def test_bądź_co_bądź(self):
        sentences = [
            "To twój bądź co bądź ojciec."
        ]

        self.assertSentences(sentences)
