from ..test_comma_corrector import TestCommaCorrector


class TestJednak(TestCommaCorrector):
    def test_jednak_conj(self):
        sentences = [
            "Na miejsce przyjechała karetka pogotowia, jednak było już za późno.",
            "Obiecał dochować tajemnicy, jednak wszystko im powiedział."
        ]

        self.assertSentences(sentences)
    
    def test_jednak_pocz(self):
        sentences = [
            "Było bardzo zimno, postanowiliśmy jednak iść na spacer.",
            "Pracowałem ciężko, ciągle jednak brakowało mi pieniędzy."
        ]

        self.assertSentences(sentences)

    def test_jednak_part(self):
        sentences = [
            "Miałeś jednak rację.",
            "Kłamstwo jednak zawsze wyjdzie na jaw."
        ]

        self.assertSentences(sentences)
