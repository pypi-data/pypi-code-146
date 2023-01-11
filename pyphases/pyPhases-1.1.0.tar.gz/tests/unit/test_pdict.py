from unittest import TestCase
from pyPhases.util.pdict import pdict


class ObjectExporterTest(TestCase):

    def test_wrap(self):
        a = pdict({"a": 5, "b": 2})
        self.assertEqual(a, {"a": 5, "b": 2})

    def test_nested(self):
        a = pdict({"a": {"b": 2}})
        self.assertEqual(a, {"a": {"b": 2}})

    def test_array_accessList(self):
        a = pdict({"a": {"b": 2}})
        self.assertEqual(a["a"], {"b": 2})
        self.assertEqual(a[["a", "b"]], 2)

    def test_array_accessArgs(self):
        a = pdict({"a": {"b": 2}})
        self.assertEqual(a["a"], {"b": 2})
        self.assertEqual(a["a", "b"], 2)

    def test_storeList(self):
        a = pdict({"a": {"b": 2}})
        self.assertEqual(a["a"], {"b": 2})
        a[["a", "b"]] = 5
        self.assertEqual(a["a"], {"b": 5})

    def test_storeArgs(self):
        a = pdict({"a": {"b": 2}})
        self.assertEqual(a["a"], {"b": 2})
        a["a", "b"] = 5
        self.assertEqual(a["a"], {"b": 5})

    def test_defaults(self):
        a = pdict({"a": 5, "b": 2})
        a.setdefaults({"b": 5,"c": 3})

        self.assertEqual(a, {"a": 5, "b": 2, "c": 3})


    def test_updateAdd(self):
        a = pdict({"a": 5, "b": 2})
        u = {"c": 3}

        a.update(u)

        self.assertEqual(a, {"a": 5, "b": 2, "c": 3})

    def test_updateChange(self):
        a = pdict({"a": 5, "b": 2})
        u = {"a": 3}

        a.update(u)

        self.assertEqual(a, {"a": 3, "b": 2})

    def test_updateNestedChange(self):
        a = pdict({"a": 5, "b": 2, "c": {"d": 5, "e": 6}})
        u = {"a": 3, "c": {"d": 7}}

        a.update(u)

        self.assertEqual(a, {"a": 3, "b": 2, "c": {"d": 7, "e": 6}})


    def test_NoneExisting(self):
        a = pdict({"a": 5, "c": {"d": 5, "e": 6}})
        self.assertRaises(KeyError, lambda: a["c", "f"])


    def test_NoneExistingCreate(self):
        a = pdict({"a": 5})
        a.__getitem__(["b"], create=True)
        self.assertIn("b", a)

    def test_UpdateEmpty(self):
        a = pdict({})
        a.update({"a": {"b": 5}})
        self.assertIn("a", a)
        self.assertEqual(a["a"], {"b": 5})

    def test_UpdeateNested(self):
        a = pdict({"loader": {"a": 5}})
        a.update({"loader": {"b": 5}})

        # a.update({"b": {"c": 5}})
        self.assertIn("loader", a)
        self.assertIn("a", a["loader"])
        self.assertIn("b", a["loader"])
        self.assertEqual( a["loader"]["a"], 5)
        self.assertEqual( a["loader"]["b"], 5)


    def test_UpdateNestedTwoDim(self):
        a = pdict({"config": {"loader": {"a": 5}}})
        a.update({"config": {"loader": {"b": 5}}})

        self.assertIn("config", a)
        self.assertIn("loader", a["config"])
        self.assertIn("a", a["config"]["loader"])
        self.assertIn("b", a["config"]["loader"])
        self.assertEqual( a["config"]["loader"]["a"], 5)
        self.assertEqual( a["config"]["loader"]["b"], 5)
