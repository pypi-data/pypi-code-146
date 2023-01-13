from ..test_comma_corrector import TestCommaCorrector


class TestTylko(TestCommaCorrector):
    def test_tylko(self):
        sentences = [
            "Nic nie mówił, tylko spojrzał na mnie.",
            "Nie uczyła się, tylko poszła spać."
        ]

        self.assertSentences(sentences)

    def test_tylko_part(self):
        sentences = [
            "Kupiłam tylko masło i mąkę.",
            "Mówię o tym tylko tobie."
        ]

        self.assertSentences(sentences)
    
    def test_tylko_że(self):
        sentences = [
            "Ta książka jest bardzo ciekawa, tylko że za długa.",
            "Dzisiaj jest bardzo ciepło, tylko że wieje chłodny wiatr.",
            "Był niezwykle zdolny, tylko że bardzo leniwy."
        ]

        self.assertSentences(sentences)