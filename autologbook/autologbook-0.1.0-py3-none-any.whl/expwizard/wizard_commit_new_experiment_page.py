import datetime
import re
from pathlib import Path

import elog
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QProgressDialog

from autologbook.autotools import generate_default_conf, write_conffile
from expwizard.constants import WizardPage, fully_implemented_microscope, microscope_lut
from expwizard.wizard_commit_new_experiment_page_ui import Ui_NewExperimentCommitPage


class CommitNewExperimentPage(QWizardPage, Ui_NewExperimentCommitPage):
    def __init__(self, parent):
        super().__init__(parent)

        self.setupUi(self)
        self.exp_filename_field.setVisible(False)
        self.registerField('exp_filename', self.exp_filename_field)

        self.setPixmap(QWizard.LogoPixmap, QPixmap(':/expwizard/ec-logo.jpg'))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(':/expwizard/glossy-microscope.png'))
        self.setCommitPage(True)

        if hasattr(parent, 'settings'):
            self.settings = parent.settings
        else:
            self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'ecjrc', 'experimentwizard')
        if hasattr(parent, 'timeout'):
            self.timeout = parent.timeout
        else:
            self.timeout = int(self.settings.value('elog_timeout', 10))

        self.elog_instance = None
        self.protocol_id = None
        self.msg_id = None

        self.local_path = None
        self.network_path = None
        self.experiment_filename = None
        self.message_attributes = {}
        self.attachments = []

    def validatePage(self) -> bool:
        # here is where the experiment is actually created.
        if not self.wizard().hasVisitedPage(WizardPage.PageReviewConfiguration):
            # if the Review configuration page was not visited, then the connection was not tested.
            # we need to do it now.
            self.wizard().page(WizardPage.PageReviewConfiguration).initializePage()
            if not self.wizard().page(WizardPage.PageReviewConfiguration).validatePage():
                return False

        num_steps = 5
        progress_dialog = QProgressDialog('Creating a new experiment', 'Abort creation', 0, num_steps - 1, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setWindowTitle('Progress')

        progress_dialog.setLabelText('Establishing connection to the elog server')
        if not self.elog_instance:
            self.elog_instance = self._get_elog_handle()
        progress_dialog.setValue(progress_dialog.value() + 1)

        progress_dialog.setLabelText('Posting the message')
        self.post_new_experiment_entry()
        progress_dialog.setValue(progress_dialog.value() + 1)

        progress_dialog.setLabelText('Preparing the folders')
        self.generate_folders()
        progress_dialog.setValue(progress_dialog.value() + 1)

        progress_dialog.setLabelText('Generating experiment file')
        self.generate_experiment_file()
        progress_dialog.setValue(progress_dialog.value() + 1)

        progress_dialog.setLabelText('Uploading experiment file')
        self.upload_experiment_file()
        progress_dialog.setValue(progress_dialog.value() + 1)

        return True

    def _get_elog_handle(self) -> elog.Logbook:
        return elog.open(
            hostname=self.settings.value('elog_hostname'),
            port=int(self.settings.value('elog_port')),
            user=self.settings.value('elog_user_name'),
            password=self.settings.value('elog_password'),
            use_ssl=self.settings.value('elog_use_ssl'),
            logbook=self.settings.value('protocol_list_logbook'),
            encrypt_pwd=False
        )

    def _get_next_protocol_id(self) -> int:
        last_msg_id = self.elog_instance.get_last_message_id(self.timeout)
        message, attributes, attachments = self.elog_instance.read(last_msg_id, self.timeout)
        last_protocol_id = attributes['Protocol number']
        last_protocol_id_number = int(str(last_protocol_id[4:]))
        next_protocol_id_prefix = f'{datetime.datetime.today():%y%m}'
        next_protocol_id_number = last_protocol_id_number + 1

        while True:
            ids = self.elog_instance.search({'Protocol number': next_protocol_id_number})
            if len(ids) != 0:
                next_protocol_id_number += 1
            else:
                break

        return int(f'{next_protocol_id_prefix}{next_protocol_id_number}')

    def post_new_experiment_entry(self):
        self.protocol_id = self._get_next_protocol_id()

        self.message_attributes = {
            'Protocol number': self.protocol_id,
            'Creation date': datetime.datetime.today().timestamp(),
            'Microscope': self.field('microscope'),
            'Operator': self.field('operator'),
            'Requesting unit': self.field('unit'),
            'Requesting user': self.field('project_responsible'),
            'Number of samples': self.field('number_of_samples'),
            'Sample_description': self.field('description'),
            'Analysis status': 'Waiting',
        }

        self.msg_id = self.elog_instance.post('', attributes=self.message_attributes, timeout=self.timeout)

    def generate_folders(self):
        # generate network_path path
        folder_name = Path('-'.join([str(self.protocol_id),
                                     self.field('project_name'),
                                     self.field('project_responsible')]))

        # perform a check on the network folder before continuing.
        self.check_network_folder()
        self.network_path = Path(self.settings.value('network_folder')) / folder_name
        self.network_path.mkdir(exist_ok=True, parents=True)

        if self.field('microscope') == 'Quattro':
            local = Path(self.settings.value('quattro_local_folder'))
        elif self.field('microscope') == 'FIB Versa 3D':
            local = Path(self.settings.value('versa_local_folder'))
        elif self.field('microscope') == 'Vega Tescan':
            local = Path(self.settings.value('vega_local_folder'))
        elif self.field('microscope') == 'XL40-GB':
            local = Path(self.settings.value('xl40gb_local_folder'))
        elif self.field('microscope') == 'XL40-Cold':
            local = Path(self.settings.value('xl40cold_local_folder'))
        else:
            local = ''
        self.local_path = local / folder_name
        self.local_path.mkdir(exist_ok=True, parents=True)

    def generate_experiment_file(self):

        if not self.field('microscope') in fully_implemented_microscope:
            # it makes no sense to generate an experiment file for a setup not yet implemented in the autologbook.
            return

        configuration = generate_default_conf()

        if self.field('microscope') in ['Quattro', 'FIB Versa 3D', 'Vega Tescan', 'XL40-GB', 'XL40-Cold']:
            mirror = True
        else:
            mirror = False

        configuration['GUI'] = {
            'src_path': str(self.local_path),
            'mirror_path': str(self.network_path),
            'mirror': mirror,
            'microscope': microscope_lut[self.field('microscope')],
            'custom_ownership': True,
            'projectID': self.protocol_id,
            'project_name': self.field('project_name'),
            'responsible': self.field('project_responsible'),
        }

        configuration['elog']['elog_user'] = self.settings.value('elog_user_name')
        configuration['elog']['elog_password'] = self.settings.value('elog_password')
        configuration['elog']['elog_hostname'] = self.settings.value('elog_hostname')
        configuration['elog']['elog_port'] = str(self.settings.value('elog_port'))
        configuration['elog']['use_ssl'] = str(self.settings.value('elog_use_ssl'))

        self.experiment_filename = self.local_path / Path(
            '-'.join([str(self.protocol_id), self.field('project_name'), self.field('project_responsible')]) + '.exp'
        )
        write_conffile(configuration, self.experiment_filename)
        self.attachments = [str(self.experiment_filename)]
        self.exp_filename_field.setText(str(self.experiment_filename))

    def nextId(self) -> int:
        return WizardPage.PageConclusion

    def upload_experiment_file(self):

        if not self.field('microscope') in fully_implemented_microscope:
            # it makes no sense to upload an experiment file for a setup not yet implemented in the autologbook.
            return

        self.elog_instance.post('', msg_id=self.msg_id, attributes=self.message_attributes,
                                attachments=self.attachments, encoding='HTML', timeout=self.timeout)

    def check_network_folder(self):
        """ Check if the network folder is ok

        Generally the network folder is ending with a year (four digits). It is helpful to have this year matching
        the current one.

        This method is taking care of check if the folder ends with a year, if so it is checking if the year is still
        current and otherwise, it is updating the default settings.

        """
        network_folder = Path(self.settings.value('network_folder'))

        # does the network folder finishes with a year?
        last_folder = network_folder.parts[-1]
        pattern = '^[0-9]{4}$'
        if re.search(pattern, last_folder):
            # yes there is a year at the end of the network folder. if so, we need, to check if the year is still
            # update
            if str(last_folder) != f'{datetime.datetime.now():%Y}':
                # HAPPY NEW YEAR!
                network_folder = network_folder.parent / Path(f'{datetime.datetime.now():%Y}')
                network_folder.mkdir(exist_ok=True, parents=True)
                self.settings.setValue('network_folder', str(network_folder))
