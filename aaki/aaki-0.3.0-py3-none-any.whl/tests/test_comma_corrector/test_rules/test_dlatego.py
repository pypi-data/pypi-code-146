from ..test_comma_corrector import TestCommaCorrector


class TestDlatego(TestCommaCorrector):
    def test_dlatego(self):
        sentences = [
            "Byłem zmęczony, dlatego zasnąłem bardzo wcześnie.",
            "W tym filmie gra moja ulubiona aktorka, dlatego chętnie go obejrzę.",
            "Mam mało pieniędzy, dlatego muszę oszczędzać."
        ]

        self.assertSentences(sentences)
