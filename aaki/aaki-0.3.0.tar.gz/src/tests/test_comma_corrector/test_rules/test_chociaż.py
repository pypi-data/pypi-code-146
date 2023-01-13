from ..test_comma_corrector import TestCommaCorrector


class TestChociaż(TestCommaCorrector):
    def test_chociaż(self):
        sentences = [
            "Zdał egzamin, chociaż w ogóle się nie uczył.",
            "Muszę tam iść, chociaż nie mam na to ochoty."
        ]

        self.assertSentences(sentences)
    
    def test_chociaż_pocz(self):
        sentences = [
            "Chociaż jestem chory, pójdę dziś do pracy.",
            "Chociaż wciąż jest zima, robi się coraz cieplej."
        ]

        self.assertSentences(sentences)
    
    def test_chociaż_part(self):
        sentences = [
            "Mogłaś chociaż przeprosić.",
            "Daj mi chociaż dzisiaj spokój."
        ]

        self.assertSentences(sentences)