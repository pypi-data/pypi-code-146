import unittest as ut
from regex_dict import RegexDict


class TestRegexDict(ut.TestCase):
    key1, key2, key3, key4 = "value1", ".*value2", "value3.*", "value4"
    value1, value2, value3, value4 = 1, 2, 3, 4

    test_dict = {key1: value1, key2: value2, key3: value3, key4: value4}
    test_regex = RegexDict(test_dict)

    def test_value1(self):
        self.assertEqual(self.test_regex[self.key1], self.test_dict[self.key1])
        self.assertNotEqual(
            self.test_regex[f"{self.key1}sdsdfs"], self.test_dict[self.key1])

    def test_value2(self):
        self.assertEqual(
            self.test_regex[f"sdfsdfs{self.key2}"], self.test_dict[self.key2])
        self.assertNotEqual(
            self.test_regex[f"sdfsdfs{self.key2}asdas"], self.test_dict[self.key2])

    def test_value3(self):
        self.assertEqual(
            self.test_regex[f"{self.key3}safsdfsdf"], self.test_dict[self.key3])
        self.assertNotEqual(
            self.test_regex[f"as{self.key3}safsdfsdf"], self.test_dict[self.key3])

    def test_value4(self):
        self.assertEqual(self.test_regex[self.key4], self.test_dict[self.key4])
        self.assertNotEqual(
            self.test_regex[f"v{self.key4}"], self.test_dict[self.key4])

    def test_len(self):
        self.assertEqual(len(self.test_regex), len(self.test_dict))

    def test_get(self):
        self.assertEqual(self.test_regex.get(self.key1),
                         self.test_dict.get(self.key1))
        self.assertEqual(self.test_regex.get("test", "test"),
                         self.test_dict.get("test", "test"))


if __name__ == "__main__":
    ut.main(verbosity=2)
