"""
Implement the experiment wizard

This file contains the implementation class of the ExperimentWizard used to create a new experiment or to continue an
existing one.

The user has to decide at the beginning of the wizard, if he is about to start a new experiment or continue an
existing one.

If a new experiment is started, then he has to enter the details of the experiment and the wizard will
perform the following actions:

    1.  Get a new and unique protocol ID from the microscopy protocol logbook.

    2.  Insert an entry in this logbook with the parameters provided by the user.

    3.  Depending on the microscope selection, experiment folders will be created on both the local_path disk and on the
        remote drive.

    4.  An experiment file (containing the information provided by the user, the protocol ID and the directory paths)
        is generated. This file can be directly opened in autologbook to start the automatic documentation.

    5.  The experiment file is attached to the microscopy protocol logbook entry for future use.

At this point, the user can start automatically the autologbook tool with the newly generated experiment file.

If the user wants to continue an existing experiment, then first of all, he needs to find the experiment he wants to
continue. This is accomplished from a dedicated wizard page. Once the protocol ID of the desired experiment is found,
then the following actions are performed:

    1.  Check if the entry in the microscopy protocol logbook has an experiment file attached and if the microscope
        is fully supported by the autologbook tool.
        It is possible that the user has in the local folder also a copy of the experiment file. If a local one is
        found, and it is different from the remote one, then the user is asked to compare and decide which one to use.

        If the microscope is not fully supported, the wizard has nothing else to do.

    2.  If the entry has no attached experiment file, but the microscope is fully supported then the following is done:
        2.1 A local folder with the same protocol number is searched for an experiment file. If more than one is found,
            the user can decide which one to use.
        2.2 If no experiment file is found, then the remote folder is also search for one.
        2.3 If also there, there was none, then a new one is made with the information taken from the protocol list.

    3.  At this point we should have an experiment file. If the microscope is fully supported, then the user can start
        the autologbook directly with it.

"""

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QWizard

from autologbook.autogui import main_gui as autogui_main
from autologbook.autotools import main_parser
from expwizard.constants import WizardPage
from expwizard.wizard_commit_new_experiment_page import CommitNewExperimentPage
from expwizard.wizard_conclusion_page import ConclusionPage
from expwizard.wizard_introduction_page import IntroductionPage
from expwizard.wizard_new_experiment_page import NewExperimentPage
from expwizard.wizard_review_configuration_page import ReviewConfigurationPage
from expwizard.wizard_search_experiment_page import SearchExperimentPage

from . import resources_rc


class ExperimentWizard(QWizard):
    """
    Experiment Wizard class

    This implementation of the QWizard is allowing the user to create a new experiment or to continue an already
    existing one.

    This is the loop of pages

    1. IntroductionPage.
        The user has to select new experiment or existing one and can tick the review configuration option.

    2. ReviewConfigurationPage.
        If review configuration is ticked, then go to the review page. This page can be skipped.

    3. If new experiment then:
        3.1 NewExperimentParameterPage.
            The user has to insert all parameters
        3.2 CommitNewExperimentPage.
            The user confirm that everything is ok to go ahead.
        3.3 CreationNewExperimentPage.
            This is where the real job is done. The user can follow on the screen the progress.

    4. If old experiment then:
        4.1 SearchExperimentPage.
            Allow the user to search for an experiment from the microscopy protocol list.
            In the validatePage, perform all the required checks.
            - The selected protocol may or may not have an experiment attached.
            - The selected protocol may or may not have a microscope that is fully supported.

    5. ConclusionPage.
        Summary of what happened.
        Checkbox to start autologbook with the experiment if the microscope is fully supported.
    """

    def __init__(self, parent: QWidget = None, app: QApplication = None):
        super().__init__(parent=parent)
        self.app = app

        # insert here all pages
        self.setPage(WizardPage.PageIntro, IntroductionPage(self))
        self.setPage(WizardPage.PageReviewConfiguration, ReviewConfigurationPage(self))
        self.setPage(WizardPage.PageNewExperiment, NewExperimentPage(self))
        self.setPage(WizardPage.PageCommitNewExperiment, CommitNewExperimentPage(self))
        self.setPage(WizardPage.PageSearchExperiment, SearchExperimentPage(self))
        self.setPage(WizardPage.PageConclusion, ConclusionPage(self))

        # declare from which page you want to start
        self.setStartId(WizardPage.PageIntro)

        # do some look and feel changes
        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowTitle('EC-JRC-Karlsruhe - Microscopy lab')
        self.setWindowIcon(QIcon(QPixmap(':/expwizard/glossy-microscope.png')))

        # we want to have a help button
        self.setOption(QWizard.HaveHelpButton, True)
        self.setOption(QWizard.HelpButtonOnRight, False)
        # noinspection PyUnresolvedReferences
        self.helpRequested.connect(self.show_help)

        # this object contains the setting.
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'ecjrc', 'experimentwizard')
        self.timeout = int(self.settings.value('elog_timeout', 10))

        # the protocol id with its corresponding msg_id
        self.protocol_id = None
        self.msg_id = None

    def show_help(self):
        """Show a help message for the current page"""

        if self.currentId() == WizardPage.PageIntro:
            message = 'The procedure to start a <b>new</b> experiment or to continue an <b>existing</b> one begins ' \
                      'here. Select one of the two options and click next to continue.<br><br>' \
                      'All configuration settings can be reviewed and the connection to the logbook verified by ' \
                      'ticking the corresponding checkbox. '

        elif self.currentId() == WizardPage.PageReviewConfiguration:
            message = 'Carefully review the value of all the configuration parameters. If unsure, you can restore the' \
                      ' default values by clicking on the corresponding button. <br><br> When clicking on Next, ' \
                      'the inserted parameters will be stored in the application settings for future use and a ' \
                      'connection test will be performed. <br><br> Connection tests can be performed anytime by ' \
                      'clicking on the corresponding button. '

        elif self.currentId() == WizardPage.PageNewExperiment:
            message = 'Fill in the presented fields in order to generate a new entry in the microscopy protocol list ' \
                      'and to be able to start the experiment.'

        elif self.currentId() == WizardPage.PageCommitNewExperiment:
            message = 'From this page you can confirm the generation of the new experiment.'

        elif self.currentId() == WizardPage.PageConclusion:
            message = 'You have done everything. If you want, select the checkbox to automatically start autologbook ' \
                      'with the new or with the selected experiment. '

        elif self.currentId() == WizardPage.PageSearchExperiment:
            message = 'Since you want to continue an existing experiment, this page will help you in finding it. ' \
                      '<br><br>' \
                      'Use the fields in the top part to insert some searching criteria, keep in mind that all fields '\
                      'are logically ORed and then press Search. <br><br>' \
                      'The results will be shown in the table below, from where you can select the experiment you ' \
                      'want to continue. <br><br>' \
                      'Selecting one of them will allow you to continue in the wizard.' \


        else:
            message = 'Sorry, no help is available at this stage for this specific page.'

        QMessageBox.information(self, 'Experiment wizard help', message)

    def accept(self) -> None:
        """
        Reimplement the accept method.

        If the user selected the option to automatically start the autologbook, this will be launched from here
        """
        if bool(self.field('start')):
            parser = main_parser()
            args = parser.parse_args(['--no-qapp', '-l', 'vipdebug', '-e', self.field('exp_filename'), '-x'])
            autogui_main(args)

        super(ExperimentWizard, self).accept()
