from looqbox.render.looqbox.base_looqbox_render import BrowserRender
from looqbox.objects.tests import LooqObject
from looqbox.objects.tests import ObjTable
import pandas as pd
import numpy as np
import unittest
import json


class TestObjectTable(unittest.TestCase):
    """
    Test looq_table file
    """

    def setUp(self) -> None:
        data = np.array([
            [100, 120, 98, 73, 20, 157, 124, 0, 9999, 100],
            [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        ]).T

        df = pd.DataFrame(data, columns=['Venda', 'Meta'])
        self.looq_object_table = ObjTable(df)

        self.visitor = BrowserRender()
        self.visitor.remove_nones = False

    def test_instance(self):
        looq_object_table = self.looq_object_table

        self.assertIsInstance(looq_object_table, LooqObject)

    def test_header_json_structure(self):
        looq_object_table = self.looq_object_table

        # Testing JSON header keys
        json_table_keys = list(looq_object_table.to_json_structure(self.visitor)["header"].keys())
        self.assertTrue("content" in json_table_keys, msg="content not found in header JSON structure test")
        self.assertTrue("visible" in json_table_keys, msg="visible not found in header JSON structure test")
        self.assertTrue("group" in json_table_keys, msg="group not found in header JSON structure test")

    def test_body_json_structure(self):
        looq_object_table = self.looq_object_table

        # Testing JSON body keys
        json_table_keys = list(looq_object_table.to_json_structure(self.visitor)["body"].keys())
        self.assertTrue("content" in json_table_keys, msg="content not found in body JSON structure test")
        self.assertTrue("_lq_column_config" in json_table_keys,
                        msg="_lq_column_config not found in body JSON structure test")

    def test_footer_json_structure(self):
        looq_object_table = self.looq_object_table

        # Testing JSON footer keys
        json_table_keys = list(looq_object_table.to_json_structure(self.visitor)["footer"].keys())
        self.assertTrue("content" in json_table_keys, msg="content not found in footer JSON structure test")
        self.assertTrue("subtotal" in json_table_keys, msg="subtotal not found in footer JSON structure test")

    def test_subtotal_structure(self):
        looq_object_table = self.looq_object_table
        looq_object_table.subtotal = [{"text": "Subtotal text", "link": "Subtotal link"}]
        json_table = looq_object_table.to_json_structure(self.visitor)

        # Testing JSON footer keys
        self.assertTrue(isinstance(json_table["footer"]["subtotal"], list))

    def test_collapse_structure(self) -> None:
        data = np.array([
            [100, 120, 98, 73, 20, 157, 124, 0, 9999, 100],
            [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        ]).T

        df = pd.DataFrame(data, columns=['Venda', 'Meta'])
        table = ObjTable(df)
        table.collapseable = True
        table.row_hierarchy = [1, 1, 1, 2, 3, 4, 2, 2, 1, 1]
        collapsed_row = table.to_json_structure(self.visitor)["body"]["content"][2]

        # Since the key value is generated randomly it was removed for testing purposes
        collapsed_row.pop("key")
        tree_data1 = collapsed_row["tree_data"]
        tree_data2 = tree_data1[0]["tree_data"]
        tree_data3 = tree_data2[0]["tree_data"]

        tree_data1[0].pop("key")
        tree_data2[0].pop("key")
        tree_data3[0].pop("key")

        tree_data2[0]["tree_data"] = tree_data3
        tree_data1[0]["tree_data"] = tree_data2
        collapsed_row["tree_data"] = tree_data1

        collapsed_model = {
            "Venda": 98,
            "Meta": 100,
            "tree_data": [
                {
                    "Venda": 73,
                    "Meta": 100,
                    "tree_data": [
                        {
                            "Venda": 20,
                            "Meta": 100,
                            "tree_data": [
                                {
                                    "Venda": 157,
                                    "Meta": 100,
                                    "tree_data": None
                                }
                            ]
                        }
                    ]
                },
                {
                    "Venda": 124,
                    "Meta": 100
                },
                {
                    "Venda": 0,
                    "Meta": 100
                }
            ],
            "_lq_cell_config": {
                "Meta": {
                    "class": None,
                    "drill": None,
                    "drillText": None,
                    "filter": None,
                    "format": None,
                    "style": None,
                    "tooltip": None
                },
                "Venda": {
                    "class": None,
                    "drill": None,
                    "drillText": None,
                    "filter": None,
                    "format": None,
                    "style": None,
                    "tooltip": None
                }
            },
            "_lq_row_config": {
                "class": None,
                "drill": None,
                "format": None,
                "style": None,
                "tooltip": None
            }
        }

        self.assertEqual(collapsed_row, collapsed_model, msg="collapse does not match json structure properly")


if __name__ == '__main__':
    unittest.main()
