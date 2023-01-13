# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import shutil

from pybpodgui_api.models.experiment.experiment_base import ExperimentBase

logger = logging.getLogger(__name__)


class ExperimentIO(ExperimentBase):
    """
    Save and Load actions for Experiment
    """
    def __init__(self, project):
        super(ExperimentIO, self).__init__(project)

        # initial name. Used to track if the name was updated
        self.initial_name = None

    ##########################################################################
    #       FUNCTIONS                                                        #
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        # data.update({'task': self.task.name if self.task else None})
        data.update({'setups': []})

        for setup in self.setups:
            data['setups'].append(setup.collect_data({}))

        return data

    def save(self):
        """
        Save experiment data on filesystem.

        :ivar dict parent_path: Project path.
        :return: Dictionary containing the experiment info to save.
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping experiment without name")
        else:
            if self.initial_name is not None:
                initial_path = os.path.join(self.project.path, 'experiments', self.initial_name)

                if initial_path != self.path:
                    shutil.move(initial_path, self.path)
                    # current_filepath = os.path.join(self.path, self.initial_name+'.json')
                    # future_filepath  = os.path.join(self.path, self.name+'.json')
                    # shutil.move( current_filepath, future_filepath )

            if not os.path.exists(self.path):
                os.makedirs(self.path)

            self.initial_name = self.name

            # save setups
            for setup in self.setups:
                setup.save()

            self.project.remove_non_existing_repositories(
                os.path.join(self.path, 'setups'),
                [setup.name for setup in self.setups]
            )

    def load(self, path):
        """
        Load experiment data from filesystem

        :ivar str experiment_path: Path of the experiment
        :ivar dict data: data object that contains all experiment info
        :return: Dictionary with loaded experiment info.
        """
        self.name = os.path.basename(path)
        # with open( os.path.join(self.path, self.name+'.json'), 'r' ) as stream:
        #     data = json.load(stream)
        # self.uuid4 = data.uuid4 if data.uuid4 else self.uuid4

        self.initial_name = self.name

        setupspath = os.path.join(self.path, 'setups')
        if os.path.exists(setupspath):
            for name in os.listdir(setupspath):
                if os.path.isfile(os.path.join(setupspath, name)):
                    continue
                setup = self.create_setup()
                setup.load(os.path.join(setupspath, name))

    def __clean_setups_path(self, experiment_path):
        # remove from the setups directory the unused setup files
        setups_paths = [setup.path for setup in self.setups]
        for path in self.__list_all_setups_in_folder(experiment_path):
            if path not in setups_paths:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)

    def __generate_experiments_path(self, project_path):
        return os.path.join(project_path, 'experiments')

    def __generate_experiment_path(self, experiments_path):
        return os.path.join(experiments_path, self.name)

    def __list_all_setups_in_folder(self, experiment_path):
        search_4_dirs_path = os.path.join(experiment_path, 'setups')
        if not os.path.exists(search_4_dirs_path):
            return []
        return sorted([os.path.join(search_4_dirs_path, d) for d in os.listdir(search_4_dirs_path) if
                       os.path.isdir(os.path.join(search_4_dirs_path, d))])
