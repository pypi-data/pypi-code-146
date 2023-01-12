from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlLabel
from pyforms.controls   import ControlText
from pyforms.controls   import ControlList
from pyforms.controls   import ControlButton
from pyforms.controls   import ControlProgress
from pyforms.controls   import ControlTextArea
from pyforms.controls   import ControlCombo
from pyforms.controls   import ControlWeb

from AnyQt.QtWidgets import QApplication
from AnyQt.QtCore    import QTimer

from .package_win    import PackageWindow

from confapp import conf

from importlib import reload

import yaml
import sys
import subprocess
import xmlrpc.client
import pkg_resources
import datetime

import markdown2

conf.PYBPOD_REPOSITORIES_TXT_LIST = '../../repositories.yml'


class UpdateCenter(BaseWidget):

    MAIN_PACKAGE_NAME = 'pyforms-gui'

    pypi = xmlrpc.client.ServerProxy('https://pypi.org')

    def __init__(self, *args, **kwargs):
        super().__init__('Update center')

        self.set_margin(10)

        self._versions      = ControlCombo('Versions', changed_event=self.__versions_changed_evt)
        self._web           = ControlWeb('Web', default='https://google.com')
        self._install       = ControlButton('Install')

        #Definition of the forms fields
        self._packageslst = ControlList('PACKAGES', readonly=True, select_entire_row=True)
        self._searchbox   = ControlText('Search')
        self._searchbtn   = ControlButton('Load packages', default=self.__searchbtn_evt)
        self._progress    = ControlProgress('Progress')

        self._formset = [
            {
                'Available versions': [
                    (' ', '_versions','_install'),
                    '_web',
                ],
                'Packages': [
                    '_packageslst'
                ]
            },
            '_progress'
        ]
        QTimer.singleShot(300, self.load_packages_list)

    def __searchbtn_evt(self):
        self.load_packages_list()


    def __versions_changed_evt(self):
        """
        Called to update the version documentation
        """
        version = self._versions.value
        data = self.pypi.release_data(self.MAIN_PACKAGE_NAME, version)
        self._web.html = markdown2.markdown( data.get('description', '') )


    def load_application_info(self):

        name = 'pyforms-gui'

        new_version = self.pypi.package_releases(name)
        if not new_version:
            new_version = self.pypi.package_releases(name.capitalize())

        if new_version is None: return new_version

        new_version  = new_version[0]
        all_versions = self.pypi.package_releases(name, True)
        data = self.pypi.release_data(name, new_version)


        return new_version, all_versions, data.get('description', '')


    def load_packages_list(self):
        reload(pkg_resources)
        self._packageslst.clear()
        QApplication.processEvents()

        new_version, all_versions, description = self.load_application_info()
        
        self._web.html = markdown2.markdown(description, extras=["footnotes"])


        with open(conf.PYBPOD_REPOSITORIES_TXT_LIST) as infile:

            data = yaml.load(infile)
            
            self._versions.clear()
            for recipe in data.get('recipes', []):
                for name, d in recipe.items():
                    self._versions.add_item(name)
                    #self._web.html = d.get('description', '')


            packages_lst = data.get('packages',[])

            self._progress.value = 0
            self._progress.max   = len(packages_lst)

            for index, name in enumerate(packages_lst):
                name = name.strip(' \t\n\r')

                QApplication.processEvents()

                
                self._packageslst += [PackageWindow(title=name, parent_widget=self)]

                self._progress.value = index+1
                QApplication.processEvents()

            self._progress.hide()


