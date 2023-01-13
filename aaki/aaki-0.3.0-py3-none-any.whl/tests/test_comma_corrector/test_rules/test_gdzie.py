from ..test_comma_corrector import TestCommaCorrector


class TestGdzie(TestCommaCorrector):
    def test_gdzie(self):
        sentences = [
            "Wiem, gdzie jesteś.",
            "Byłem w kraju, gdzie panują dziwne zwyczaje.",
            "Powiedz mi, gdzie się ukrywasz."
        ]

        self.assertSentences(sentences)
    
    def test_gdzie_pocz(self):
        sentences = [
            "Gdzie dwóch się bije, tam trzeci korzysta."
        ]

        self.assertSentences(sentences)
    
    def test_gdzie_wtr(self):
        sentences = [
            "Tam, gdzie się znalazł, było pusto i cicho.",
            "Stąd, gdzie stałam, nie było nic widać."
        ]

        self.assertSentences(sentences)
    
    def test_gdzie_join(self):
        sentences = [
            "Pojechał na wieś, tam gdzie się urodził.",
            "Pojechał tam, gdzie się urodził."
        ]

        self.assertSentences(sentences)