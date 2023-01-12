import configparser
import re
import shutil
import webbrowser
from pathlib import Path

import elog
import requests
from PyQt5.QtCore import QSettings, QSortFilterProxyModel, Qt, QModelIndex
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QProgressDialog, QWizard, QWizardPage, QDialog, QMessageBox

from autologbook.autotools import generate_default_conf, write_conffile
from expwizard import search_results_model
from expwizard.constants import WizardPage, microscope_in_protocol_list, fully_implemented_microscope, microscope_lut
from expwizard.dialog_compare_experiment_file import CompareExperimentDialog
from expwizard.dialog_select_experiment_file import SelectExperimentDialog
from expwizard.wizard_search_experiment_page_ui import Ui_SearchExperimentPage


class SearchExperimentPage(QWizardPage, Ui_SearchExperimentPage):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setPixmap(QWizard.LogoPixmap, QPixmap(':/expwizard/ec-logo.jpg'))
        self.microscope_combo.addItem(' -- ALL -- ')
        self.microscope_combo.addItems(microscope_in_protocol_list)

        if hasattr(parent, 'settings'):
            self.settings = parent.settings
        else:
            self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'ecjrc', 'experimentwizard')
        if hasattr(parent, 'timeout'):
            self.timeout = parent.timeout
        else:
            self.timeout = int(self.settings.value('elog_timeout', 10))

        # create the model
        self.search_results_model = search_results_model.SearchResultsModel()
        # create the proxy and set it to the model
        self.search_results_proxy_model = QSortFilterProxyModel(self)
        self.search_results_proxy_model.setSourceModel(self.search_results_model)
        # set the table view to the proxy model
        self.search_results_table_view.setModel(self.search_results_proxy_model)
        self.search_results_table_view.setSortingEnabled(True)
        self.search_results_table_view.verticalHeader().setVisible(False)

        self.registerField('msg_id', self.msg_id_field)

    def initializePage(self) -> None:
        if not self.wizard().hasVisitedPage(WizardPage.PageReviewConfiguration):
            # if the Review configuration page was not visited, then the connection was not tested.
            # we need to do it now.
            self.wizard().page(WizardPage.PageReviewConfiguration).initializePage()
            if not self.wizard().page(WizardPage.PageReviewConfiguration).validatePage():
                QMessageBox.critical(self, 'Connection error', 'There was a connection error. Go back to the previous '
                                                               'page and review the configuration setting.',
                                     buttons=QMessageBox.Ok)

    def nextId(self) -> int:
        return WizardPage.PageConclusion

    def search_experiment(self):

        attributes_to_be_searched = dict()

        if self.protocol_id_search_field.text():
            attributes_to_be_searched['Protocol number'] = self.protocol_id_search_field.text()

        if self.microscope_combo.currentText() != ' -- ALL -- ':
            attributes_to_be_searched['Microscope'] = self.microscope_combo.currentText()

        if self.requesting_user_search_field.text():
            attributes_to_be_searched['Requesting user'] = self.requesting_user_search_field.text()

        if self.requesting_unit_search_field.text():
            attributes_to_be_searched['Requesting unit'] = self.requesting_user_search_field.text()

        progress_dialog = QProgressDialog('Performing DB search', 'Abort search', 0, 0, self)
        progress_dialog.setValue(0)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setWindowTitle('Progress')

        logbook = self._get_elog_handle()
        ids = logbook.search(attributes_to_be_searched)
        progress_dialog.setMaximum(len(ids))
        results = list()
        for msg_id in ids:
            message, attributes, attachments = logbook.read(msg_id)
            record = search_results_model.ProtocolRecord.from_elog_attributes(attributes)
            record.msg_id = msg_id
            record.url = f'{self.settings.value("elog_hostname")}:{self.settings.value("elog_port")}/' \
                         f'{self.settings.value("protocol_list_logbook")}/{msg_id}'
            for attach in attachments:
                pattern = re.compile(fr"{attributes['Protocol number']}-.*\.exp$")
                if pattern.search(attach):
                    record.experiment_filename = attach
                    break
            results.append(record)
            progress_dialog.setValue(progress_dialog.value() + 1)
            if msg_id % 10 == 0:
                self.search_results_model.set_search_results(results)

        self.search_results_model.set_search_results(results)

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

    def record_selected(self, index: QModelIndex):
        if index.isValid():
            self.msg_id_field.setText(str(index.data(search_results_model.SearchResultsModel.UserRole.MSG_ID)))
            self.experiment_file_field.setText(
                index.data(search_results_model.SearchResultsModel.UserRole.EXPERIMENT_FILE))
            self.open_record_button.setEnabled(True)
            self.setField('microscope', index.data(search_results_model.SearchResultsModel.UserRole.MICROSCOPE))
        else:
            self.msg_id_field.clear()
            self.experiment_file_field.clear()
            self.open_record_button.setEnabled(False)
            self.setField('microscope', '')
        self.completeChanged.emit()
        self.setField('exp_filename', self.experiment_file_field.text())

    def open_record_in_browser(self):
        index = self.search_results_table_view.selectionModel().currentIndex()
        if index.isValid():
            webbrowser.open(index.data(search_results_model.SearchResultsModel.UserRole.URL), new=0, autoraise=True)

    def isComplete(self) -> bool:
        return self.search_results_table_view.selectionModel().currentIndex().isValid()

    def validatePage(self) -> bool:
        # do we have an exp file?

        if self.experiment_file_field.text():
            # if so, then download it to a temporary file
            response = requests.get(self.experiment_file_field.text(), verify=False)
            url = Path(self.experiment_file_field.text())

            # read in the experiment file
            remote_exp = configparser.ConfigParser()
            remote_exp.read_string(response.content.decode('utf-8'))

            # it is possible that we have already a local experiment file.
            # if so, it must be in the src_path
            if remote_exp.get('GUI', 'src_path', fallback='None'):
                src_path = Path(remote_exp.get('GUI', 'src_path'))
                # search for exp in this folder.
                local_exp_files = list()
                for exp_file in src_path.glob('*.exp'):
                    local_exp_files.append(exp_file)

                if len(local_exp_files) == 0:
                    # no experiment file found locally.
                    # then we just save the remote one in the local folder.
                    filename = src_path / Path(str(url.name)[14:])
                    write_conffile(remote_exp, filename)
                    self.setField('exp_filename', str(filename))

                elif len(local_exp_files) == 1:
                    # we found one file, let's open it to compare it with the remote one
                    local_exp = configparser.ConfigParser()
                    local_exp.read(local_exp_files[0])

                    if remote_exp == local_exp:
                        # the two are identical, so forget about the remote and use the local.
                        self.setField('exp_filename', str(local_exp_files[0]))
                    else:
                        # now we are in troubles.
                        dialog = CompareExperimentDialog(self)
                        dialog.load_remote_experiment(str(Path(url.name)), response.content)
                        dialog.load_local_experiment_list(local_exp_files)
                        return_code = dialog.exec()
                        if return_code == CompareExperimentDialog.ReturnValue.AcceptLocal:
                            self.setField('exp_filename', dialog.local_experiment_selector.currentText())
                            print('accepting local %s' % dialog.local_experiment_selector.currentText())
                        elif return_code == CompareExperimentDialog.ReturnValue.AcceptRemote:
                            # we overwrite the local one.
                            bck = str(local_exp_files[0]) + '.bck'
                            shutil.copy(local_exp_files[0], Path(bck))
                            write_conffile(remote_exp, local_exp_files[0])
                            self.setField('exp_filename', str(local_exp_files[0]))
                        else:
                            QMessageBox.critical(self, 'Experiment file.', 'You have to select either the remote or '
                                                                           'the local file.')
                            return False
                elif len(local_exp_files) > 1:
                    # we found several exp local files
                    dialog = CompareExperimentDialog(self)
                    dialog.load_remote_experiment(str(Path(url.name)), response.content)
                    dialog.load_local_experiment_list(local_exp_files)
                    return_code = dialog.exec()
                    if return_code == CompareExperimentDialog.ReturnValue.AcceptLocal:
                        self.setField('exp_filename', dialog.local_experiment_selector.currentText())
                        print('accepting local %s' % dialog.local_experiment_selector.currentText())
                    elif return_code == CompareExperimentDialog.ReturnValue.AcceptRemote:
                        filename = Path(str(Path(str(url.name)[14:])))  # remove the timestamp
                        write_conffile(remote_exp, src_path / filename)
                        self.setField('exp_filename', str(src_path / filename))
                    else:
                        QMessageBox.critical(self, 'Experiment file.', 'You have to select either the remote or '
                                                                       'one the local files.')
                        return False

        else:
            # we don't have an experiment file
            if self.field('microscope') in fully_implemented_microscope:
                # we don't have an experiment file, but the microscope is fully implemented, so we can generate one
                self.generate_experiment_file()

        return True

    def generate_experiment_file(self):
        record = search_results_model. \
            ProtocolRecord.from_tuple(
            self.search_results_table_view.currentIndex().data(search_results_model.SearchResultsModel.UserRole.TUPLE))

        # search for the local folder
        if record.microscope == 'Quattro':
            base_local_folder = Path(self.settings.value('quattro_local_folder'))
        elif record.microscope == 'FIB Versa 3D':
            base_local_folder = Path(self.settings.value('versa_local_folder'))
        elif record.microscope == 'Vega Tescan':
            base_local_folder = Path(self.settings.value('vega_local_folder'))
        elif record.microscope == 'XL40-GB':
            base_local_folder = Path(self.settings.value('xl40gb_local_folder'))
        elif record.microscope == 'XL40-Cold':
            base_local_folder = Path(self.settings.value('xl40cold_local_folder'))
        else:
            base_local_folder = Path.cwd()

        # we may have already a folder for this experiment. if so it has to start with the protocol ID
        src_path = None
        for elem in base_local_folder.glob('*'):
            if elem.is_dir() and str(elem.name).startswith(record.protocol_id):
                src_path = elem
                break

        # check if by chance there is an experiment file in this folder
        exp_file_list = [str(elem) for elem in src_path.glob('*.exp')]
        if len(exp_file_list) == 1:
            # we got it
            self.setField('exp_filename', str(exp_file_list[0]))
            # upload it to the logbook for the next time
            logbook = self._get_elog_handle()
            msg_id = self.field('msg_id')
            attachments = [str(exp_file_list[0])]
            logbook.post('', msg_id=msg_id, attachments=attachments, encoding='HTML', timeout=self.timeout)
            return
        elif len(exp_file_list) > 1:
            # we got many
            dialog = SelectExperimentDialog(self)
            dialog.load_local_experiment_list(exp_file_list)
            while dialog.exec() != QDialog.Accepted:
                exp_filename = dialog.local_experiment_selector.currentText()
                self.setField('exp_filename', exp_filename)
                logbook = self._get_elog_handle()
                msg_id = self.field('msg_id')
                attachments = [exp_filename]
                logbook.post('', msg_id=msg_id, attachments=attachments, encoding='HTML', timeout=self.timeout)
                return

        project_name = 'project'
        if src_path:
            # src_path may contain the project name in the form of
            # protocolID - projectName - projectResponsible
            folder_name = src_path.parts[-1]
            pattern = '^([\\d]+)\\s*[-_]\\s*([\\w\\W]+)\\s*[-_]\\s*([\\w\\W]+)$'
            match = re.search(pattern, folder_name)
            if match:
                project_name = match[2]
        else:
            # we could not find any folder.
            # then we create a new one
            src_path = base_local_folder / Path('-'.join([str(record.protocol_id),
                                                          project_name,
                                                          record.requesting_user]))
            src_path.mkdir(parents=True, exist_ok=True)

        mirror_path = None
        year = Path(f'20{str(record.protocol_id)[:2]}')
        # check if the network folder contains the year as last level
        base_network_folder = Path(self.settings.value('network_folder'))
        last_folder = str(base_network_folder.parts[-1])
        pattern = '^[0-9]{4}$'
        if re.search(pattern, last_folder):
            # the base network folder contains already the year
            base_network_folder = base_network_folder.parent

        # append the protocol year
        base_network_folder = base_network_folder / year
        for elem in base_network_folder.glob('*'):
            if elem.is_dir() and str(elem.name).startswith(record.protocol_id):
                mirror_path = elem

        if mirror_path is None:
            # we could not find a folder for this protocol. very strange but still possible.
            # we have to create it
            mirror_path = base_network_folder / Path('-'.join([str(record.protocol_id),
                                                               project_name,
                                                               record.requesting_user]))
            mirror_path.mkdir(parents=True, exist_ok=True)
        else:
            # we found a folder, so maybe we have an experiment file in there.
            exp_file_list = [str(elem) for elem in mirror_path.glob('*.exp')]
            if len(exp_file_list) == 1:
                # here you have it
                self.setField('exp_filename', str(exp_file_list[0]))
                # upload it to the logbook for the next time
                logbook = self._get_elog_handle()
                msg_id = self.field('msg_id')
                attachments = [str(exp_file_list[0])]
                logbook.post('', msg_id=msg_id, attachments=attachments, encoding='HTML', timeout=self.timeout)
                return
            elif len(exp_file_list) > 1:
                # we got many
                dialog = SelectExperimentDialog(self)
                dialog.load_local_experiment_list(exp_file_list)
                while dialog.exec() != QDialog.Accepted:
                    exp_filename = dialog.local_experiment_selector.currentText()
                    self.setField('exp_filename', exp_filename)
                    logbook = self._get_elog_handle()
                    msg_id = self.field('msg_id')
                    attachments = [exp_filename]
                    logbook.post('', msg_id=msg_id, attachments=attachments, encoding='HTML', timeout=self.timeout)
                    return

        # bad luck, we could not find any experiment file anywhere. so we have to generate it as last chance.
        configuration = generate_default_conf()
        configuration['GUI'] = {
            'src_path': str(src_path),
            'mirror_path': str(mirror_path),
            'mirror': True,
            'microscope': microscope_lut[record.microscope],
            'custom_ownership': True,
            'projectID': record.protocol_id,
            'project_name': project_name,
            'responsible': record.requesting_user,
        }

        configuration['elog']['elog_user'] = self.settings.value('elog_user_name')
        configuration['elog']['elog_password'] = self.settings.value('elog_password')
        configuration['elog']['elog_hostname'] = self.settings.value('elog_hostname')
        configuration['elog']['elog_port'] = str(self.settings.value('elog_port'))
        configuration['elog']['use_ssl'] = str(self.settings.value('elog_use_ssl'))

        experiment_filename = src_path / Path('-'.join([
            str(record.protocol_id),
            project_name,
            record.requesting_user]) + '.exp'
                                              )
        write_conffile(configuration, experiment_filename)
        self.setField('exp_filename', str(experiment_filename))

        logbook = self._get_elog_handle()
        msg_id = self.field('msg_id')
        attachments = [str(experiment_filename)]
        logbook.post('', msg_id=msg_id, attachments=attachments, encoding='HTML', timeout=self.timeout)

        return
