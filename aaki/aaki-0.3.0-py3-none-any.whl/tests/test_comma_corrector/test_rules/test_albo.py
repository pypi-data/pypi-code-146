from ..test_comma_corrector import TestCommaCorrector


class TestAlbo(TestCommaCorrector):
    def test_albo_powt(self):
        sentences = [
            "Albo pójdziemy do teatru, albo do kina.",
            "Wrócę do domu albo za godzinę, albo za dwie, albo za trzy."
        ]

        self.assertSentences(sentences)
    
    def test_albo_dopow(self):
        sentences = [
            "Był zawsze uczniem niezwykle zdolnym, albo raczej bardzo pilnym.",
            "Zwykle wykazywał się niesamowitą odwagą, albo raczej brawurą."
        ]

        self.assertSentences(sentences)
    

    def test_albo_wtr(self):
        sentences = [
            "Zwykle jestem bardzo ostrożna, albo raczej tchórzliwa, dlatego unikam niepewnych sytuacji."
        ]

        self.assertSentences(sentences)
    
    def test_albo_rown(self):
        sentences = [
            "Teraz albo nigdy.",
            "Kup ryż albo makaron.",
            "Wieczorami lubię czytać książki albo słuchać muzyki."
        ]

        self.assertSentences(sentences)
