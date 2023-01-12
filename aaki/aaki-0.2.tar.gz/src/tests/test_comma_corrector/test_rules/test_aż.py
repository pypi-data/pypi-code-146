from ..test_comma_corrector import TestCommaCorrector


class TestAż(TestCommaCorrector):
    def test_aż_conj(self):
        sentences = [
            "Długo milczał, aż nagle krzyknął.",
            "Szłam wolno, aż w końcu przyspieszyłam kroku.",
            "Ćwiczyłem tak długo, aż się zmęczyłem.",
            "Prowadziła zbiórkę, aż zebrała potrzebną kwotę."
        ]

        self.assertSentences(sentences)

    def test_aż_part(self):
        sentences = [
            "Zjadł aż pięć kawałków tortu.",
            "Spałam dziś aż do południa."
        ]

        self.assertSentences(sentences)
