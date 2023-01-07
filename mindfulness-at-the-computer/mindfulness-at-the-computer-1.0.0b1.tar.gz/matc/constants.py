"""
This file is separete from shared.py since that file/module contains functions that require
access to QtCore and QtGui, and this file has to be used during the setup process, before we have
imported pyside
"""

# APPLICATION_VERSION = "1.0.0-beta.1-dev.6"
# [Semantic versioning](semver.org) is used, and we may also add `dev` at the end of the version
# Example: `1.2.3-alpha.4-dev.5`

APPLICATION_PRETTY_NAME = "Mindfulness at the Computer"
APPLICATION_NAME = "mindfulness-at-the-computer"
EMAIL_ADDRESS = "tord.dellsen@gmail.com"

SHORT_DESCR = "Helps you stay mindful of your breathing while using your computer."

LOG_FILE_NAME_STR = "matc.log"

"""
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        # print("Please run this to start the application the first time: python3 -m matc")


class PostInstallCommand(install):
    def run(self):
        install.run(self)
"""
