from ..test_comma_corrector import TestCommaCorrector


class TestKtóry(TestCommaCorrector):
    def test_który(self):
        sentences = [
            "Nie wiem, który z was mówi prawdę.",
            "Podaj mi tę książkę, która leży na biurku."
        ]

        self.assertSentences(sentences)

    def test_który_pocz(self):
        sentences = [
            "Który z nich jest godny zaufania, naprawdę nie wiem."
        ]

        self.assertSentences(sentences)

    def test_który_wtr(self):
        sentences = [
            "Obraz, który widzimy, pochodzi z XVIII wieku.",
            "Ta kobieta, którą spotkałam, powiedziała mi, że wszystko jest w porządku."
        ]

        self.assertSentences(sentences)

    def test_który_join(self):
        sentences = [
            "To jest dom, w którym się wychowałam.",
            "Marek to człowiek, na którego można liczyć.",
            "Byłam ostatnio koncercie, podczas którego włączył się alarm przeciwpożarowy."
        ]

        self.assertSentences(sentences)

    def test_który_powt(self):
        sentences = [
            "Znałam kobietę, która uwielbiała koty i która miała ich w domu aż osiem.",
            "To jest dom, który jest w bardzo dobrym stanie i który nie wymaga remontu."
        ]

        self.assertSentences(sentences)
