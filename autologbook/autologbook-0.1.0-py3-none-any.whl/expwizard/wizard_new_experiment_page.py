from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizard, QWizardPage

from expwizard.constants import WizardPage
from expwizard.wizard_new_experiment_page_ui import Ui_NewExperimentPage


class NewExperimentPage(QWizardPage, Ui_NewExperimentPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.setPixmap(QWizard.LogoPixmap, QPixmap(':/expwizard/ec-logo.jpg'))

        self.registerField('project_name*', self.project_name)
        self.registerField('project_responsible*', self.project_responsible)
        self.registerField('unit', self.unit_combobox, 'currentText', self.unit_combobox.currentIndexChanged)

        self.registerField('description', self.sample_description, 'plainText', self.sample_description.textChanged)
        self.registerField('number_of_samples', self.number_of_samples)
        self.registerField('microscope', self.microscope_combobox, 'currentText',
                           self.microscope_combobox.currentIndexChanged)
        self.registerField('operator', self.microscope_operator)

    def nextId(self) -> int:
        return WizardPage.PageCommitNewExperiment
