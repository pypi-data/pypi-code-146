from ..test_comma_corrector import TestCommaCorrector


class TestGdy(TestCommaCorrector):
    def test_gdy(self):
        sentences = [
            "Było południe, gdy się obudziłem.",
            "Nie lubię, gdy się tak zachowujesz.",
            "Skończyłam studia, gdy miałam dwadzieścia pięć lat."
        ]

        self.assertSentences(sentences)

    def test_gdy_pocz(self):
        sentences = [
            "Gdy wracałam do domu, zerwał się silny wiatr.",
            "Gdy w końcu się spotkamy, wszystko dokładnie ci opowiem."
        ]

        self.assertSentences(sentences)

    def test_gdy_join(self):
        sentences = [
            "Zrozumiałam to, dopiero gdy sama tego doświadczyłam.",
            "Śpisz, podczas gdy powinieneś być już dawno w pracy."
        ]

        self.assertSentences(sentences)

    def test_zwłaszcza_gdy(self):
        sentences = [
            "Powinieneś pić dużo wody, zwłaszcza gdy jest gorąco.",
            "Lubię na nią patrzeć, zwłaszcza gdy się uśmiecha.",
            "Bywał niemiły, zwłaszcza gdy nie czuł się zbyt dobrze."
        ]

        self.assertSentences(sentences)

    def test_w_przypadku_gdy(self):
        sentences = [
            "Zrobię to, w przypadku gdy nie będzie innego wyjścia.",
        ]

        self.assertSentences(sentences)

    def test_w_przypadku_gdy_pocz(self):
        sentences = [
            "W przypadku gdy wszyscy zachorujemy, nasz wyjazd trzeba będzie przełożyć."
        ]

        self.assertSentences(sentences)

    def test_w_sytuacji_gdy(self):
        sentences = [
            "Należy przeprowadzić operację, w sytuacji gdy życie pacjenta jest zagrożone."
        ]

        self.assertSentences(sentences)

    def test_w_sytuacji_gdy_pocz(self):
        sentences = [
            "W sytuacji gdy nie dojdziemy do porozumienia, nasza dalsza współpraca nie będzie możliwa."
        ]

        self.assertSentences(sentences)
