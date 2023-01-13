from ..test_comma_corrector import TestCommaCorrector


class TestCo(TestCommaCorrector):
    def test_co_wpro(self):
        sentences = [
            "Zapomniałam, co mówiłeś wczoraj.",
            "Robił, co chciał."
        ]

        self.assertSentences(sentences)
    
    def test_co_przed_orz(self):
        sentences = [
            "To, co jest dobre dla ciebie, nie musi być odpowiednie dla mnie.",
            "Dobra książka to coś, co lubię najbardziej.",
            "Chcę ci życzyć wszystkiego, co najlepsze."
        ]

        self.assertSentences(sentences)
    
    def test_co_okol(self):
        sentences = [
            "Nie mam co robić.",
            "U nich w domu nie było co jeść."
        ]

        self.assertSentences(sentences)
    
    def test_co_part(self):
        sentences = [
            "Opuszczał lekcje co najmniej raz w tygodniu.",
            "Do kina chodzę średnio co miesiąc."
        ]

        self.assertSentences(sentences)