from ..test_comma_corrector import TestCommaCorrector


class TestBo(TestCommaCorrector):
    def test_bo(self):
        sentences = [
            "Zostaniemy dziś w domu, bo na dworze jest bardzo zimno.",
            "Wiem, bo czytałem o tym w gazecie.",
            "Załóż czapkę, bo zmarzniesz.",
            "Te informacje są dla nas nieprzydatne, bo nieaktualne.",
            "Drogie, bo drogie, ale jakie piękne."
        ]

        self.assertSentences(sentences)