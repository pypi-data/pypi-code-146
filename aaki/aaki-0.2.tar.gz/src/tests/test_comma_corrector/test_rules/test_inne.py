from ..test_comma_corrector import TestCommaCorrector


class TestInne(TestCommaCorrector):
    def test_poza_tym(self):
        sentences = [
            "Ugotowałam obiad, poza tym zrobiłam deser.",
            "Nie lubię go, poza tym drażni mnie jego stosunek do pewnych spraw.",
            "Umiem grać na gitarze, pianinie i flecie, poza tym trochę na skrzypcach."
        ]

        self.assertSentences(sentences)

    def test_dzięki_temu(self):
        sentences = [
            "Na dworzec dotarłem o szesnastej, dzięki temu zdążyłem na pociąg.",
            "Lekcje odrobiłam zaraz po przyjściu ze szkoły, dzięki temu mam wolny wieczór."
        ]

        self.assertSentences(sentences)
    
    def test_dzięki_temu_rzecz_cel(self):
        sentences = [
            "Zdałam ten egzamin dzięki twojej pomocy.",
            "Odniosła sukces dzięki odwadze."
        ]

        self.assertSentences(sentences)
    
    def test_dzięki_temu_pocz(self):
        sentences = [
            "Dzięki temu nauczycielowi polubiłam fizykę.",
            "Dzięki twojemu zaangażowaniu nasza firma odniosła sukces."
        ]

        self.assertSentences(sentences)
    
    def test_co_więcej(self):
        sentences = [
            "Nie sądziłam, że mnie to spotka, co więcej, myślałam, że to wręcz nierealne.",
            "Moja babcia ma ponad osiemdziesiąt lat, ale dalej cieszy się dobrym zdrowiem. Co więcej, wciąż jeździ na rowerze.",
            "Bardzo ją polubiłem, co więcej, ja się w niej zakochałem!"
        ]

        self.assertSentences(sentences)