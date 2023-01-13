# !/usr/bin/python3
# -*- coding: utf-8 -*-

""" pycontrol.api.models.project

"""
import logging
import uuid
import os
import shutil
from pybpodgui_api.models.experiment import Experiment
from pybpodgui_api.models.board import Board
from pybpodgui_api.models.task import Task
from pybpodgui_api.models.subject import Subject
from pybpodgui_api.models.user import User
from pybpodgui_api.utils.copy_directory import copy_directory

logger = logging.getLogger(__name__)


class ProjectBase(object):
    """
    A project is a collection of experiments and an hardware configuration
    """

    def __init__(self):
        self.uuid4 = uuid.uuid4()
        self.name = ''
        self._experiments = []
        self._tasks = []
        self._boards = []
        self._subjects = []
        self._users = []
        self._path = None

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def subjects(self):
        """
        Get the list of subjects in the project

        :rtype: list(Subject)
        """
        return self._subjects

    @property
    def experiments(self):
        """
        Get the list of experiments in the project

        :rtype: list(Experiment)
        """
        return self._experiments

    @property
    def boards(self):
        """
        Get the list of boards in the project

        :rtype: list(Board)
        """
        return self._boards

    @property
    def tasks(self):
        """
        Get the list of tasks in the project

        :rtype: list(Task)
        """
        return self._tasks

    @property
    def path(self):
        """
        Get and set the project path

        :rtype: str
        """
        return self._path

    @property
    def users(self):
        """
        Get the list of users in the project

        :rtype: list(User)
        """
        return self._users

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def name(self):
        """
        Get and set the project name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def import_task(self, filepath, importdir=False):
        if self.path is None:
            raise Exception('The project has to be saved first')

        filename, file_extension = os.path.splitext(os.path.basename(filepath))

        # check if there are any existing task with the same name
        if self.find_task(filename) is not None:
            raise Exception(
                """There is already a task named [{}].The import was aborted""".format(filename),
            )
        ###########################################################

        # create the task, folder, and copy the files
        task = self.create_task()
        task.name = filename
        task.make_path()
        new_filepath = os.path.join(task.path, task.name+'.py')
        task.filepath = new_filepath

        if importdir:
            copy_directory(os.path.dirname(filepath), task.path + "/")
        else:
            shutil.copy(filepath, new_filepath)
        ###########################################################

        return task

    def __add__(self, obj):
        if isinstance(obj, Experiment):
            self._experiments.append(obj)

        if isinstance(obj, Board):
            self._boards.append(obj)

        if isinstance(obj, Task):
            self._tasks.append(obj)

        if isinstance(obj, Subject):
            self._subjects.append(obj)

        if isinstance(obj, User):
            self._users.append(obj)

        return self

    def __sub__(self, obj):
        if isinstance(obj, Experiment):
            self._experiments.remove(obj)

        if isinstance(obj, Board):
            self._boards.remove(obj)

        if isinstance(obj, Task):
            self._tasks.remove(obj)

        if isinstance(obj, Subject):
            self._subjects.remove(obj)

        if isinstance(obj, User):
            self._users.remove(obj)

        return self

    def find_board(self, name):
        """
        Find a board by the name

        :ivar str name: Name of the board to find.
        :rtype: Board
        """
        for board in self.boards:
            if board.name == name:
                return board
        return None

    def find_task(self, name):
        """
        Find a task by the name

        :ivar str name: Name of the task to find.
        :rtype: Task
        """
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def find_subject(self, name):
        """
        Find a subject by the name

        :ivar str name: Name of the subject to find.
        :rtype: Subject
        """
        for subject in self.subjects:
            if subject.name == name:
                return subject
        return None

    def find_setup_by_id(self, uuid4):
        """
        Find a setup by the id

        :ivar str uuid4: UUID4 of the setup to find.
        :rtype: Setup
        """
        for experiment in self.experiments:
            for setup in experiment.setups:
                if setup.uuid4 == uuid4:
                    return setup
        return None

    def find_subject_by_id(self, uuid4):
        """
        Find a subject by the name

        :ivar str name: Name of the subject to find.
        :rtype: Subject
        """
        for subject in self.subjects:
            if subject.uuid4 == uuid4:
                return subject
        return None

    def find_session(self, uuid4):
        for experiment in self.experiments:
            for setup in experiment.setups:
                for session in setup.sessions:
                    if session.uuid4 == uuid4:
                        return session
        return None

    def find_user(self, username):
        for user in self.users:
            if user.name == username:
                return user
        return None

    def create_experiment(self):
        """
        Add an experiment to the project, and return it.

        :rtype: Experiment
        """
        return Experiment(self)

    def create_board(self):
        """
        Add an board to the project, and return it.

        :rtype: Board
        """
        return Board(self)

    def create_task(self):
        """
        Add an task to the project, and return it.

        :rtype: Task
        """
        return Task(self)

    def create_subject(self):
        """
        Add an subject to the project, and return it.

        :rtype: Subject
        """
        return Subject(self)

    def create_user(self):
        """
        Add a user bject to the project, and return it.

        :rtype: User
        """
        return User(self)
