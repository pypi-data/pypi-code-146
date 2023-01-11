from unittest import TestCase
from pyPhases.Data import Data
from pyPhases.Project import Project
from pyPhases.util.pdict import pdict


class TestData(TestCase):

    def defaultTestData(self):
        testProject = Project("myProject")
        testProject.config = {"a": "foo", "b": "bar", "c": "c"}

        Data("myData", testProject, ["a"])
        Data("myData2",testProject, ["a", "b"])

        return Data.create("testData", testProject, ["c", "myData"])


    def test_toString(self):
        testData = Data("myData", Project())
        self.assertEqual(str(testData), "myData")

    def test_Init(self):
        testData = Data("test", Project(),  ["a", "b"])
        self.assertEqual(testData.name, "test")
        self.assertEqual(testData.dataTags, ["a", "b"])
        self.assertEqual(testData.project.dataNames["test"], testData)

    def test_create(self):
        testProject = Project("myProject")
        testData = Data.create("test", testProject, ["a", "b"])
        self.assertEqual(testData.name, "test")
        self.assertEqual(testData.dataTags, ["a", "b"])
        self.assertEqual(testData.project.dataNames["test"], testData)

    def test_hasTobeHashed(self):
        testData = Data("test", Project(),  ["a", "b"])
        self.assertEqual(testData.hasTobeHashed(["a"]), True)
        self.assertEqual(testData.hasTobeHashed({"foo": "bar"}), True)
        self.assertEqual(testData.hasTobeHashed(pdict()), True)
        self.assertEqual(testData.hasTobeHashed(pdict({"foo": "bar"})), True)

        self.assertEqual(testData.hasTobeHashed("foo"), False)
        self.assertEqual(testData.hasTobeHashed(5), False)
        self.assertEqual(testData.hasTobeHashed(None), False)

    def test_flattenLongString(self):
        testData = Data("test", Project(),  ["a", "b"])
        self.assertEqual(testData.flattenLongString("foo"), "0beec7b5")
        self.assertEqual(testData.flattenLongString("foo bar"), "3773dea6")
        self.assertEqual(testData.flattenLongString("foo bar baz"), "c7567e8b")
        self.assertEqual(testData.flattenLongString("foo bar baz "), "f72f7597")

        self.assertEqual(testData.flattenLongString(str(["foo"])), "68681ff7")
        self.assertEqual(testData.flattenLongString(str({"foo": "bar"})), "8f3536a8")

    def test_flatten(self):
        testData = Data("test", Project(),  ["a", "b"])
        self.assertEqual(testData.flatten("foo"), "foo")
        self.assertEqual(testData.flatten(5), "5")
        self.assertEqual(testData.flatten(None), None)
        self.assertEqual(testData.flatten(["foo"]), "68681ff7")
        self.assertEqual(testData.flatten({"foo": "bar"}), "8f3536a8")


        self.assertEqual(testData.flatten("foo-bar"), "foo-bar")
        # remove spaces and brackets
        self.assertEqual(testData.flatten("foo (-)  bar"), "foo-bar")

        # replace special chars
        self.assertEqual(testData.flatten("€"), "-")
        self.assertEqual(testData.flatten("\\"), "-")
        self.assertEqual(testData.flatten("ß"), "-")
        self.assertEqual(testData.flatten("$"), "-")
        self.assertEqual(testData.flatten("&"), "-")
        self.assertEqual(testData.flatten("\""), "-")

    def test_flattenConfigValues(self):
        self.assertEqual(Data.flattenConfigValues("foo bar"), "foobar")

    def test_getTagValueFromConfig(self):
        testProject = Project("myProject")
        testProject.config = {"a": "foo", "b": "bar", "c": "c"}
        testData = Data.create("testData", testProject, ["a", "b"])
        self.assertEqual(testData._getTagValue("a"), "foo")
        self.assertEqual(testData._getTagValue("b"), "bar")
        self.assertEqual(testData._getTagValue("c"), "c")

    def test_getTagValueFromData(self):
        testProject = Project("myProject")
        Data("myData", testProject, ["a"])
        Data("myData2", testProject, ["a", "b"])
        testProject.config = {"a": "foo", "b": "bar", "c": "c"}
        testData = Data.create("testData", testProject, ["myData"])
        self.assertEqual(testData._getTagValue("myData"), "foo")
        self.assertEqual(testData._getTagValue("myData2"), "foo-bar")

    def test_getDependencyDictOnConfig(self):
        testProject = Project("myProject")
        testProject.config = {"a": "foo", "b": "bar", "c": "c"}

        testData = Data.create("testData", testProject, ["a", "b"])
        self.assertEqual(testData.getDependencyDict(["a"]), {'a': 'foo'})
        self.assertEqual(testData.getDependencyDict(["b"]), {'b': 'bar'})
        self.assertEqual(testData.getDependencyDict(["a", "b"]), {'a': 'foo', 'b': 'bar'})
        self.assertEqual(testData.getDependencyDict(), {'a': 'foo', 'b': 'bar'})

    def test_getDependencyDictOnData(self):
        testProject = Project("myProject")
        Data("myData", testProject, ["a"])
        Data("myData2", testProject, ["a", "b"])
        testProject.config = {"a": "foo", "b": "bar", "c": "c"}

        testData = Data.create("testData", testProject, ["c", "myData"])
        self.assertEqual(testData.getDependencyDict(["a"]), {'a': 'foo'})
        self.assertEqual(testData.getDependencyDict(["b"]), {'b': 'bar'})
        self.assertEqual(testData.getDependencyDict(["a", "b"]), {'a': 'foo', 'b': 'bar'})
        self.assertEqual(testData.getDependencyDict(["myData"]), {'a': 'foo'})
        self.assertEqual(testData.getDependencyDict(["myData2"]), {'a': 'foo', 'b': 'bar'})

        self.assertEqual(testData.getDependencyDict(), {'c': 'c', 'a': 'foo'})

    def test_parseDatanames(self):
        testData = self.defaultTestData()
        self.assertEqual(testData.parseDatanames(["c", "myData"]), 'c-foo')

    def test_getTagString(self):
        testData = self.defaultTestData()
        self.assertEqual(testData.getTagString(), 'c-foo')

    def test_str(self):
        testData = self.defaultTestData()
        self.assertEqual(str(testData), 'testDatac-foo')

    def test_getDataId(self):
        testData = self.defaultTestData()
        self.assertEqual(testData.getDataId(), 'testDatac-foo--current')
