from ..test_comma_corrector import TestCommaCorrector


class TestKiedy(TestCommaCorrector):
    def test_kiedy(self):
        sentences = [
            "Nie wiem, kiedy to się stało.",
            "Przychodź do mnie, kiedy tylko chcesz."
        ]

        self.assertSentences(sentences)

    def test_kiedy_pocz(self):
        sentences = [
            "Kiedy wracałam do domu, spadł deszcz.",
            "Kiedy dzwoniłeś, byłam w łazience."
        ]

        self.assertSentences(sentences)
    
    def test_kiedy_wtr(self):
        sentences = [
            "We wtorek, kiedy szłam do pracy, spotkałam Marka.",
            "Teraz, kiedy są wakacje, nie muszę wstawać o świcie."
        ]

        self.assertSentences(sentences)