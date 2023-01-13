from ..test_comma_corrector import TestCommaCorrector


class TestAni(TestCommaCorrector):
    def test_ani(self):
        sentences = [
            "Nie chcę herbaty ani kawy.",
            "W moim domu nie ma telewizora ani radia."
        ]

        self.assertSentences(sentences)

    def test_ani_wtr(self):
        sentences = [
            "Nie przyszedł na umówione spotkanie, ani też nie zawiadomił nikogo.",
        ]

        self.assertSentences(sentences)

    def test_ani_powt(self):
        sentences = [
            "Nie mogłam ruszyć ani ręką, ani nogą.",
            "Ani nie pracowałem, ani nie odpocząłem."
        ]

        self.assertSentences(sentences)

    def test_ani_part(self):
        sentences = [
            "Nie miał ani grosza.",
            "Nie powiedziała ani słowa."
        ]

        self.assertSentences(sentences)