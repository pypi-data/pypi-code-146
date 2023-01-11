import shutil
from pathlib import Path
from unittest import TestCase

from pyPhases.Data import DataNotFound
from pyPhases.exporter.PickleExporter import PickleExporter
from tests.util.ExporterTestHelper import ExporterTestHelper


class TestPickleExporter(ExporterTestHelper, TestCase):

    @classmethod
    def setUpClass(cls):
        path = "./tests/data"
        shutil.rmtree(path, ignore_errors=True, onerror=None)
        Path(path).mkdir(parents=True, exist_ok=True)

    def getExporter(self):
        return PickleExporter({
            "basePath": "./tests/data"
        })

    def getSupportedObjects(self):
        return [
            5,
            "test",
            5.5,
            [2, "test", 5.5],
            {"foo": "bar"},
            (2, "test", 5.5)
        ]

    def testCheckType(self):
        exporter = PickleExporter()

        class MyClass():
            pass

        self.assertEqual(exporter.checkType(MyClass), False)
        PickleExporter.supportedTypes = [MyClass]
        self.assertEqual(exporter.checkType(MyClass), True)

    def test_dataNotFound(self):
        self.assertRaises(DataNotFound, self.getExporter().read, "unknown")




