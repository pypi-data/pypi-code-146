import pyforms
from AnyQt import QtCore, QtGui
from pybpod_alyx_module.module_api import AlyxModule
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList


class AlyxDetails(AlyxModule, BaseWidget):

    TITLE = 'Alyx subject details'

    def __init__(self, _subject=None):
        BaseWidget.__init__(self, self.TITLE, parent_win=_subject.mainwindow)
        AlyxModule.__init__(self)

        self._details_list = ControlList('Alyx subject details', readonly=True)
        self._details_list += ('Nickname', _subject.name)
        #self._details_list += ('URL', _subject.alyx_url)
        self._details_list += ('ID', _subject.alyx_id)
        self._details_list += ('Responsible user', _subject.alyx_responsible_user)
        self._details_list += ('Birth date', _subject.alyx_birth_date)
        self._details_list += ('Age (weeks)', _subject.alyx_age_weeks)
        self._details_list += ('Death date', _subject.alyx_death_date)
        self._details_list += ('Species', _subject.alyx_species)
        self._details_list += ('Sex', _subject.alyx_sex)
        self._details_list += ('Litter', _subject.alyx_litter)
        self._details_list += ('Strain', _subject.alyx_strain)
        self._details_list += ('Source', _subject.alyx_source)
        self._details_list += ('Line', _subject.alyx_line)
        self._details_list += ('Projects', ", ".join(map(str, _subject.alyx_projects)) if _subject.alyx_projects else None)
        self._details_list += ('Lab', _subject.alyx_lab)
        self._details_list += ('Genotype', ", ".join(map(str, _subject.alyx_genotype)) if _subject.alyx_genotype else None)
        self._details_list += ('Description', _subject.alyx_description)
        self._details_list += ('Alive', _subject.alyx_alive)
        #self._details_list += ('Weighings', ", ".join(map(str, _subject.alyx_weighings)) if _subject.alyx_weighings else None)
        #self._details_list += ('Reference weight', _subject.alyx_reference_weight)
        #self._details_list += ('Water administrations', ", ".join(map(str, _subject.alyx_water_administrations)) if _subject.alyx_water_administrations else None)
        #self._details_list += ('Last water restriction', _subject.alyx_last_water_restriction)
        #self._details_list += ('Expected water', _subject.alyx_expected_water)
        #self._details_list += ('Remaining water', _subject.alyx_remaining_water)

        self.set_margin(10)
        self.setMinimumWidth(500)
        self.setMinimumHeight(560)

        self.formset = [
            '_details_list'
        ]

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    pyforms.start_app(AlyxDetails, geometry=(0, 0, 300, 300))
