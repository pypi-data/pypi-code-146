# !/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os


class TaskCommand(object):

    WHEN_PRE = 0
    WHEN_POST = 1

    def __init__(self, task=None):
        self.task = task
        self.task += self

        self.when = None

    def execute(self):
        pass


class ScriptCmd(TaskCommand):

    def __init__(self, task=None):
        super(ScriptCmd, self).__init__(task)
        self.script = ''

    def execute(self, **kwargs):
        global_dict = globals()
        global_dict.update(kwargs)
        script_path = os.path.join(self.task.path, self.script)

        environment = os.environ.copy()
        environment['PYTHONPATH'] = os.pathsep.join([os.path.abspath(self.task.path)])

        proc = subprocess.Popen(
            ['python', os.path.abspath(script_path)],
            cwd=self.task.path,
            env=environment
        )
        proc.wait()
        # exec(open(script_path).read(), global_dict)

    def __str__(self):
        return self.script

    def save(self):
        """
        Save board task data on filesystem.

        :ivar str setup_path: Setup path.
        :return: Dictionary containing the board task info to save.
        :rtype: dict
        """
        return {'type': 'create_scriptcmd', 'when': self.when, 'script': self.script}

    def load(self, data):
        """
        Load setup data from filesystem

        :ivar str setup_path: Path of the setup
        :ivar dict data: data object that contains all setup info
        """
        self.when = data['when']
        self.script = data['script']

    def collect_data(self, data):
        data.update({'script': self.script})
        data.update({'when': self.when})

        return data


class ExecCmd(TaskCommand):

    def __init__(self, task=None):
        super(ExecCmd, self).__init__(task)
        self.cmd = ''

    def execute(self, **kwargs):
        p = subprocess.Popen(
            self.cmd.split(' '),
            cwd=self.task.path,
            # stdin=subprocess.PIPE,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE
        )

    def __str__(self):
        return self.cmd

    def save(self):
        """
        Save board task data on filesystem.

        :ivar str setup_path: Setup path.
        :return: Dictionary containing the board task info to save.
        :rtype: dict
        """
        return {'type': 'create_execcmd', 'when': self.when, 'cmd': self.cmd}

    def load(self, data):
        """
        Load setup data from filesystem

        :ivar str setup_path: Path of the setup
        :ivar dict data: data object that contains all setup info
        """
        self.when = data['when']
        self.cmd = data['cmd']

    def collect_data(self, data):
        data.update({'cmd': self.cmd})
        data.update({'when': self.when})

        return data
