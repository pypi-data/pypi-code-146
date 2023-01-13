from ..test_comma_corrector import TestCommaCorrector


class TestWięc(TestCommaCorrector):
    def test_więc_cons_conj(self):
        sentences = [
            "Cały dzień pracowałem, więc teraz jestem zmęczony.",
            "Od rana padał deszcz, więc nie pojechaliśmy na wycieczkę."
        ]

        self.assertSentences(sentences)
    
    def test_więc_enum(self):
        sentences = [
            "Na miejscu stawili się wszyscy, a więc dyrektor, nauczyciele i uczniowie.",
            "Umówiłem się z nim na dwudziestą, więc za godzinę.",
            "Było tak, jak się spodziewałam, a więc autobus nie przyjechał na czas, a ja spóźniłam się do szkoły."
        ]

        self.assertSentences(sentences)
    
    def test_więc_part(self):
        sentences = [
            "Do widzenia więc!",
            "No więc słucham.",
            "A więc to twoja sprawka."
        ]

        self.assertSentences(sentences)