from ..test_comma_corrector import TestCommaCorrector


class TestAle(TestCommaCorrector):
    def test_ale_conj(self):
        sentences = [
            "Zrobiła to, ale niedokładnie.",
            "To było pyszne, ale bardzo niezdrowe.",
            "Zarabiał niewiele, ale był bardzo oszczędny.",
            "Wprawdzie nie protestowała, ale zgodziła się niechętnie."
        ]

        self.assertSentences(sentences)

    def test_ale_part(self):
        sentences = [
            "Zobacz, ale samochód!",
            "Ale heca!",
            "Dostałem prezent, ale jaki!"
        ]

        self.assertSentences(sentences)

    def test_ale_excl(self):
        sentences = [
            "Ale, ale, my tu się dobrze bawimy, a oni czekają.",
            "Ale, ale, czy już jej powiedziałeś?"
        ]

        self.assertSentences(sentences)

    def test_ale_noun(self):
        sentences = [
            "Ona zwykle ma jakieś ale.",
            "To jest świetne, jest tylko jedno ale."
        ]

        self.assertSentences(sentences)
