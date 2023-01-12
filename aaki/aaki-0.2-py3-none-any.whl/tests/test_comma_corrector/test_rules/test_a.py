from ..test_comma_corrector import TestCommaCorrector


class TestA(TestCommaCorrector):
    def test_a(self):
        sentences = [
            "Zdecydowaliśmy się kupić mieszkanie, a nie dom.",
            "Pojechał samochodem, a nie autobusem.",
            "Damian czeka na ciebie od 10 minut, a ty ciągle wybierasz ubranie.",
            "Wiem, że zajmował się hodowlą węży, skorpionów, pająków, a nawet patyczaków."
        ]

        self.assertSentences(sentences)

    def test_a_także(self):
        sentences = [
            "Latem zwiedziłam Włochy, Hiszpanię i Francję, a także Turcję.",
            "Odpowiedzialność za to spoczywa na uczniach, a także ich rodzicach.",
            "Chciał spędzić ten czas aktywnie, a także odpocząć."
        ]

        self.assertSentences(sentences)