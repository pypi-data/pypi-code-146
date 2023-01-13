from ..test_comma_corrector import TestCommaCorrector


class TestCzy(TestCommaCorrector):
    def test_czy_conj(self):
        sentences = [
            "Zjesz cukierka czy ciastko?",
            "Idziesz pobiegać czy chcesz odpocząć?",
            "Najczęściej gościmy u nas turystów z Niemiec, Austrii czy Turcji.",
            "To był Adam czy Marcin, czy Andrzej?",
            "Było to chyba we wtorek, czy może w środę, naprawdę nie pamiętam.",
            "Kupiła dwie sukienki, chyba zieloną i pomarańczową, czy coś w tym stylu."
        ]

        self.assertSentences(sentences)

    def test_czy_part(self):
        sentences = [
            "Nie wiem, czy to zrobił.",
            "Musimy najpierw ustalić, czy to w ogóle możliwe.",
            "Tak naprawdę nie wiadomo, czy była tam tego dnia.",
            "Od tego, czy sprzedamy wystarczającą ilość towaru, zależy nasza przyszłość.",
            "Asia pytała, czy napijecie się kawy czy herbaty.",
            "Nie wiedział, czy może poczęstować się cukierkami, czy nie."
        ]

        self.assertSentences(sentences)
