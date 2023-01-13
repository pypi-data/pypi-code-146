from ..test_comma_corrector import TestCommaCorrector


class TestNawet(TestCommaCorrector):
    def test_nawet(self):
        sentences = [
            "Przyszła i nawet się nie odezwała.",
            "Nie zostawiła po sobie nawet jednego śladu."
        ]

        self.assertSentences(sentences)

    def test_nawet_konkr(self):
        sentences = [
            "U nas jest zimno, nawet latem.",
            "Zawsze jej towarzyszył, nawet w chwilach największego zagrożenia.",
            "Dalej tam pracowałem, nawet awansowałem.",
        ]

        self.assertSentences(sentences)

    def test_nawet_srod(self):
        sentences = [
            "Jego książki były dobre, nawet świetne, ale nie zgodził się na ich publikację.",
            "Zrezygnowała ze wszystkiego, nawet z najdrobniejszych przyjemności, aby im pomóc."
        ]

        self.assertSentences(sentences)