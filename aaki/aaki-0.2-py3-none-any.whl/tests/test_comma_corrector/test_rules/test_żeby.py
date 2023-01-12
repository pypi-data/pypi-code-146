from ..test_comma_corrector import TestCommaCorrector


class TestŻeby(TestCommaCorrector):
    def test_żeby(self):
        sentences = [
            "Muszę dużo się uczyć, żeby zdać egzaminy.",
            "Chcę wyjechać, żeby odpocząć.",
            "Jesteś zbyt dumny, żeby o to poprosić.",
            "Podjęła tę pracę, żeby tylko zarobić pieniądze."
        ]

        self.assertSentences(sentences)
    
    def test_żeby_pocz(self):
        sentences = [
            "Żeby odpocząć, muszę wyjechać.",
            "Żeby wygrać nagrodę, trzeba wziąć udział w konkursie."
        ]

        self.assertSentences(sentences)
