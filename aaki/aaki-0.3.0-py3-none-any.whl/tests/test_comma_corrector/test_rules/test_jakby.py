from ..test_comma_corrector import TestCommaCorrector


class TestJakby(TestCommaCorrector):
    def test_jakby(self):
        sentences = [
            "Przyjechałby do ciebie, jakby miał na to czas.",
            "Wygląda, jakby spał."
        ]

        self.assertSentences(sentences)

    def test_jakby_pocz(self):
        sentences = [
            "Jakby mógł, na pewno by to zrobił.",
            "Jakby to znalazła, to by wam oddała."
        ]

        self.assertSentences(sentences)

    def test_jakby_wtr(self):
        sentences = [
            "Nagle usłyszał coś, jakby grzmot, co przerwało panującą wokół ciszę.",
            "Przyszedł, jakby na zawołanie, kiedy akurat miałam do niego dzwonić."
        ]

        self.assertSentences(sentences)

    def test_jakby_wpro(self):
        sentences = [
            "Usłyszał jakby grzmot.",
            "Dzień wydawał się jakby pogodniejszy."
        ]

        self.assertSentences(sentences)
