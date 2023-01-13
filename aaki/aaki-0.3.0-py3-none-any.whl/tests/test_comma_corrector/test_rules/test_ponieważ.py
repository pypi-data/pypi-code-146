from ..test_comma_corrector import TestCommaCorrector


class TestPonieważ(TestCommaCorrector):
    def test_ponieważ(self):
        sentences = [
            "Nie mogę teraz rozmawiać, ponieważ jestem bardzo zajęty.",
            "Wróciliśmy dziś wcześniej do domu, ponieważ pogoda nie sprzyjała spacerom."
        ]
    
        self.assertSentences(sentences)
    
    def test_ponieważ_pocz(self):
        sentences = [
            "Ponieważ jestem bardzo zmęczona, muszę położyć się dziś wcześnie spać.",
            "Ponieważ musiałem wyjechać, nie byłem wczoraj w pracy."
        ]
    
        self.assertSentences(sentences)
    
    def test_ponieważ_wtr(self):
        sentences = [
            "Dzisiejsze zebranie, ponieważ było bardzo ważne, przedłużyło się o godzinę.",
            "Gatunek ten, ponieważ jest zagrożony, powinno się chronić szczególnie."
        ]
    
        self.assertSentences(sentences)