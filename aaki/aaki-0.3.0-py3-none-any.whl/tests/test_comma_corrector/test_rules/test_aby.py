from ..test_comma_corrector import TestCommaCorrector


class TestAby(TestCommaCorrector):
    def test_aby_conj(self):
        sentences = [
            "Nastawiła budzik, aby wstać wcześnie.",
            "Aby wcześnie wstać, nastawiła budzik.",
            "Poszedł do sklepu, aby kupić słodycze.",
            "Nie mogła pozwolić sobie na to, aby wydać zbyt dużo pieniędzy."
        ]

        self.assertSentences(sentences)

    def test_tak_aby(self):
        sentences = [
            "Jechał szybko, tak aby zdążyli na samolot.",
            "Jechał tak, aby zdążyli na samolot.",
            "Mówiła szeptem, tak aby nikt nie usłyszał.",
            "Czytałam list wolno i dokładnie, tak aby niczego nie pominąć.",
            "Zrobiłam to tak, aby wszyscy byli zadowoleni.",
            "Powiedziałam to tak, aby usłyszał."
        ]

        self.assertSentences(sentences)

    def test_aby_part(self):
        sentences = [
            "Czy to aby działa?",
            "Czy to aby nie działa?"
        ]

        self.assertSentences(sentences)
