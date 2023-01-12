from ..test_comma_corrector import TestCommaCorrector


class TestZanim(TestCommaCorrector):
    def test_zanim(self):
        sentences = [
            "Wyszłam, zanim wróciłeś do domu.",
            "Zrób zakupy, zanim pójdziesz do kina.",
            "Zdążyłem dobiec na przystanek, zanim odjechał autobus."
        ]

        self.assertSentences(sentences)

    def test_zanim_pocz(self):
        sentences = [
            "Zanim odpowiesz, zastanów się dobrze."
            "Zanim zdecyduję się na wyjazd, muszę złożyć wniosek o urlop."
        ]

        self.assertSentences(sentences)

    def test_zanim_wtr(self):
        sentences = [
            "Zawsze, zanim wyjdę z domu, sprawdzam, czy zamknęłam wszystkie okna."
            "Codziennie, zanim pójdę do pracy, biegam w pobliskim parku."
        ]

        self.assertSentences(sentences)