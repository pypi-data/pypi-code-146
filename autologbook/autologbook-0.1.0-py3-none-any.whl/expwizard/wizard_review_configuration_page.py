import datetime
from pathlib import Path

import elog
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizard, QWizardPage, QFileDialog, QLineEdit, QDoubleSpinBox, QSpinBox, QCheckBox, \
    QMessageBox, QProgressDialog

from autologbook.autotools import encrypt_pass
from expwizard.constants import WizardPage, default_settings
from expwizard.wizard_review_configuration_page_ui import Ui_ReviewConfigurationPage


class ReviewConfigurationPage(QWizardPage, Ui_ReviewConfigurationPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setPixmap(QWizard.LogoPixmap, QPixmap(':/expwizard/ec-logo.jpg'))
        if hasattr(parent, 'settings'):
            self.settings = parent.settings
        else:
            self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'ecjrc', 'experimentwizard')
        self.timeout = float(self.settings.value('elog_timeout',10))
        self.password_needs_update = False
        self.connection_is_ok = False

    def _sleep_inputs(self, sleep: bool = True):

        for widget in [widget for widget in self.findChildren((QLineEdit, QDoubleSpinBox, QSpinBox, QCheckBox))
                       if not widget.objectName().startswith('qt_spinbox')]:
            widget.blockSignals(sleep)

    def initializePage(self) -> None:
        '''
        Pre-fill the field values with the ones stored in setting.

        These parameters are stored in the settings instead that on Wizard fields because we want them to be persistent
        between following application executions.

        '''

        self.elog_user_field.setText(self.settings.value('elog_user_name', 'log-robot', type=str))
        self.elog_password_field.setText(self.settings.value('elog_password', 'mTZtK2iFHhwqixkhJV0JkplSqMMu9ykWOhcNY'
                                                                              '/1WyL7', type=str))
        self.elog_hostname_field.setText(self.settings.value('elog_hostname', 'https://10.166.16.24', type=str))
        self.elog_port_field.setValue(self.settings.value('elog_port', 8080, type=int))
        self.elog_ssl_check_box.setChecked(self.settings.value('elog_use_ssl', True, type=bool))
        self.elog_timeout_spinbox.setValue(self.settings.value('elog_timeout', 12, type=float))

        self.protocol_list_logbook_field.setText(
            self.settings.value('protocol_list_logbook', 'Microscopy-Protocol', type=str))
        self.network_folder.setText(
            self.settings.value('network_folder', f'R:\\A226\\Results\\{datetime.datetime.now():%Y}', type=str))

        self.quattro_elog_logbook_field.setText(self.settings.value('quattro_logbook', 'Quattro-Analysis', type=str))
        self.quattro_local_path.setText(self.settings.value('quattro_local_folder', 'M:\\', type=str))

        self.versa_elog_logbook_field.setText(self.settings.value('versa_logbook', 'Versa-Analysis', type=str))
        self.versa_local_path.setText(self.settings.value('versa_local_folder', 'M:\\', type=str))

        self.vega_elog_logbook_field.setText(self.settings.value('vega_logbook', 'Vega-Analysis', type=str))
        self.vega_local_path.setText(self.settings.value('vega_local_folder', 'M:\\', type=str))

        self.xl40gb_elog_logbook_field.setText(self.settings.value('xl40gb_logbook', 'XL40-GB-Analysis', type=str))
        self.xl40gb_local_path.setText(self.settings.value('xl40gb_local_folder', 'M:\\', type=str))

        self.xl40cold_elog_logbook_field.setText(self.settings.value('xl40cold_logbook', 'XL40-Cold-Analysis', type=str))
        self.xl40cold_local_path.setText(self.settings.value('xl40cold_local_folder', 'M:\\', type=str))

    def password_changed(self):
        self.password_needs_update = True

    def search_folder(self):

        lut = {
            'network_path_search_button': self.network_folder,
            'quattro_path_search_button': self.quattro_local_path,
            'versa_path_search_button': self.versa_local_path,
            'vega_path_search_button': self.vega_local_path,
            'xl40gb_path_search_button': self.xl40gb_local_path,
            'xl40cold_path_search_button': self.xl40cold_local_path,
        }
        button_name = self.sender().objectName()

        if button_name in lut.keys():
            field = lut[button_name]
            folder = QFileDialog.getExistingDirectory(self, 'Select a folder', str(Path(field.text())))
            if folder:
                field.setText(str(Path(folder)))

    def validatePage(self) -> bool:
        self.update_settings()
        if self.connection_is_ok:
            return True
        else:
            return self.test_connection()

    def _get_elog_handle(self, logbook: str) -> elog.Logbook:
        return elog.open(
            hostname=self.elog_hostname_field.text(),
            port=self.elog_port_field.value(),
            user=self.elog_user_field.text(),
            password=self._encrypt_pass(),
            use_ssl=self.elog_ssl_check_box.isChecked(),
            logbook=logbook,
            encrypt_pwd=False
        )

    def connection_to_be_retested(self):
        self.connection_test_label.setText('Parameters changed. Connection need to be re-tested')
        self.connection_is_ok = False

    def test_connection(self) -> bool:

        logbook_to_be_tested = [self.protocol_list_logbook_field.text(),
                                self.quattro_elog_logbook_field.text(),
                                self.versa_elog_logbook_field.text(),
                                self.vega_elog_logbook_field.text(),
                                self.xl40gb_elog_logbook_field.text(),
                                self.xl40cold_elog_logbook_field.text()]

        operation_to_be_tested = ['read', 'write', 'delete']

        number_of_test = len(logbook_to_be_tested) * len(operation_to_be_tested)

        progress_dialog = QProgressDialog('Testing connection', 'Abort connection test', 0, number_of_test-1,self )
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setWindowTitle('Progress...')


        for logbook in logbook_to_be_tested:
            if progress_dialog.wasCanceled():
                break
            logbook_instance = self._get_elog_handle(logbook)
            mid = -1
            if 'Analysis' in logbook:
                attrib = {
                    'Operator': self.elog_user_field.text(),
                    'Protocol ID': -1,
                    'Project': 'Test project',
                    'Customer': 'Test customer'
                }
            else:
                attrib = dict()

            for operation in operation_to_be_tested:
                progress_dialog.setValue(progress_dialog.value()+1)
                progress_dialog.setLabelText(f'Checking {operation} operation on {logbook}')
                if progress_dialog.wasCanceled():
                    break
                try:
                    if operation == 'read':
                        logbook_instance.get_last_message_id(timeout=self.timeout)
                    elif operation == 'write':
                        mid = logbook_instance.post('Test message', attributes=attrib, timeout=self.timeout)
                    elif operation == 'delete':
                        logbook_instance.delete(mid)
                except elog.LogbookError:
                    QMessageBox.critical(self, 'Connection test',
                                         f'Test of type \'{operation}\' on logbook {logbook} failed!')
                    progress_dialog.close()
                    self.connection_is_ok = False
                    self.connection_test_label.setText('Connection test failed!')
                    return False

        self.connection_is_ok = True
        self.connection_test_label.setText('Connection test successful!')
        return True

    def nextId(self) -> int:

        if self.field('new_experiment'):
            return WizardPage.PageNewExperiment
        else:
            return WizardPage.PageConclusion

    def update_settings(self):

        # for the password field we cannot take directly the value from the field
        self.settings.setValue('elog_password', self._encrypt_pass())

        # for all other parameters, just move the field content to the corresponding setting value.
        self.settings.setValue('elog_user_name', self.elog_user_field.text())
        self.settings.setValue('elog_hostname', self.elog_hostname_field.text())
        self.settings.setValue('elog_port', self.elog_port_field.value())
        self.settings.setValue('elog_use_ssl', self.elog_ssl_check_box.isChecked())
        self.settings.setValue('elog_timeout', self.elog_timeout_spinbox.value())

        self.settings.setValue('protocol_list_logbook', self.protocol_list_logbook_field.text())

        self.settings.setValue('quattro_logbook', self.quattro_elog_logbook_field.text())
        self.settings.setValue('versa_logbook', self.versa_elog_logbook_field.text())
        self.settings.setValue('vega_logbook', self.vega_elog_logbook_field.text())
        self.settings.setValue('xl40gb_logbook', self.xl40gb_elog_logbook_field.text())
        self.settings.setValue('xl40cold_logbook', self.xl40cold_elog_logbook_field.text())

        self.settings.setValue('network_folder', str(Path(self.network_folder.text())))
        self.settings.setValue('quattro_local_folder', str(Path(self.quattro_local_path.text())))
        self.settings.setValue('versa_local_folder', str(Path(self.versa_local_path.text())))
        self.settings.setValue('vega_local_folder', str(Path(self.vega_local_path.text())))
        self.settings.setValue('xl40gb_local_folder', str(Path(self.xl40gb_local_path.text())))
        self.settings.setValue('xl40cold_local_folder', str(Path(self.xl40gb_local_path.text())))

    def _encrypt_pass(self) -> str:
        if self.password_needs_update:
            self.elog_password_field.setText(encrypt_pass(self.elog_password_field.text()))
            self.password_needs_update = False
        return self.elog_password_field.text()

    def restore_defaults(self):

        # put the default values in the settings
        for key, value in default_settings.items():
            self.settings.setValue(key, value['value'])

        # transfer the settings to the GUI
        self.initializePage()

        # remember that the password is already encrypted
        self.password_needs_update = False