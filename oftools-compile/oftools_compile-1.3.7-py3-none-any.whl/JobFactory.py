#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to retrieve the parameters entered by the user and launch the corresponding job.

Typical usage example:
  job_factory = JobFactory(profile)
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Clear import Clear
from .CompileJob import CompileJob
from .DeployJob import DeployJob
from .SetupJob import SetupJob


class JobFactory(object):
    """A class used to create all the jobs required with the given profile.

    Attributes:
        _profile {Profile}

    Methods:
        __init__(profile) -- Initializes the class with the _profile attribute.
        create(job_name) -- Creates the job according to the input parameter.
    """

    def __init__(self, profile):
        """Initializes the class with the _profile attribute.
        """
        self._profile = profile

    def create(self, job_name):
        """Creates the job according to the input parameter.

        Arguments:
            job_name {string} -- Name of the section in the profile or name of the command line option used (grouping and clear).

        Returns:
            Job object -- Appropriate Job object depending on the input.
        """
        if job_name.startswith('setup'):
            return SetupJob(self._profile, job_name)
        elif job_name.startswith('deploy'):
            return DeployJob(self._profile, job_name)
        elif job_name == 'clear':
            return Clear()
        else:
            return CompileJob(self._profile, job_name)