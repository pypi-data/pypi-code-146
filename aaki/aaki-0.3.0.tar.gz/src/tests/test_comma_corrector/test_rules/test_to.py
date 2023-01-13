from ..test_comma_corrector import TestCommaCorrector


class TestTo(TestCommaCorrector):
    def test_to(self):
        sentences = [
            "Chcesz, to idź tam.",
            "Podaj telefon, to zadzwonię do niego.",
            "Opuszczałeś lekcje, to masz teraz zaległości."
        ]

        self.assertSentences(sentences)

    def test_to_compl(self):
        sentences = [
            "Jeśli chcesz, to zostań tutaj.",
            "Skoro tak bardzo ci na niej zależy, to zaproś ją do kina.",
            "Gdyby przyszła punktualnie, to nic by się nie stało."
        ]

        self.assertSentences(sentences)

    def test_to_join(self):
        sentences = [
            "Do ciasta dodaj przyprawy korzenne, to jest cynamon, goździki, kardamon i anyż.",
            "Zrobię to potem, to znaczy kiedy odrobię lekcje."
        ]

        self.assertSentences(sentences)

    def test_to_conn(self):
        sentences = [
            "Zakopane to zimowa stolica Polski.",
            "Warzywa to źródło wielu cennych witamin.",
            "Właściwie to nic na temat nie wiem."
        ]

        self.assertSentences(sentences)