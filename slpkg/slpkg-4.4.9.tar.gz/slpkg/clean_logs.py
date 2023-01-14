#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.views.views import ViewMessage
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class CleanLogsDependencies:
    """ Cleans the logs from packages. """

    def __init__(self, flags: list):
        self.flags = flags
        self.session = Session

    def clean(self):
        """ Deletes the log table from the database. """
        dependencies = self.session.query(
            LogsDependencies.name, LogsDependencies.requires).all()

        if dependencies:
            view = ViewMessage(self.flags)
            view.logs_packages(dependencies)
            view.question()

            self.session.query(LogsDependencies).delete()
            self.session.commit()
        else:
            print('\nNothing to clean.\n')
