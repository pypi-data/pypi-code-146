from ..test_comma_corrector import TestCommaCorrector


class TestŻe(TestCommaCorrector):
    def test_że(self):
        sentences = [
            "Powiedziała, że chce jak najszybciej skończyć pracę.",
            "Sytuacja była tak trudna, że nikt nie wiedział, jak z niej wybrnąć.",
            "Był bardzo głodny, mimo że zjadł kolację.",
            "Kupiłem ich tyle, że wystarczy dla całej rodziny.",
            "Mógłbym wyjechać za granicę, tyle że nie znam języków.",
            "Napisał, że kupi mleko oraz że umyje samochód.",
            "Nie powiedział, że mnie lubi ani że mnie nie lubi."
        ]

        self.assertSentences(sentences)

    def test_chyba_że(self):
        sentences = [
            "Nie zrobię tego, chyba że coś mi obiecasz.",
            "Wyślę ten list jeszcze dzisiaj, chyba że poczta będzie zamknięta.",
            "Pojedziemy jutro na plażę, chyba że będzie padać."
        ]

        self.assertSentences(sentences)

    def test_mimo_że(self):
        sentences = [
            "Nie byłam głodna, mimo że nic dziś nie jadłam.",
            "Przyjęcie się udało, mimo że nie wszyscy goście dotarli.",
        ]

        self.assertSentences(sentences)

    def test_mimoże_pocz(self):
        sentences = [
            "Mimo że dbam o swoje zdrowie, ciągle źle się czuję."
        ]

        self.assertSentences(sentences)

    def test_mimo_że_wtr(self):
        sentences = [
            "Znów, mimo że dużo się uczyłam, nie zdałam egzaminu."
        ]

        self.assertSentences(sentences)

    def test_z_tym_że(self):
        sentences = [
            "Zacznę dziś czytać tę książkę, z tym że dopiero wieczorem.",
            "Przygotuję dziś kolację, z tym że bez mięsa.",
            "Zgodzę się na to, z tym że mam jeden warunek."
        ]

        self.assertSentences(sentences)