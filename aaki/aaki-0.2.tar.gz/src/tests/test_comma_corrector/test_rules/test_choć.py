from ..test_comma_corrector import TestCommaCorrector


class TestChoć(TestCommaCorrector):
    def test_choć_conj(self):
        sentences = [
            "Uprawiał sport, choć był niepełnosprawny.",
            "Poszła tam, choć nie powinna."
        ]

        self.assertSentences(sentences)
    
    def test_choć_conj_pocz(self):
        sentences = [
            "Choć jestem przeziębiony, muszę iść do pracy.",
            "Choć nie jestem o tym przekonany, zrobię to."
        ]

        self.assertSentences(sentences)
    
    def test_choć_part(self):
        sentences = [
            "Zrób choć zakupy.",
            "Powinieneś choć przeprosić."
        ]

        self.assertSentences(sentences)