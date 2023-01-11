from unittest import TestCase
from pyPhases import Project, Phase
from pyPhases.exporter.PickleExporter import PickleExporter


class PhaseTest(TestCase):

    def test_project(self):


        project = Project()
        project.registerExporter(PickleExporter())

        project.name = 'myTestProject'
        project.namespace = 'tud.ibmt'

        phase1 = Phase()


