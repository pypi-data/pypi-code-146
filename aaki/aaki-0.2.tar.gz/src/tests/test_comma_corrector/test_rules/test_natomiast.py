from ..test_comma_corrector import TestCommaCorrector


class TestNatomiast(TestCommaCorrector):
    def test_natomiast(self):
        sentences = [
            "Nie mam ochoty na lody, natomiast z przyjemnością zjem kawałek tortu.",
            "Wczoraj czułam się dobrze, natomiast dzisiaj nie mam na nic siły."
        ]

        self.assertSentences(sentences)
    
    def test_natomiast_poprz(self):
        sentences = [
            "My natomiast musimy ustalić plan działania.",
            "Mam natomiast inną prośbę."
        ]

        self.assertSentences(sentences)