from unittest import TestCase
from pyPhases.Project import  Project
from pyPhases.PluginAdapter import PluginAdapter
from pyPhases.util.pdict import pdict


class TestPluginAdapter(TestCase):

    def setUp(self):
        self.options = {'option1': 'value1', 'option2': 'value2'}
        self.project = Project()
        self.project.config = pdict({'key': 'value'})
        self.plugin = PluginAdapter(self.project, self.options)

    def test_init(self):
        self.assertEqual(self.plugin.project, self.project)
        self.assertEqual(self.plugin.options, self.options)

    def test_getConfig(self):
        self.assertEqual(self.plugin.getConfig('key'), "value")

    def test_initPlugin(self):
        new_project = Project()
        self.plugin.initPlugin(new_project)
        self.assertEqual(self.plugin.project, new_project)
