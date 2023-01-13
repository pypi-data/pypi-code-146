# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import hashlib
import shutil

import pybpodgui_api
from sca.formats import json

from pybpodgui_api.models.project.project_base import ProjectBase

logger = logging.getLogger(__name__)


class ProjectIO(ProjectBase):

    def __init__(self):
        super(ProjectIO, self).__init__()

        self.data_hash = None
        self.data = None

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def load(self, project_path):
        """
        Load project from a folder.

        :ivar str project_path: Full path of the project to load.
        """
        self.name = os.path.basename(project_path)
        self.path = project_path

        with open(os.path.join(self.path, self.name+'.json'), 'r') as stream:
            self.data = data = json.load(stream)

        self.uuid4 = data.uuid4 if data.uuid4 else self.uuid4

        logger.debug('=== LOAD USERS ===')
        userspath = os.path.join(self.path, 'users')
        if os.path.exists(userspath):
            for name in os.listdir(userspath):
                if os.path.isfile(os.path.join(userspath, name)):
                    continue
                user = self.create_user()
                user.load(os.path.join(userspath, name))

        logger.debug("==== LOAD TASKS ====")

        # load tasks
        taskspath = os.path.join(self.path, 'tasks')
        if os.path.exists(taskspath):
            for name in os.listdir(taskspath):
                if os.path.isfile(os.path.join(taskspath, name)):
                    continue
                task = self.create_task()
                task.load(os.path.join(taskspath, name))

        logger.debug("==== LOAD BOARDS ====")

        # load boards
        boardspath = os.path.join(self.path, 'boards')
        if os.path.exists(boardspath):
            for name in os.listdir(boardspath):
                if os.path.isfile(os.path.join(boardspath, name)):
                    continue
                board = self.create_board()
                board.load(os.path.join(boardspath, name))

        logger.debug("==== LOAD SUBJECTS ====")

        # load subjects
        subjectspath = os.path.join(self.path, 'subjects')
        if os.path.exists(subjectspath):
            for name in os.listdir(subjectspath):
                if os.path.isfile(os.path.join(subjectspath, name)):
                    continue
                subject = self.create_subject()
                subject.load(os.path.join(subjectspath, name))

        logger.debug("==== LOAD EXPERIMENTS ====")

        # load experiments
        experimentspath = os.path.join(self.path, 'experiments')
        if os.path.exists(experimentspath):
            for name in os.listdir(experimentspath):
                if os.path.isfile(os.path.join(experimentspath, name)):
                    continue
                experiment = self.create_experiment()
                experiment.load(os.path.join(experimentspath, name))

        logger.debug("==== POSTLOAD SUBJECTS ====")
        for subject in self.subjects:
            subject.post_load()

        self.data_hash = self.__generate_project_hash()

        logger.debug("==== LOAD FINNISHED ====")

    def save(self, project_path):
        """
        Save project data on file
        :param str project_path: path to project
        :return: project data saved on settings file
        """

        if project_path is not None:
            self.path = project_path

        logger.debug("saving project path: %s",  project_path)
        logger.debug("current project name: %s", self.name)
        logger.debug("current project path: %s", self.path)

        ########### SAVE THE USERS ############
        userspath = os.path.join(self.path, 'users')
        if not os.path.exists(userspath):
            os.makedirs(userspath)
        for user in self.users:
            user.save()
        self.remove_non_existing_repositories(userspath, [user.name for user in self.users])

        ########### SAVE THE TASKS ############
        taskspath = os.path.join(self.path, 'tasks')
        if not os.path.exists(taskspath):
            os.makedirs(taskspath)
        for task in self.tasks:
            task.save()
        self.remove_non_existing_repositories(taskspath, [task.name for task in self.tasks])

        ########### SAVE THE BOARDS ###########
        boardspath = os.path.join(self.path, 'boards')
        if not os.path.exists(boardspath):
            os.makedirs(boardspath)
        for board in self.boards:
            board.save()
        self.remove_non_existing_repositories(boardspath, [board.name for board in self.boards])

        ########### SAVE THE SUBJECTS ###############
        subjectspath = os.path.join(self.path, 'subjects')
        if not os.path.exists(subjectspath):
            os.makedirs(subjectspath)
        for subject in self.subjects:
            subject.save()
        self.remove_non_existing_repositories(subjectspath, [subject.name for subject in self.subjects])

        ########### SAVE THE EXPERIMENTS ############
        experimentspath = os.path.join(self.path, 'experiments')
        if not os.path.exists(experimentspath):
            os.makedirs(experimentspath)
        for experiment in self.experiments:
            experiment.save()
        self.remove_non_existing_repositories(experimentspath, [experiment.name for experiment in self.experiments])

        ########### SAVE THE PROJECT ############

        if self.data:
            data = self.data
        else:
            data = json.scadict(
                uuid4_id=self.uuid4,
                software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                def_url='http://pybpod.readthedocs.org',
                def_text='This file contains information about a PyBpod project.'
            )
        data['name'] = self.name

        name = os.path.basename(self.path)
        config_path = os.path.join(self.path, name+'.json')
        with open(config_path, 'w') as fstream:
            json.dump(data, fstream)

        self.data_hash = self.__generate_project_hash()

    def remove_non_existing_repositories(self, path, names):
        try:
            nodes = os.listdir(path)
        except:
            nodes = []

        for nodename in nodes:
            if nodename not in names:
                nodepath = os.path.join(path, nodename)
                if not os.path.isfile(nodepath):
                    shutil.rmtree(nodepath)

    def is_saved(self):
        """
        Verifies if project has changes by doing a recursive checksum on all entities

        :rtype: bool
        """
        if not self.path:
            return False

        current_hash = self.__generate_project_hash()

        if self.data_hash != current_hash:
            logger.warning("Different project data hashes:\n%s\n%s", self.data_hash, current_hash)
            return False

        return True

    def collect_data(self, data):
        """
        Collect the data of the project. This function is used to calculate the checksum of the project and verify if it was updated.

        :rtype: dict
        """
        data.update({'name': self.name})
        data.update({'experiments': []})
        data.update({'boards': []})
        data.update({'users': []})
        data.update({'subjects': []})
        data.update({'tasks': []})

        for board in self.boards:
            data['boards'].append(board.collect_data({}))

        for experiment in self.experiments:
            data['experiments'].append(experiment.collect_data({}))

        for task in self.tasks:
            data['tasks'].append(task.collect_data({}))

        for user in self.users:
            data['users'].append(user.collect_data({}))

        for subject in self.subjects:
            data['subjects'].append(subject.collect_data({}))

        logger.debug("Project data: %s", data)

        return data

    def __save_project_hash(self):
        self.data_hash = self.__generate_project_hash()
        logger.debug("Project data hash: %s", self.data_hash)

    def __generate_project_hash(self):
        return hashlib.sha256(
            json.dumps(self.collect_data(data={}), sort_keys=True).encode('utf-8')).hexdigest()
