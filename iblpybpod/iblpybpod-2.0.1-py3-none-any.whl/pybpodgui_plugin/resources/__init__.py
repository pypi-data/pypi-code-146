# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os

# see pyforms_generic_editor.resources.__init__ for generic icons


def path(filename):
    return os.path.join(os.path.dirname(__file__), 'icons', filename)


BOARD_SMALL_ICON = path('board.png')

BOARDS_SMALL_ICON = path('boards.png')
BOX_SMALL_ICON = path('box.png')

SUBJECT_SMALL_ICON = path('subject.png')
SUBJECTS_SMALL_ICON = path('subjects.png')
UPLOAD_SMALL_ICON = path('upload.png')

EXPERIMENT_SMALL_ICON = path('experiment.png')
EXPERIMENTS_SMALL_ICON = path('experiments.png')

TASK_SMALL_ICON = path('task.png')
TASKS_SMALL_ICON = path('tasks.png')

CODEFILE_SMALL_ICON = path('codefile.png')
OTHERFILE_SMALL_ICON = path('otherfile.png')

PERSON_SMALL_ICON = path('person.png')
PERSONS_SMALL_ICON = path('persons.png')

REFRESH_SMALL_ICON = path('refresh.png')