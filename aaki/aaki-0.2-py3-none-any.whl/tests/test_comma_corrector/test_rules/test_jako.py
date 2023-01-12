from ..test_comma_corrector import TestCommaCorrector


class TestJako(TestCommaCorrector):
    def test_jako(self):
        sentences = [
            "Pojechał tam jako przedstawiciel naszego kraju.",
            "Uważam, że jako rodzic mam decydujący głos w sprawie wychowania mojego syna.",
            "Przyszedłem tam jako pierwszy."
        ]

        self.assertSentences(sentences)

    def test_jako_wtr(self):
        sentences = [
            "Szkoła, jako placówka oświatowa, powinna znać edukacyjne potrzeby uczniów.",
            "Marek, jako nauczyciel, cieszył się sympatią wśród uczniów."
        ]

        self.assertSentences(sentences)

    def test_jako_przycz(self):
        sentences = [
            "Był ceniony, jako wybitny naukowiec.",
            "Jest bardzo popularny, jako gwiazda muzyki pop.",
            "Masz prawo do zasiłku, jako rodzic."
        ]

        self.assertSentences(sentences)

    def test_jako_że(self):
        sentences = [
            "Zadzwonił do niej, jako że nie przyszła dziś do szkoły.",
            "Poszła do lekarza, jako że źle się czuła."
        ]

        self.assertSentences(sentences)
    
    def test_jako_że_pocz(self):
        sentences = [
            "Jako że od miesiąca stosuję dietę, schudłam już pięć kilogramów.",
            "Jako że przez całe życie zajmowałam się tym zagadnieniem, wiem prawie wszystko na ten temat."
        ]

        self.assertSentences(sentences)
    
    def test_jako_że_wtr(self):
        sentences = [
            "Moja mama, jako że jest pielęgniarką, mogła zrobić mi ten zastrzyk.",
            "Ta książka, jako że jest kompleksowym opracowaniem, da ci odpowiedzi na wszystkie pytania."
        ]