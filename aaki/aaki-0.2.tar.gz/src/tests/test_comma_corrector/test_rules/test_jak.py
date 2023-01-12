from ..test_comma_corrector import TestCommaCorrector


class TestJak(TestCommaCorrector):
    def test_jak(self):
        sentences = [
            "Powiem Ci, jak to zrobiłem.",
            "Nie wiem, jak ty, ale spróbowałbym użyć wkrętarki.",
            "W dobrej grze, jak w dobrym filmie, akcja toczy się wartko.",
            "Szybki jak błyskawica.",
            "Marta bardzo lubi owoce tropikalne, takie jak ananasy, banany, brzoskwinie i pomarańcze.",
            "Był równie zmęczony, jak zadowolony.",
            "Adam był tak samo szybki jak Dawid.",
            "Daniel postąpił tak, jak doradziła mu Marta.",
            "Ich oczom ukazał się wysoki dom z zielonym dachem, taki sam jak opisywała go Agnieszka."
        ]

        self.assertSentences(sentences)

    def test_podobnie_jak(self):
        sentences = [
            "Ona ubrała się podobnie jak ja.",
            "Zrób to podobnie jak oni."
        ]

        self.assertSentences(sentences)

    def test_podobnie_jak_wtr(self):
        sentences = [
            "Dzisiaj i wczoraj, podobnie jak dwa dni temu, padał deszcz.",
            "Zawsze robisz mi na złość, podobnie jak twoja siostra."
        ]

        self.assertSentences(sentences)
    
    def test_jak_również(self):
        sentences = [
            "Lubię filmy przygodowe, obyczajowe, jak również sensacyjne.",
            "W konkursie mogą wziąć udział zawodowi pisarze, jak również amatorzy."
        ]

        self.assertSentences(sentences)
    
    def test_taki_jak(self):
        sentences = [
            "Człowiek taki jak ty nie powinien zabierać głosu w tej sprawie.",
            "Jesteś taka nieśmiała jak twoja siostra."
        ]

        self.assertSentences(sentences)
    
    def test_jak_i(self):
        sentences = [
            "Martwił mnie jej stan zdrowia, jak i to, że nie wiedziałem, co nastąpi potem.",
            "Suka, jak i szczenięta, wymagały opieki weterynarza."
        ]

        self.assertSentences(sentences)