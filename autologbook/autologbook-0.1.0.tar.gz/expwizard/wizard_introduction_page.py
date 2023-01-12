from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizard, QWizardPage

from expwizard.constants import WizardPage
from expwizard.wizard_introduction_page_ui import Ui_IntroductionPage


class IntroductionPage(QWizardPage, Ui_IntroductionPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # setting the style parameters. It is not possible to set them from the Designer
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(':/expwizard/glossy-microscope.png'))
        self.setPixmap(QWizard.LogoPixmap, QPixmap(':/expwizard/ec-logo.jpg'))

        self.registerField('new_experiment',self.new_experiment_radio)
        self.registerField('review_configuration', self.review_configuration_checkbox)

    def nextId(self) -> int:
        if self.review_configuration_checkbox.isChecked():
            return WizardPage.PageReviewConfiguration
        else:
            if self.new_experiment_radio.isChecked():
                return WizardPage.PageNewExperiment
            else:
                return WizardPage.PageSearchExperiment