from ..test_comma_corrector import TestCommaCorrector


class TestBy(TestCommaCorrector):
    def test_by(self):
        sentences = [
            "Uczył się dużo, by zdać egzamin.",
            "Marzę o tym, by znów tam pojechać."
        ]

        self.assertSentences(sentences)
    
    def test_by_pocz(self):
        sentences = [
            "By zdążyć dzisiaj do pracy, jechałem szybciej niż zwykle.",
            "By schudnąć, przeszłam na restrykcyjną dietę."
        ]

        self.assertSentences(sentences)
    
    def test_by_wtr(self):
        sentences = [
            "Nauczyciel prosił, by tego nie robili, wszystkich uczniów."
        ]

        self.assertSentences(sentences)
    
    def test_by_join(self):
        sentences = [
            "To była lekkomyślność, by nie powiedzieć głupota.",
            "Był znany z odwagi, by nie rzec brawury."
        ]

        self.assertSentences(sentences)