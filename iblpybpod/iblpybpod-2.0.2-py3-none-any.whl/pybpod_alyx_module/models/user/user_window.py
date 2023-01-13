from AnyQt import QtCore
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlButton, ControlLabel
from pybpod_alyx_module.module_api import AlyxModule
from AnyQt.QtWidgets import QLineEdit

from pybpodgui_api.models.project import Project
from pybpod_alyx_module.models.subject.alyx_subject import AlyxSubject
from pybpodgui_api.models.subject import Subject
from pybpodgui_api.models.user import User

class UserWindow(User, AlyxModule, BaseWidget):

    TITLE = 'Alyx connection'

    def __init__(self, _project):
        BaseWidget.__init__(self, self.TITLE)
        AlyxModule.__init__(self)
        User.__init__(self, _project)

        self.project = _project
        
        self._namebox = ControlText('User:')
        self._password = ControlText('Password:')
        self._connect_btn = ControlButton('Connect',default = self._connect)
        self._status_lbl = ControlLabel('Status: Not Connected')
        self._getsubjects_btn = ControlButton('Get Subjects', default = self._get_subjects)

        self.set_margin(10)

        self._namebox.value = self._name

        self._namebox.changed_event = self.__name_changed_evt
        
        self._password.form.lineEdit.setEchoMode(QLineEdit.Password)

        self.formset = [
            '_namebox',
            '_password',
            '_connect_btn',
            '_status_lbl',
            '_getsubjects_btn'
        ]

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def _connect(self):
        if self._connect_to_alyx(self._namebox.value,self._password.value):
            self._status_lbl.value = 'Status: CONNECTED'

    def _get_subjects(self):
        result = self.get_alyx_subjects(self._name)
        for subj in result:
            subjname = subj['nickname']
            existing = False
            for s in self.project.subjects:
                if s.name == subjname:
                    existing = True
                    reply = self.question('Subject' + s.name + 'Already exists locally. Replace details?', 'Update Subject')
                    if reply == 'yes':
                        s.add_alyx_info(subj)
            if existing == False:
                newsubject = AlyxSubject(self.project)
                newsubject.add_alyx_info(subj)

    
    def __name_changed_evt(self):
        if not hasattr(self, '_update_name') or not self._update_name:
            self.name = self._namebox.value
            

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._update_name = True  # Flag to avoid recursive calls when editing the name text field
        self._name = value
        self._update_name = False