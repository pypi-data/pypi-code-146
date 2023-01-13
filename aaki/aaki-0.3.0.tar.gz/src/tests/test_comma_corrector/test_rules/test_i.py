from ..test_comma_corrector import TestCommaCorrector


class TestI(TestCommaCorrector):
    def test_i_conj(self):
        sentences = [
            "Dostałam od niego książkę i kwiaty.",
            "Kup jajka, ser i wędlinę.",
            "Lubię psy i koty."
        ]

        self.assertSentences(sentences)

    def test_i_wspl(self):
        sentences = [
            "Lubię słuchać muzyki i czytać książki.",
            "Codziennie chodzę na siłownię i ćwiczę w domu.",
            "Ona tylko ciągle narzeka i narzeka."
        ]

        self.assertSentences(sentences)

    def test_i_powt(self):
        sentences = [
            "Lubię jabłka i gruszki, i jeszcze śliwki.",
            "Latem zwiedziłam i Francję, i Holandię.",
            "I słońce świeciło, i padał deszcz.",
        ]

        self.assertSentences(sentences)

    def test_i_powt_not_rown(self):
        sentences = [
            "Byłem w kinie i spotkałem tam Piotrka i Marcina.",
            "Dotknęłam klamki i nacisnęłam ją szybko i mocno."
        ]

        self.assertSentences(sentences)

    def test_i_wtr(self):
        sentences = [
            "Znam ją od dawna, i to bardzo dobrze.",
            "Chodzę na siłownię, i to codziennie.",
            "Nie pójdę tam, i koniec."
        ]

        self.assertSentences(sentences)

    def test_i_zam_podrz(self):
        sentences = [
            "Lubię oglądać filmy, które trzymają w napięciu, i słuchać muzyki, która mnie relaksuje.",
            "Zdecyduj w końcu, co robimy, i zacznijmy działać."
        ]

        self.assertSentences(sentences)

    def test_i_cons_conj(self):
        sentences = [
            "Nie spałem dziś w nocy, i jestem bardzo zmęczony.",
            "Ta wieża jest bardzo wysoka, i nie każdy na nią wejdzie."
        ]

        self.assertSentences(sentences)
