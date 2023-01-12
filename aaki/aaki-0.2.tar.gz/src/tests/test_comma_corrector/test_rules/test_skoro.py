from ..test_comma_corrector import TestCommaCorrector


class TestSkoro(TestCommaCorrector):
    def test_skoro(self):
        sentences = [
            "Zrobię to, skoro tak nalegasz.",
            "Musiał dziwnie wyglądać, skoro wszyscy zwracali na niego uwagę.",
            "Jak mam im ufać, skoro zawiedli mnie już tyle razy."
        ]

        self.assertSentences(sentences)

    def test_skoro_pocz(self):
        sentences = [
            "Skoro nie możesz mi pomóc, to chociaż nie przeszkadzaj.",
            "Skoro nie zrozumiałaś, musiałam wyrazić się niezbyt jasno."
        ]

        self.assertSentences(sentences)

    def test_skoro_wtr(self):
        sentences = [
            "Postanowiłam, że pod koniec wakacji, skoro wtedy mam urlop, wybiorę się do Paryża.",
            "Iść z tobą do kina, skoro sobie tego nie życzysz, nie zamierzam."
        ]

        self.assertSentences(sentences)
