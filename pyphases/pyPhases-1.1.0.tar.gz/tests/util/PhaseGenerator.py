from pyPhases.test.TestCase import TestCase
from pyPhases import Phase, Project


class TestPhase(Phase):
    def __init__(self, options={}) -> None:
        super().__init__(options)
        self.mainExecuted = 0

    def main(self):
        self.log("MAIN")
        self.project.registerData("data" + self.name, 5)
        self.mainExecuted += 1


class PhaseGenerator:
    @staticmethod
    def defaultConfig():
        return {"p1": 1, "p2": 2}

    @staticmethod
    def completeConfig():
        return {
            "p1": 1,
            "p2": 2,
            "p1c1": 1,
            "p1c2": 2,
            "p2c1": 1,
            "p2c2": 2,
            "p3c1": 1,
            "p3c2": 2,
            "p4c1": 1,
            "p4c2": 2,
        }

    @staticmethod
    def generatePhase(config={"opt1": 1, "opt2": 2}, dataName=""):
        phase = TestPhase()
        phase.config = config
        phase.exportData = ["data" + dataName]

        return phase

    @staticmethod
    def generateProject(name="testProject", config=None, withDefaultPhases=True) -> Project:
        project = Project()
        project.name = name
        project.config = config if config is not None else PhaseGenerator.defaultConfig()

        if withDefaultPhases:
            project.addPhase(PhaseGenerator.generatePhase(config={"p1c1": 1, "p1c2": 2}, dataName="phase1"), "phase1")
            project.addPhase(PhaseGenerator.generatePhase(config={"p2c1": 1, "p2c2": 2}, dataName="phase2"), "phase2")
            project.addPhase(PhaseGenerator.generatePhase(config={"p3c1": 1, "p3c2": 2}, dataName="phase3"), "phase3")
            project.addPhase(PhaseGenerator.generatePhase(config={"p4c1": 1, "p4c2": 2}, dataName="phase4"), "phase4")

        project.prepareAllPhases()
        return project


project = PhaseGenerator.generateProject()
TestCase.project = project
