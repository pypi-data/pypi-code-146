from abc import abstractmethod

class ExporterTestHelper():

    @abstractmethod
    def getExporter(self):
        pass

    @abstractmethod
    def getSupportedObjects(self):
        pass

    def testCheckSupportedTypes(self):
        exporter = self.getExporter()

        for obj in self.getSupportedObjects():
            self.assertEqual(exporter.checkType(type(obj)), True)


    def testExportImport(self):

        exporter = self.getExporter()

        for index, obj in enumerate(self.getSupportedObjects()):
            dataId = "test" + str(index)
            self.assertFalse(exporter.exists(dataId))
            exporter.write(dataId, obj)
            self.assertTrue(exporter.exists(dataId))

            importedModel = exporter.read(dataId)

            self.assertIsInstance(importedModel, type(obj))
            self.assertEqual(importedModel, obj)




