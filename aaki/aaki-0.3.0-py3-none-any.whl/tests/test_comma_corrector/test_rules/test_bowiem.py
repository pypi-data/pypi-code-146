from ..test_comma_corrector import TestCommaCorrector


class TestBowiem(TestCommaCorrector):
    def test_bowiem(self):
        sentences = [
            "Nie przyszedł dziś do szkoły, bowiem zachorował.",
            "Nie była w stanie tego udowodnić, bowiem brakowało jej argumentów."
        ]

        self.assertSentences(sentences)

    def test_bowiem_srod(self):
        sentences = [
            "Nie zrobiłam zakupów, zapomniałam bowiem zabrać ze sobą portfel.",
            "Rząd podjął radykalne kroki, tego bowiem oczekiwali obywatele."
        ]

        self.assertSentences(sentences)

    def test_bowiem_poprz(self):
        sentences = [
            "Był on bowiem wielokrotnie poruszany w naszym gronie.",
            "Obawiałam się bowiem, że mogłaby być niebezpieczna."
        ]

        self.assertSentences(sentences)
