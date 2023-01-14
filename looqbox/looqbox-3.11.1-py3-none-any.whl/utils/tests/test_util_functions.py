from looqbox.utils.i18n.internationalization_manager import I18nManager
from looqbox.objects.visual.looq_table import ObjTable
from looqbox.utils.utils import *
import pandas as pd
import unittest
import datetime


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        self.raw_number = 1.23544
        self.raw_percent = 0.641238
        self.currency_symbol = "$"
        self.raw_date = "2022-10-25"
        self.raw_datetime = "2022-10-25 05:02:00"

    #
    # def test_title_with_date(self):
    #     """
    #     Test title_with_date function
    #     """
    #
    #     date_1 = ['2019-01-01', '2019-01-01']
    #     date_2 = ['2018-12-10', '2018-12-16']
    #     date_3 = ['2018-01-01', '2018-01-31']
    #     date_4 = ['2018-01-01', '2018-12-31']
    #
    #     self.assertEqual('Período  dia  01/01/2019',
    #                      title_with_date('Período', date_1, "pt-br"))
    #
    #     self.assertEqual('Período  de  10/12/2018 a 16/12/2018',
    #                      title_with_date('Período', date_2, "pt-br"))
    #
    #     self.assertEqual('Período  de  01/01/2018 a 31/01/2018',
    #                      title_with_date('Período', date_3, "pt-br"))
    #
    #     self.assertEqual('Período  de  01/01/2018 a 31/12/2018',
    #                      title_with_date('Período', date_4, "pt-br"))

    def test_format_cnpj(self):
        """
        Test format_cnpj function
        """

        self.assertEqual('00.100.000/0100-01',
                         format_cnpj('0100000010001'))

    def test_format_cpf(self):
        """
        Test format_cpf function
        """

        self.assertEqual('001.001.001-01',
                         format_cpf('00100100101'))

    def test_number_format(self):

        model_value_2_places = "1,24"
        test_value_2_places = format(self.raw_number, "number:2")

        self.assertEqual(test_value_2_places, model_value_2_places)

        model_value_5_places = "1,23544"
        test_value_5_places = format(self.raw_number, "number:5")

        self.assertEqual(test_value_5_places, model_value_5_places)

    def test_percent_format(self):

        model_value_2_places = "64,12%"
        test_value_2_places = format(self.raw_percent, "percent:2")

        self.assertEqual(test_value_2_places, model_value_2_places)

        model_value_4_places = "64,1238%"
        test_value_4_places = format(self.raw_percent, "percent:4")
        
        self.assertEqual(test_value_4_places, model_value_4_places)

    def test_currency_format(self):

        model_value = "$1,24"
        test_value = format(self.raw_number, "currency:"+self.currency_symbol)

        self.assertEqual(test_value, model_value)

    def test_date_format(self):

        model_date = "25/10/2022"
        test_date = format(self.raw_date, "date")

        self.assertEqual(test_date, model_date)

        test_date_uppercase = format(self.raw_date, "Date")

        self.assertEqual(test_date_uppercase, model_date)

    def test_datetime_format(self):

        model_datetime = "25/10/2022 05:02:00"
        test_datetime = format(self.raw_datetime, "datetime")

        self.assertEqual(model_datetime, test_datetime)

        test_datetime_uppercase = format(self.raw_datetime, "Datetime")

        self.assertEqual(model_datetime, test_datetime_uppercase)

    def test_drill_if(self):
        """
        Test drill_if function
        """

        table = ObjTable()
        stores = ['Sao Paulo', 'LooqCity', 'Chicago', 'Roma', 'Tokio',
                  'Belem', 'Berlin', 'New York', 'Franca', 'London']
        codes = range(0, 10)

        table.data = pd.DataFrame({"Codigo": list(codes), "Loja": stores,
                                   "Venda": [200, 580, 965, 753, 134, 741, 156, 452, 764, 1000]},
                                  columns=["Codigo", "Loja", "Venda"])

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual([[{'text': 'Head', 'link': 'Teste da meta da loja Sao Paulo'},
                           {'text': 'Head', 'link': 'Teste da meta da loja LooqCity'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Chicago'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Roma'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Tokio'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Belem'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Berlin'},
                           {'text': 'Head', 'link': 'Teste da meta da loja New York'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Franca'},
                           {'text': 'Head', 'link': 'Teste da meta da loja London'}]],
                         drill_if(table.cell_link["Loja"], [None, 1]))

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual([[{'text': 'Head 2', 'link': 'Teste da meta da loja Sao Paulo'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja LooqCity'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Chicago'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Roma'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Tokio'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Belem'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Berlin'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja New York'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Franca'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja London'}]],
                         drill_if(table.cell_link["Loja"], [1, None]))

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual(None, drill_if(table.cell_link["Loja"], [1, 1]))

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual([[{'text': 'Head', 'link': 'Teste da meta da loja Sao Paulo'},
                           {'text': 'Head', 'link': 'Teste da meta da loja LooqCity'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Chicago'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Roma'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Tokio'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Belem'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Berlin'},
                           {'text': 'Head', 'link': 'Teste da meta da loja New York'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Franca'},
                           {'text': 'Head', 'link': 'Teste da meta da loja London'}],
                          [{'text': 'Head 2', 'link': 'Teste da meta da loja Sao Paulo'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja LooqCity'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Chicago'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Roma'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Tokio'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Belem'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Berlin'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja New York'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Franca'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja London'}]],
                         drill_if(table.cell_link["Loja"], [None, None]))

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual(None, drill_if(table.cell_link["Venda"], 1))

    def test_current_day(self):
        """
        Test current_day function
        """

        self.assertEqual(
            [datetime.datetime.now().strftime("%Y-%m-%d"),
             datetime.datetime.now().strftime("%Y-%m-%d")],
            current_day('date'))
        self.assertEqual(
            [datetime.datetime.now().strftime("%Y-%m-%d"),
             datetime.datetime.now().strftime("%Y-%m-%d")],
            current_day())
        self.assertEqual([datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")],
                         current_day('datetime'))
        self.assertEqual(
            [datetime.datetime.now().strftime("%Y-%m-%d"),
             datetime.datetime.now().strftime("%Y-%m-%d")],
            current_day('Date'))
        self.assertEqual([datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")],
                         current_day('DateTime'))
        self.assertEqual([datetime.datetime.now().strftime("%Y-%m-%d"),
                          datetime.datetime.now().strftime("%Y-%m-%d")],
                         current_day('kjhsdfj'))

    def test_partition(self):
        """
        Test current_day function
        """

        self.assertEqual([["foo", "foo"]], partition("foo"))
        self.assertEqual([["foo", 1]], partition(["foo", 1]))
        self.assertEqual([["foo", 5], [5, True]], partition(["foo", 5, True]))
        self.assertEqual([["foo", 5], [5, True], [True, "goo"]], partition(["foo", 5, True, "goo"]))
