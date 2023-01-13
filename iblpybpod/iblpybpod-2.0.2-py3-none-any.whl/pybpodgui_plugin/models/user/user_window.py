from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pybpodgui_api.models.user import User


class UserWindow(User, BaseWidget):

    def __init__(self, project=None):

        BaseWidget.__init__(self, 'User')
        self._namebox = ControlText('Name')
        User.__init__(self, project)

        # print(self._name)

        self.layout().setContentsMargins(5, 10, 5, 5)

        self._formset = [
            '_namebox'
        ]

        self._namebox.value = self._name

        self._namebox.changed_event = self.__name_changed_evt

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
        self._namebox.value = value
        self._update_name = False
