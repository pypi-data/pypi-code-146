from __future__ import annotations

experiment: Experiment = None


def set_experiment(experiment_: Experiment) -> None:
    global experiment
    experiment = experiment_


def get_experiment() -> Experiment:
    global experiment
    return experiment


class Experiment:
    def __init__(self, exp_name, team_name):
        self.__exp_name = exp_name
        self.__team_name = team_name

    @property
    def exp_name(self):
        return self.__exp_name

    @property
    def team_name(self):
        return self.__team_name
