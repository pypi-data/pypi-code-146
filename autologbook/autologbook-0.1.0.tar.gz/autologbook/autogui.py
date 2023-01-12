# -*- coding: utf-8 -*-
#  Copyright (c) 2022.  Antonio Bulgheroni.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
Created on Sat May 21 12:10:26 2022

@author: elog-admin
"""
from __future__ import annotations

import configparser
import ctypes
import logging
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any

import elog
import urllib3
import watchdog.events
import watchdog.observers
import yaml
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import (
    QAbstractItemView,
    QAbstractTableModel,
    QItemSelection,
    QItemSelectionModel,
    QModelIndex,
    QPersistentModelIndex,
    QSortFilterProxyModel,
    QStandardItem,
    QStandardItemModel,
)
from PyQt5.QtCore import QEvent, QObject, QPoint, QRegExp, Qt, QTimer, QUrl
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QLinearGradient, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QFileDialog,
    QHeaderView,
    QMainWindow,
    QMenu,
    QMessageBox,
    QShortcut,
)
from elog.logbook_exceptions import LogbookServerTimeout
from tenacity import after_log, retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from yaml.representer import SafeRepresenter

from autologbook.autoprotocol import HTMLHelperMixin
from autologbook import autoconfig, autoerror, autoprotocol, autotools, autowatchdog
from autologbook.about_dialog_ui import Ui_About
from autologbook.autotools import (
    CustomEditVisibilityFlag,
    ElementType,
    ElementTypeVisitiliyFlag,
    FSCommandType,
    MetadataVisibilityFlag,
    ReadOnlyDecision,
    UserRole,
    VisibilityFlag,
)
from autologbook.change_sample_dialog_ui import Ui_ChangeSampleDialog
from autologbook.configuration_editor_ui import Ui_configurationDialog
from autologbook.edit_lock_dialog_ui import Ui_OverwriteEntryDialog
from autologbook.main_window_ui import Ui_MainWindow
from autologbook.protocol_editor_ui import Ui_tree_viewer_dialog
from autologbook.rename_dialog_ui import Ui_RenameDialog
from autologbook.restore_element import RecoverElementDialog
from autologbook.user_editor_ui import Ui_UserEditor

Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot
urllib3.disable_warnings()
represent_literal_str = autotools.change_style(
    '|', SafeRepresenter.represent_str)
yaml.add_representer(autotools.literal_str, represent_literal_str)
log = logging.getLogger('__main__')


class PathValidator:
    """
    Helper class to validate the input paths.

    Use it to validate the input folder fields to decide
    if the watchdog can be started or not.

    """

    # TODO: consider the possibility to replace the validity constants with
    # a flag enumerator.
    Invalid = 0
    AcceptableIfMirroringActive = 10
    AcceptableIfCustomOwnership = 20
    Acceptable = 30

    def __init__(self, path: str | Path, base_path='R:\\A226\\Results',
                 pattern='^([\\d]+)\\s*[-_]\\s*([\\w\\W]+)\\s*[-_]\\s*([\\w\\W]+)$'):
        r"""
        Build an instance of the PathValidator.

        You won't use it because you should use the static class function ValidatePath

        Note: traditionally Versa paths are starting with a # symbol. While this is perfectly
              ok with the filesystem, when the path is converted to a URI on the image file server
              the # symbol is causing problems. The webserver will consider it as the starting
              point of a URL fragment and not part of the URL itself.
              **We cannot accept # symbols in protocol folder on the Image Server!**

        Parameters
        ----------
        path : Path | str
            This is the path that is being validated.
        base_path : Path | str, optional
            This is the base path where all the protocols should be saved.
            The default is 'R:\\A226\\Results'.
        pattern : str, optional
            This is the pattern that the leaf folder should match.
            It should be something like this:
                1234 - ProjectName - ProjectResponsible
            The default is '^([\d]+)\s*[-_]\s*([\w\W]+)\s*[-_]\s*([\w\W]+)$'.

        Returns
        -------
        None.

        """
        self.path = path
        self.base_path = Path(base_path)
        self.pattern = pattern

    def get_ownership_parameters(self):
        """
        Retrieve the ownership parameters from the folder name.

        Using the pattern provided in the constructor, try to guess the three
        ownership parameters. If it fails, None is returned.

        Returns
        -------
        int or str
            The project ID
        str
            The project name
        str
            The responsible..

        """
        if self.path == '':
            return None
        self.path = Path(self.path)
        folder_name = self.path.parts[-1]
        match = re.search(self.pattern, folder_name)
        if match:
            return match[1], match[2], match[3]
        return None

    def validate(self):
        """
        Validate the path.

        This class member can return three possible state:
            1. Invalid. The provided path is invalid and thus the watchdog cannot be start
            2. AcceptableIfMirroringActive. The provided path is not invalid and the watchdog
               can be started if the mirroring is activated and the mirroring folder is Acceptable
            3. Acceptable. The provided path is valid in all cases.

        There are several checks that need to be done:
            1. The path is empty or not existing, or not a directory, then Invalid is returned.
            2. The path is not relative to the base_path, then AcceptableIfMirroringActive is returned.
            3. The path is relative to the base_path, but the leaf directory is not matching the regular
               expression, then AccetableIfMirroringActive is returned.
            4. the path is starting with # symbol (traditional Versa folder), then
               AcceptableIfMirroringActive is returned
            5. The path is relative to the base_path and the leaf directory is matching the regular
               expression then Acceptable is returned.

        Returns
        -------
        VALIDITY Constant
            See the description for an explanation.

        """
        if not self.path:
            return self.Invalid
        self.path = Path(self.path)

        if len(str(self.path)) == 0:
            return self.Invalid
        if self.path.exists() and self.path.is_dir():
            if '#' in str(self.path):
                # found a # symbol in the path. Very likely this is a Versa folder.
                # the folder can be accepted only if it is mirrored somewhere else.
                return self.AcceptableIfMirroringActive
            if self.path.is_relative_to(autoconfig.IMAGE_SERVER_BASE_PATH):
                # the path is in the right position.
                # let's check if the ownership variables are in the folder name
                folder_name = self.path.parts[-1]
                match = re.search(self.pattern, folder_name)
                if match:
                    # very good, we are all set
                    return self.Acceptable
                else:
                    # we need to ask the user to use custom ownership variables
                    return self.AcceptableIfCustomOwnership
            return self.AcceptableIfMirroringActive
        return self.Invalid


def validate_path(path: str | Path, base_path: str | Path = 'R:\\A226\\Results',
                  pattern: str | re.Pattern = '^*([\\d]+)\\s*[-_]\\s*([\\w\\W]+)\\s*[-_]\\s*([\\w\\W]+)$') -> int:
    """Return the validity of a path."""
    return PathValidator(path, base_path, pattern).validate()


class Signaller(QtCore.QObject):
    """
    A subclass of QObject to contain a signal.

    Only QObejct derived instances are allowed to have a signal, so if you want to have a no
    QtObject to emit a signal, you have to add a Signaller like this to its attributes.

    This specific signaller contains only one Qt Signal emitting a formatted string a logging.LogRecord
    and it is used to establish a communication between the logging module and a PlainText object in a
    QtWindow.

    """

    signal = Signal(str, logging.LogRecord)


class QtHandler(logging.Handler):
    """
    A subclass of the logging.Handler.

    It incorporates a Signaller to be able to emit a Qt Signal.

    """

    def __init__(self, slotfunc, *args, **kwargs):
        """
        Build an instance of QtHandler.

        Parameters
        ----------
        slotfunc : CALLABLE
            The slot function which the Signaller.signal is connected.
        *args : positional arguments
            All other positional arguments to be passed to the parent constructor.
        **kwargs : keyword arguments
            All keywork arguments to be passed to the parent constructor.

        Returns
        -------
        None.

        """
        super().__init__(*args, **kwargs)
        self.signaller = Signaller()
        self.signaller.signal.connect(slotfunc)

    def emit(self, record):
        """Emit the signaller signal containing the formatted string and the logging.Record."""
        s = self.format(record)
        self.signaller.signal.emit(s, record)


class Worker(QtCore.QObject):
    """
    A Worker class derived from QObject.

    This class will be performing the real job.
    It will be moved to a separate Thread in order to leave the original thread responsible only of the user interface.

    """

    # signal informing about the worker running status
    worker_is_running = Signal(bool, name='work_is_running')

    def __init__(self, parent=None):
        """
        Build an instance of a generic worker.

        It sets its parent and call the super constructor

        Parameters
        ----------
        parent : Object, optional
            The parent object.

        Returns
        -------
        None.

        """
        self.parent = parent

        self.running = False

        # a list with the required parameters
        self.required_parameters = []

        # a dictionary with the actual parameters
        self.params = {}

        super().__init__(parent=parent)

    def update_parameters(self, *args, **kwargs):
        """
        Transfer the execution parameters from the GUI to the worker Thread.

        All keyword arguments are already provided in the code but can be overridden here

        Keyword arguments
        ------------------

        elog_hostname: STRING
            The FQDN of the elog server including the protocol. For example https://10 .166.16.24

        elog_port: INTEGER
            The numeric value of the port where there elog server is listening.

        elog_user: STRING
            The username connecting to the logbook.

        elog_password: STRING
            The password to connect to the logbook in plain text

        Returns
        -------
        None.

        """
        # check if all required parameters are transmitted
        for param in self.required_parameters:
            if param in kwargs:
                self.params[param] = kwargs[param]
            else:
                log.error('Missing %s. Cannot update worker parameters' % param)
                raise autoerror.MissingWorkerParameter(f'Missing {param}.')

    @Slot()
    def toggle(self):
        """
        Toggle the status of the watchdog.

        The watchdog pushbutton on the GUI should have a toggle mechanical
        function instead of a pushbutton one.

        Using this slot we are mimicking the same mechanical behaviour.

        This is actually the only slot that should be connected to the GUIThread
        receiving the start/stop signal.

        Returns
        -------
        None.

        """
        if self.running:
            self.running = False
            self.stop()
        else:
            self.running = True
            self.start()


class SingleWatchdogWorker(Worker):
    """
    Specialized worker taking care of mirroring and logbook generation.

    The mirroring function is only optional.
    """

    def __init__(self, parent=None):
        """
        Build an instance of a FSWatchdogWorker.

        Parameters
        ----------
        parent : Object, optional
            The parent object. The default is None.
            In normal circumstances this is the Main Window

        Returns
        -------
        None.
        """

        # call the worker init
        super().__init__(parent=parent)

        # list of required parameters
        self.required_parameters.extend([
            'original_path',  # this the where the microscope software is saving the images.
            'destination_path',  # this is where the mirroring component has to copy the files
            'is_mirroring_requested',  # a flag to specify whether the mirroring is required or not
            'microscope',  # this is the microscope type
            'projectID',  # this is the project ID aka protocol number
            'project_name',  # this is the project name
            'responsible'  # this is the project responsible
        ])

        # this is the reference to the protocol instance
        self.autoprotocol_instance = None

        # this is the reference to the event handler
        self.autologbook_event_handler = None

        # this is the reference to the watchdog observer
        self.watchdog_observer = None

    def update_parameters(self, *args, **kwargs):
        """
        Transfer the execution parameters from the GUI to the SingleWatchdogWorker.

        Keywords parameter
        ------------------
        original_path : Path-like or string
            The source path of the mirroring

        destination_path : Path-like or string
            The destination path of the mirroring

        is_mirroring_requested : Bool
            A boolean flag to ask for mirroring or not

        microscope : string
            The name of the microscope. This will affect the subclass of ELOGProtocol and
            ELOGProtocolEventHandler. Possible values are:
                Quattro : for the Thermofisher Quattro S.
                Versa : for the Thermofisher Versa 3D FIB
                Vega : for the Tescan VEGA
                XL40-Cold and XL40-GB: for the Philips XL40 family
        projectID : string or None
            The customized protocol ID. Use None if you want to have it guessed from the
            folder name.

        project_name : string or None
            The project name for the protocol. Use None if you want to have it guessed from the
            folder name.

        responsible : string or None
            The name of the responsible for the experiment. Use None if you want to have it guessed from the
            folder name.

        Those parameters are sent to the worker everytime the enable_watchdog is set,
        and this is happening if and only if the validate_inputs is returning true

        Raises:
        -------
        MissingWorkerParameter if a parameter is missing in the kwargs.

        Returns
        -------
        None.

        """
        # call the super method
        # the super method will loop over all required parameters and transfer their
        # value from the kwargs to the params dictionary.
        super().update_parameters(*args, **kwargs)

        # if mirroring is requested we need to apply a trick to have the right folder where the yaml_filename is-
        if self.params['is_mirroring_requested']:
            where = 'original_path'
        else:
            where = 'destination_path'

        if self.params['projectID'] is None:
            # if the projectID is None, it means that it will be guessed afterwards, but we have to do it now for the
            # yaml_filename
            folder = self.params['destination_path'].parts[-1]
            pattern = '^#*([\\d]+)\\s*[-_]\\s*([\\w\\W]+)\\s*[-_]\\s*([\\w\\W]+)$'
            match = re.search(pattern, folder)
            if match:
                project_id = match.group(1)
            else:
                project_id = 'unknown'
        else:
            project_id = self.params['projectID']

        yaml_filename = self.params[where] / Path(f'protocol-{project_id}.yaml')

        # now let's prepare what is needed.
        # first the autoprotocol_instance. This depends on the type of microscope:
        if self.params['microscope'] == 'Quattro':
            self.autoprotocol_instance = autoprotocol.QuattroELOGProtocol(
                path=self.params['destination_path'],  # REMEMBER: the destination_path is on the image server
                elog_hostname=autoconfig.ELOG_HOSTNAME,
                elog_port=autoconfig.ELOG_PORT,
                elog_user=autoconfig.ELOG_USER,
                elog_password=autoconfig.ELOG_PASSWORD,
                elog_use_ssl=autoconfig.USE_SSL,
                protocol=self.params['projectID'],
                project=self.params['project_name'],
                responsible=self.params['responsible'],
                yaml_filename=yaml_filename
            )

            self.autologbook_event_handler = autowatchdog.QuattroELOGProtocolEventHandler(
                autoprotocol_instance=self.autoprotocol_instance, **self.params)

        elif self.params['microscope'] == 'Versa':
            self.autoprotocol_instance = autoprotocol.VersaELOGProtocol(
                path=self.params['destination_path'],  # REMEMBER: the destination_path is on the image server
                elog_hostname=autoconfig.ELOG_HOSTNAME,
                elog_port=autoconfig.ELOG_PORT,
                elog_user=autoconfig.ELOG_USER,
                elog_password=autoconfig.ELOG_PASSWORD,
                elog_use_ssl=autoconfig.USE_SSL,
                protocol=self.params['projectID'],
                project=self.params['project_name'],
                responsible=self.params['responsible'],
                yaml_filename=yaml_filename
            )

            self.autologbook_event_handler = autowatchdog.VersaELOGProtocolEventHandler(
                autoprotocol_instance=self.autoprotocol_instance, **self.params)

        elif self.params['microscope'] == 'Vega':
            self.autoprotocol_instance = autoprotocol.VegaELOGProtocol(
                path=self.params['destination_path'],  # REMEMBER: the destination_path is on the image server
                elog_hostname=autoconfig.ELOG_HOSTNAME,
                elog_port=autoconfig.ELOG_PORT,
                elog_user=autoconfig.ELOG_USER,
                elog_password=autoconfig.ELOG_PASSWORD,
                elog_use_ssl=autoconfig.USE_SSL,
                protocol=self.params['projectID'],
                project=self.params['project_name'],
                responsible=self.params['responsible'],
                yaml_filename=yaml_filename
            )

            self.autologbook_event_handler = autowatchdog.VegaELOGProtocolEventHandler(
                autoprotocol_instance=self.autoprotocol_instance, **self.params)

        elif self.params['microscope'] in ['XL40-GB', 'XL40-Cold']:

            if self.params['microscope'] == 'XL40-GB':
                logbook = autoconfig.XL40GB_LOGBOOK
            else:
                logbook = autoconfig.XL40COLD_LOGBOOK

            self.autoprotocol_instance = autoprotocol.XL40ELOGProtocol(
                path=self.params['destination_path'],  # REMEMBER: the destination_path is on the image server
                elog_hostname=autoconfig.ELOG_HOSTNAME,
                elog_port=autoconfig.ELOG_PORT,
                elog_user=autoconfig.ELOG_USER,
                elog_password=autoconfig.ELOG_PASSWORD,
                elog_use_ssl=autoconfig.USE_SSL,
                elog_logbook=logbook,
                protocol=self.params['projectID'],
                project=self.params['project_name'],
                responsible=self.params['responsible'],
                yaml_filename=yaml_filename
            )

            self.autologbook_event_handler = autowatchdog.XL40ELOGProtocolEventHandler(
                autoprotocol_instance=self.autoprotocol_instance, **self.params)

        # connect the autoprocol_instance signal_dispatcher to the main window proxy signals
        self.autoprotocol_instance.signal_dispatcher.added_element.connect(
            self.parent.added_element.emit)
        self.autoprotocol_instance.signal_dispatcher.removed_element.connect(
            self.parent.removed_element.emit)
        # we are ready to start. Just wait the start signal!

    @Slot()
    def start(self):
        """
        Start the SingleWatchdogWorker.

        A new Observer instance is generated everytime this slot is called,
        scheduled to work with an autologbookEventHandler and started.

        All the already existing items in the monitored path are also processed.

        IMPORTANT NOTE
        --------------
        Never call this slot directly, but always pass via the toggle slot to
        transform the start watchdog push button in a start/stop toggle switch.

        Returns
        -------
        None.

        """
        # inform the GUI that we have started working
        self.worker_is_running.emit(True)

        # rename the thread
        threading.current_thread().name = autotools.ctname()
        log.info('Starting protocol watchdog')

        # it's time to have an observer. It is important that a fresh observer is
        # created every time the worker is started, because otherwise the observer
        # won't be able to restart.
        self.watchdog_observer = watchdog.observers.Observer(autoconfig.AUTOLOGBOOK_WATCHDOG_TIMEOUT)
        self.watchdog_observer.schedule(self.autologbook_event_handler,
                                        path=self.params['original_path'], recursive=True)

        # get a reference of the observer.event_queue attached to the handler.
        # it is useful for advance operations.
        self.autologbook_event_handler.set_queue_reference(self.watchdog_observer.event_queue)
        # Append Obs to the thread name
        self.watchdog_observer.name = f'{autotools.ctname()}Obs'

        # remember to reset the MicroscopePicture IDs
        autoprotocol.MicroscopePicture._reset_ids()

        # reset the protocol content. this is useful if we are just restarting a watchdog
        # without having changed any worker parameters. After that emit the reset content signal
        # from the MainWindow so that the ProtocolEditor will refresh its view.
        self.autoprotocol_instance.clear_resettable_content()
        self.parent.reset_content.emit()

        # process existing items
        self.autologbook_event_handler.process_already_existing_items()

        # now start to look for new files
        self.watchdog_observer.start()

        # this will start the observer thread and also one or more event emitter threads.
        # for the sake of clarity, I'm renaming the emitter threads to something more
        # understandable
        for count, emitter in enumerate(list(self.watchdog_observer.emitters)):
            emitter.name = f'{autotools.ctname()}Emi{count}'

    @Slot()
    def stop(self):
        """
        Stop the SingleWatchdog.

        A stop signal is sent to the observer so that is not queuing any more
        events.

        The join statement assures that all currently present event in the queue
        are still dispatched.

        The HTML content of the autologbook is generated for the last time and
        since the queue is empty it will also be posted to the ELOG server this
        time with all attachments.

        Finally, a signal is sent back to the GUIThread to inform it that the
        watchdog process is finished and the status of the inputs can be changed.

        IMPORTANT NOTE
        --------------
        Never call this slot directly, but always pass via the toggle slot to
        transform the start watchdog push button in a start/stop toggle switch.

        Returns
        -------
        None.

        """
        # stop the observer
        self.watchdog_observer.stop()

        # wait until the observer is finished
        self.watchdog_observer.join()

        # for the last time generate the HTML and post it with all the attachments
        self.autoprotocol_instance.post_elog_message(skip_attachments=False)

        # inform the GUI that we have finished our task.
        self.worker_is_running.emit(False)


class AboutDialog(QDialog, Ui_About):
    """
    About Autolog Dialog.

    A very simple dialog message without button to show information about this
    program.
    """

    def __init__(self, parent=None):
        """
        Build an instance of the AboutDialog.

        Parameters
        ----------
        parent : QtObject, optional
            The parent calling QtObject. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(parent)
        self.setupUi(self)


class ConfigurationEditorDialog(QDialog, Ui_configurationDialog):
    """
    A complete configuration editor dialog.

    This dialog window allows the user to manipulate all configuration
    parameters.

    The user can load a file, save the current configuration to a file or
    reset to the default configuration.

    """

    def __init__(self, parent=None):
        """
        Build an instance of the ConfigurationEditorDialog.

        Parameters
        ----------
        parent : QtObject, optional
            The parent caller of this dialog. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)

        # we need to fill in the microscope combolist
        for i in range(self.parent.select_microscope_comboBox.model().rowCount()):
            self.default_microscope_combo.addItem(self.parent.select_microscope_comboBox.model().item(i).text())

        # use this boolean to check if the password was changed during the
        # configuration editing.
        self.password_changed = False

        # use this string to store the encrypted password
        self.encrypted_pwd = ''

    @Slot(str)
    def password_edited(self, new_plain_text_pwd):
        """
        React to a password change.

        When the user edits the password, he is introducing a plain text string.
        This will never be saved in the configuration file nor in the configuration
        object.

        This slot is automatically invoked whenever the password field is edited,
        the new encrypted password is calculated and a flag to signalize that the
        password must be updated is raised.

        Parameters
        ----------
        new_plain_text_pwd : string
            The new plain text password.

        Returns
        -------
        None.

        """
        self.password_changed = True
        self.encrypted_pwd = autotools.encrypt_pass(new_plain_text_pwd)

    def set_all_values(self, config):
        """
        Set the values of all widgets to what is stored in the configuration object.

        The coding style of this method is terrible, I will look for something
        better.

        Parameters
        ----------
        config : ConfigParser object
            The configuration parser object containing all the parameters.

        Returns
        -------
        None.

        """
        # elog
        self.elog_user_field.setText(config['elog'].get('elog_user'))
        self.elog_password_field.setText(config['elog'].get('elog_password'))
        self.elog_hostname_field.setText(config['elog'].get('elog_hostname'))
        self.elog_port_field.setValue(int(config['elog'].get('elog_port')))
        self.elog_max_auth_error_field.setValue(int(config['elog'].get('max_auth_error')))
        self.elog_ssl_check_box.setChecked(config.getboolean('elog', 'use_ssl'))
        self.elog_timeout_spinbox.setValue(config.getfloat('elog', 'elog_timeout'))
        self.attempts_on_timeout_spinbox.setValue(config.getint('elog', 'elog_timeout_max_retry'))
        self.waiting_time_between_timeout_attempts_spingbox.setValue(config.getfloat('elog', 'elog_timeout_wait'))
        self.microscopy_protocol_list.setText(config.get('elog', 'microscopy_protocol_list'))

        # autolog
        self.autologbook_max_attempts_spinbox.setValue(int(config['Autologbook watchdog'].get('max_attempts')))
        self.autologbook_wait_min_spinbox.setValue(float(config['Autologbook watchdog'].get('wait_min')))
        self.autologbook_wait_max_spinbox.setValue(float(config['Autologbook watchdog'].get('wait_max')))
        self.autologbook_wait_increment_spinbox.setValue(float(config['Autologbook watchdog'].get('wait_increment')))
        self.autologbook_min_delay_spinbox.setValue(
            float(config['Autologbook watchdog'].get('minimum delay between elog post')))
        self.autologbook_observer_timeout_spinbox.setValue(config.getfloat('Autologbook watchdog', 'observer_timeout'))

        # mirroring
        self.mirroring_max_attempts_spinbox.setValue(int(config['Mirroring watchdog'].get('max_attempts')))
        self.mirroring_wait_spinbox.setValue(float(config['Mirroring watchdog'].get('wait')))
        self.mirroring_observer_timeout_spinbox.setValue(config.getfloat('Mirroring watchdog', 'observer_timeout'))

        # quattro
        self.quattro_elog_logbook_field.setText(config['Quattro'].get('logbook'))
        self.quattro_navcam_size_spinbox.setValue(int(config['Quattro'].get('image_navcam_width')))

        # versa
        self.versa_elog_logbook_field.setText(config['Versa'].get('logbook'))

        # vega
        self.vega_elog_logbook_field.setText(config['Vega'].get('logbook'))
        self.vega_auto_calibrated_checkbok.setChecked(config.getboolean('Vega', 'auto_calibration'))

        # xl40
        self.xl40_auto_calibrated_checkbok.setChecked(config.getboolean('XL40', 'auto_calibration'))
        self.xl40cold_elog_logbook_field.setText(config['XL40-Cold'].get('logbook'))
        self.xl40gb_elog_logbook_field.setText(config['XL40-GB'].get('logbook'))

        # image server
        self.base_path_field.setText(config['Image_server'].get('base_path'))
        self.server_root_field.setText(config['Image_server'].get('server_root'))
        self.img_thumb_size_spinbox.setValue(int(config['Image_server'].get('image_thumb_width')))
        self.custom_id_start_spinBox.setValue(config.getint('Image_server', 'custom_id_start'))
        self.custom_id_tiff_tag_spinBok.setValue(config.getint('Image_server', 'tiff_tag_code'))
        self.fei_auto_calibrated_checkbok.setChecked(config.getboolean('FEI', 'auto_calibration'))
        self.fei_crop_databar_checkbok.setChecked(config.getboolean('FEI', 'databar_removal'))

        # GUI default
        self.default_microscope_combo.setCurrentText(config.get('GUI_DEFAULT', 'default_microscope'))
        self.default_protocol_folder.setText(config.get('GUI_DEFAULT', 'default_protocol_folder'))
        self.default_mirroring_folder.setText(config.get('GUI_DEFAULT', 'default_mirroring_folder'))

        # be sure that the software is informed that the password has not been changed yet.
        self.password_changed = False

    def get_conf(self):
        """
        Get a configuration object from the value in the dialog.

        A configuration parser object is created with all the sections and all
        the options set to the values in the dialog.

        Returns
        -------
        config : ConfigParser
            A ConfigParser containing the options contained in the dialog.

        """
        config = configparser.ConfigParser()
        if self.password_changed:
            new_password = self.encrypted_pwd
        else:
            new_password = self.elog_password_field.text()
        config['elog'] = {
            'elog_user': self.elog_user_field.text(),
            'elog_password': new_password,
            'elog_hostname': self.elog_hostname_field.text(),
            'elog_port': str(self.elog_port_field.value()),
            'use_encrypt_pwd': True,
            'max_auth_error': self.elog_max_auth_error_field.value(),
            'use_ssl': self.elog_ssl_check_box.isChecked(),
            'elog_timeout': str(self.elog_timeout_spinbox.value()),
            'elog_timeout_max_retry': str(self.attempts_on_timeout_spinbox.value()),
            'elog_timeout_wait': str(self.waiting_time_between_timeout_attempts_spingbox.value()),
            'microscopy_protocol_list': str(self.microscopy_protocol_list.text()),
        }
        config['Autologbook watchdog'] = {
            'max_attempts': str(self.autologbook_max_attempts_spinbox.value()),
            'wait_min': str(self.autologbook_wait_min_spinbox.value()),
            'wait_max': str(self.autologbook_wait_max_spinbox.value()),
            'wait_increment': str(self.autologbook_wait_increment_spinbox.value()),
            'minimum delay between elog post': str(self.autologbook_min_delay_spinbox.value()),
            'observer_timeout': self.autologbook_observer_timeout_spinbox.value()
        }
        config['Mirroring watchdog'] = {
            'max_attempts': str(self.mirroring_max_attempts_spinbox.value()),
            'wait': str(self.mirroring_wait_spinbox.value()),
            'observer_timeout': self.mirroring_observer_timeout_spinbox.value()
        }
        config['Quattro'] = {
            'logbook': self.quattro_elog_logbook_field.text(),
            'image_navcam_width': self.quattro_navcam_size_spinbox.value()
        }
        config['Versa'] = {
            'logbook': self.versa_elog_logbook_field.text()
        }
        config['Image_server'] = {
            'base_path': str(Path(self.base_path_field.text())),
            'server_root': self.server_root_field.text(),
            'image_thumb_width': self.img_thumb_size_spinbox.value(),
            'custom_id_start': self.custom_id_start_spinBox.value(),
            'tiff_tag_code': self.custom_id_tiff_tag_spinBok.value()
        }
        config['FEI'] = {
            'auto_calibration': self.fei_auto_calibrated_checkbok.isChecked(),
            'databar_removal': self.fei_crop_databar_checkbok.isChecked()
        }
        config['Vega'] = {
            'auto_calibration': self.vega_auto_calibrated_checkbok.isChecked(),
            'logbook': self.vega_elog_logbook_field.text()
        }
        config['XL40'] = {
            'auto_calibration': self.xl40_auto_calibrated_checkbok.isChecked(),
        }
        config['XL40-GB'] = {
            'logbook': self.xl40gb_elog_logbook_field.text(),
        }
        config['XL40-Cold'] = {
            'logbook': self.xl40cold_elog_logbook_field.text(),
        }
        config['GUI_DEFAULT'] = {
            'default_microscope': self.default_microscope_combo.currentText(),
            'default_protocol_folder': str(Path(self.default_protocol_folder.text())),
            'default_mirroring_folder': str(Path(self.default_mirroring_folder.text())),
        }
        self.password_changed = False
        return config

    @Slot()
    def save_conf_file(self):
        """
        Save the configuration from the dialog to a file.

        This slot is connected with Save configuration push button.

        Returns
        -------
        None.

        """
        directory = Path.home() / Path('Documents')
        conffile = QFileDialog.getSaveFileName(self, 'Save configuration file', directory=str(directory),
                                               filter='Configuration file (*.ini)')
        if conffile[0]:
            autotools.write_conffile(self.get_conf(), conffile[0])

    @Slot()
    def load_conf_file(self):
        """
        Load a configuration file to the dialog.

        This slot is connected to the load file pushbutton.

        Returns
        -------
        None.

        """
        directory = Path.home() / Path('Documents')
        conffile = QFileDialog.getOpenFileName(self, 'Open configuration file', directory=str(directory),
                                               filter='Configuration file (*.ini)')
        if conffile[0]:
            conf = autotools.safe_configread(conffile[0])
            self.set_all_values(conf)

    @Slot()
    def reset_conf(self):
        """
        Reset the content of the dialog to the default.

        This slot is connected to the reset default pushbutton.

        Returns
        -------
        None.

        """
        self.set_all_values(autotools.generate_default_conf())

    @Slot()
    def search_basepath(self):
        """
        Search for the base path of the image server.

        This slot is connected to the tool button next to base folder input.

        Returns
        -------
        None.

        """
        if self.base_path_field:
            directory = Path(self.base_path_field.text())
        else:
            directory = Path.home() / Path('Documents')
        returnpath = QFileDialog.getExistingDirectory(self, 'Select base path of image server',
                                                      directory=str(directory))
        if returnpath:
            self.base_path_field.setText(returnpath)


class ReadOnlyEntryDialog(QDialog, Ui_OverwriteEntryDialog):
    """Dialog window to decide how to handle read-only entries."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.decision = ReadOnlyDecision.Edit

    def set_message(self, protocol_id):
        """
        Update the message of the dialog window using the current protocol_id.

        Parameters
        ----------
        protocol_id : string
            The current protocol ID number.

        Returns
        -------
        None.

        """
        msg = (f'<html><head/><body><p>On the elog server, an entry corresponding to the protocol number {protocol_id} '
               'already exists and it is<span style=" font-weight:600;"> read-only</span>.'
               '</p><p>In order to continue, '
               'you have to select one of the following three options.'
               '</p><ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px;'
               ' -qt-list-indent: 1;">'
               '<li style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px;'
               '-qt-block-indent:0; text-indent:0px;">'
               'Force overwrite the read-only entry (<span style=" font-weight:600;">Force overwrite</span>)</li>'
               '<li style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px;'
               ' -qt-block-indent:0; text-indent:0px;">'
               'Make a backup of the read-only entry modifying its protocol ID (<span style=" font-weight:600;">'
               'Backup read-only entry</span>)</li><li style=" margin-top:12px; margin-bottom:12px; margin-left:0px; '
               'margin-right:0px; -qt-block-indent:0; text-indent:0px;">Change the protocol ID of'
               ' the current experiment'
               'manually (<span style=" font-weight:600;">Edit manually</span>)</li></ul></body></html>')
        self.label.setText(msg)

    @Slot()
    def force_overwrite_selected(self):
        """
        Set decision to ReadOnlyDecision.Overwrite.

        Returns
        -------
        None.

        """
        self.decision = ReadOnlyDecision.Overwrite
        self.done(self.decision)

    @Slot()
    def backup_readonly_selected(self):
        """
        Set decision to ReadOnlyDecision.Backup.

        Returns
        -------
        None.

        """
        self.decision = ReadOnlyDecision.Backup
        self.done(self.decision)

    @Slot()
    def cancel_selected(self):
        """
        Set decision to ReadOnlyDecision.Edit.

        Returns
        -------
        None.

        """
        self.decision = ReadOnlyDecision.Edit
        self.done(self.decision)


class TreeViewerProxyModel(QSortFilterProxyModel):
    """
    A subclass of the QSortFilterProxyModel adapted to the autolog tree browser.

    This class is reimplementing the filtering and sorting methods.
    """

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        Select which model row should be accepted when filtering.

        The proxy model has to have the recursive filtering property set to True because we want to have the
        filtering applied to recursively for each level in the hierarchical model.

        The selection is made using a FixedString regular expression.
        The following data fields are tested for matching:
        1. item name (Qt.DisplayRole)
        2. Caption (UserRole.CAPTION)
        3. Description (UserRole.DESCRIPTION)
        4. Extra (UserRole.EXTRA)

        Parameters
        ----------
        source_row: int
            The row being analyzed for filtering.
        source_parent: QModelIndex
            The parent index of the source_row

        Returns
        -------
        bool:
            True if the row has to be accepted.
        """
        proxy_index = self.sourceModel().index(source_row, 0, source_parent)
        item_name = self.sourceModel().data(proxy_index)
        interesting_fields = [
            item_name,
            self.sourceModel().data(proxy_index, UserRole.CAPTION),
            self.sourceModel().data(proxy_index, UserRole.DESCRIPTION),
            self.sourceModel().data(proxy_index, UserRole.EXTRA)
        ]
        test_results = list()
        for element in interesting_fields:
            if self.filterRegExp().indexIn(element) < 0:
                test_results.append(False)
            else:
                test_results.append(True)
        return any(test_results)

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        """
        Implement the sorting method for the proxy model.

        The hierarchical model is sorted level by level.

        The top level is made only by SectionItem, those are generated sorted at the model generation and should never
        be moved, but in any case we can rearrange them according to the original order.

        For sections not having children (as Navigation images and Attachments), their items are alphabetically sorted
        based on their names.

        For the Samples sections, it may contain three different type of items: SAMPLE, MICROSCOPE_PIC, VIDEO_FILE.
        The method will sort them in this order:
            1. images in alphabetical order,
            2. videos in alphabetical order,
            3. subsamples in alphabetical order.

        Parameters
        ----------
        left: QModelIndex
            The left model index in the comparison
        right: QModelIndex
            The right model index in the comparison

        Returns
        -------
        bool:
            True if left is less than right.
        """
        # Introduction, Navigation images, Samples, Conclusions, Attachments
        section_dict = {'Introduction': 0, 'Navigation images': 10, 'Optical images': 15,
                        'Samples': 20, 'Conclusion': 30, 'Attachments': 40}
        left_type = self.sourceModel().data(left, UserRole.ITEM_TYPE)
        left_name = self.sourceModel().data(left)
        right_type = self.sourceModel().data(right, UserRole.ITEM_TYPE)
        right_name = self.sourceModel().data(right)

        # sorting the top level made of section items.
        # we keep the original order described in the section_dict
        if left_type == ElementType.SECTION:
            if right_type == ElementType.SECTION:
                return section_dict[left_name] < section_dict[right_name]
            else:
                return True  # the section is always coming before than other types

        # sorting inside of single level sections like navigation and attachments
        elif left_type in [ElementType.NAVIGATION_PIC]:
            # the right type should be of the same type.
            return left_name < right_name

        # sorting inside the samples.
        # 1. images in alphabetical order,
        # 2. videos in alphabetical order,
        # 3. optical images in alphabetical order,
        # 4. attachments in alphabetical order,
        # 5. subsamples in alphabetical order.
        elif left_type == ElementType.MICROSCOPE_PIC:
            if right_type in [ElementType.VIDEO_FILE, ElementType.OPTICAL_PIC, ElementType.ATTACHMENT_FILE,
                              ElementType.SAMPLE]:
                return True
            else:  # right type == ElementType.MICROSCOPE_PIC
                return left_name < right_name
        elif left_type == ElementType.VIDEO_FILE:
            if right_type == ElementType.MICROSCOPE_PIC:
                return False
            elif right_type in [ElementType.OPTICAL_PIC, ElementType.ATTACHMENT_FILE, ElementType.SAMPLE]:
                return True
            else:  # right type == ElementType.VIDEO_FILE
                return left_name < right_name
        elif left_type == ElementType.OPTICAL_PIC:
            if right_type in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
                return False
            elif right_type in [ElementType.ATTACHMENT_FILE, ElementType.SAMPLE]:
                return True
            else:  # right type == ElementType.OPTICAL_PIC
                return left_name < right_name

        elif left_type == ElementType.ATTACHMENT_FILE:
            if right_type in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE, ElementType.OPTICAL_PIC]:
                return False
            elif right_type == ElementType.SAMPLE:
                return True
            else:
                return left_name < right_name
        elif left_type == ElementType.SAMPLE:
            if right_type in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE, ElementType.OPTICAL_PIC,
                              ElementType.ATTACHMENT_FILE]:
                return False
            else:  # right type == ElementType.SAMPLE
                return left_name < right_name


class MetadataModel(QAbstractTableModel):
    """
    Derived model to contain metadata from protocol items.
    """

    def __init__(self, metadata: dict | list = None):
        """
        Initialize the model.

        If provided, the metadata dictionary or list is assigned to the model.

        Parameters
        ----------
        metadata: dict | list (optional)
            A dictionary or a list of elements to be assigned to the model.

        """
        super().__init__()
        self.metadata = list()
        if metadata is not None:
            self.set_metadata(metadata)

    def set_metadata(self, metadata: dict | list = None):
        """
        Set the model data.

        The metadata dictionary or list contains all data to be transferred to the model.

        Parameters
        ----------
        metadata: dict | list
            A list of 2-uple or a dictionary of metadata to be assigned to the model.

        Returns
        -------

        """
        self.beginResetModel()
        if isinstance(metadata, list):
            self.metadata = metadata
        elif isinstance(metadata, dict):
            self.metadata = [(key, value) for key, value in metadata.items()]
        else:
            log.error('Only metadata list or dictionaries are accepted.')
        self.endResetModel()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        """
        Set the header data.

        Parameters
        ----------
        section: int
            Column number
        orientation: Qt.Orientation
            Horizontal or vertical headers
        role:
            Qt.DisplayRole
        Returns
        -------
        str:
            The name of the header section.

        """
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return 'Property'
            elif section == 1:
                return 'Value'
            else:
                return
        else:
            return

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        """
        Reimplement the index method.

        Parameters
        ----------
        row: int
            Row number
        column: int
            Column number
        parent: QModelIndex
            parent index

        Returns
        -------
        QModelIndex:
            The model index.
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column, None)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """
        Return the number of rows.

        This corresponds to the number of items in the metadata object.

        Parameters
        ----------
        parent: QModelIndex
            Parent item in the model

        Returns
        -------
        int:
            The number of rows in the model under the parent index.
        """
        return len(self.metadata)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        """
        Return the number of columns

        This is a fixed number (2).

        Parameters
        ----------
        parent: QModelIndex
            Parent item in the model

        Returns
        -------
        int:
            2.
        """
        return 2

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        """
        Reimplement the data method to retrieve data from the model.

        Parameters
        ----------
        index: QModelIndex
            The model index of the item for which the data is requested.
        role:
            The data role. Implemented only Qt.DisplayRole

        Returns
        -------
        str:
            Return the metadata value at index.row and index.column.
        """

        if not index.isValid():
            return
        if role != Qt.DisplayRole:
            return
        return self.metadata[index.row()][index.column()]


class TextItem(QStandardItem):
    """Text item derived from QStandardItem."""

    def __init__(self, txt=''):
        """
        Construct a new TextItem.

        The item_type role is set to Text.

        Parameters
        ----------
        txt : str, optional
            This is the text used as a display role. The default is ''.

        Returns
        -------
        None.
        """
        super().__init__()
        self.setText(txt)
        self.setData(ElementType.TEXT, UserRole.ITEM_TYPE)


class SectionItem(TextItem):
    """
    Section item derived from TextItem.

    This item is used to store section information.

    """

    def __init__(self, txt=''):
        """
        Construct a new SectionItem.

        The item_type role is set to Section.

        Parameters
        ----------
        txt : str, optional
            This is the text used as a display role. The default is ''.

        Returns
        -------
        None.

        """
        super().__init__(txt=txt)
        self.setData(ElementType.SECTION, UserRole.ITEM_TYPE)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : dict
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        key = self.text()
        if key in yaml_dict.keys():
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class AttachmentItem(QStandardItem):
    """
    Attachment item derived from QStandardItem.

    This item is used to store attachments.
    The display name is the attachment filename.

    The attachment key is stored in the data with attachment_path.
    The attachment filename is stored in data the with attachment_file.

    The attachment icon is set using the DecorationRole.

    """

    def __init__(self, attachment_path):
        super().__init__()
        attachment_filename = Path(attachment_path).name
        self.setText(attachment_filename)
        self.setData(ElementType.ATTACHMENT_FILE, UserRole.ITEM_TYPE)
        self.setData(attachment_path, UserRole.ATTACHMENT_PATH)
        self.setData(attachment_filename, UserRole.ATTACHMENT_FILE)
        self.setData(QIcon(':/resources/icons8-attach-48.png'), Qt.DecorationRole)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve custom information for this element from a dictionary

        Parameters
        ----------
        yaml_dict: dict
            The dictionary with the customization information.

        """
        key = self.data(UserRole.ATTACHMENT_PATH)
        if key in yaml_dict.keys():
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class SampleItem(QStandardItem):
    """
    Sample item derived from QStandardItem.

    This item is used to store samples.

    The Display name is the sample_last_name.

    The sample_full_name is stored in the data with the UserRole.SAMPLE_FULL_NAME
    The sample_last_name is stored in the data with the UserRole.SAMPLE_LAST_NAME

    The FontRole is set to the current font but bold.
    The DecorationRole is set to an icon.
    The BackgroundRole is set to a gradient.

    """

    def __init__(self, sample_full_name):
        """
        Generate a new Sample Item.

        Remember that this object needs the **full name**.

        The display text (what will appear on the Protocol Editor) is the last
        name, but the constructor needs the full name.

        Parameters
        ----------
        sample_full_name : str
            Full name (complete hierarchy) of the sample.

        Returns
        -------
        None.

        """
        super().__init__()
        sample_last_name = sample_full_name.split('/')[-1]
        self.setText(sample_last_name)
        self.setData(ElementType.SAMPLE, UserRole.ITEM_TYPE)
        self.setData(sample_full_name, UserRole.SAMPLE_FULL_NAME)
        self.setData(sample_last_name, UserRole.SAMPLE_LAST_NAME)
        self.setData(QIcon(':/resources/icons8-ice-48.png'), Qt.DecorationRole)
        self.setData(QFont('MS Shell Dlg 2', 8, QFont.Bold), Qt.FontRole)
        gradient = QLinearGradient(00, 00, 60, 100)
        gradient.setColorAt(0, QColor.fromCmyk(5, 0, 0, 20))
        gradient.setColorAt(1, Qt.white)
        self.setData(QBrush(gradient), Qt.BackgroundRole)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : Dictionary
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        key = self.data(UserRole.SAMPLE_FULL_NAME)
        if key in yaml_dict.keys():
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class NavPicItem(TextItem):
    """
    Navigation Picture Item.

    This type is used to store navigation images.
    """

    def __init__(self, txt='', img_link=''):
        """
        Constructor an instance of NaPicItem.

        The type of this item is set to NavPic.

        The DecorationRole is set to an icon.

        Parameters
        ----------
        txt : str, optional
            The name of the picture used as display_role. The default is ''.
        img_link : str, optional
            The URL where the thumbnail of the image. The default is ''.

        Returns
        -------
        None.

        """
        super().__init__(txt=txt)
        self.setData(ElementType.NAVIGATION_PIC, UserRole.ITEM_TYPE)
        self.setData(img_link, UserRole.IMAGE)
        self.setData(QIcon(':/resources/icons8-map-marker-48.png'), Qt.DecorationRole)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : dict
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        key = self.text()
        if key in yaml_dict.keys():
            if 'Caption' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Caption'], UserRole.CAPTION)
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class OpticalImageItem(HTMLHelperMixin, TextItem):
    def __init__(self, path: str | Path):
        if isinstance(path, Path):
            name = path.name
            key = str(path)
        elif isinstance(path, str):
            key = path
            path = Path(path)
            name = path.name
        else:
            raise TypeError('Path must be str or Path')

        super().__init__(name)
        self.setData(ElementType.OPTICAL_PIC, UserRole.ITEM_TYPE)
        self.setData(key, UserRole.IMAGE)
        self.setData(key, UserRole.OPTICAL_IMAGE_KEY)
        self.setData(path, UserRole.OPTICAL_IMAGE_PATH)
        url = self.convert_path_to_uri(path)
        self.setData(url, UserRole.OPTICAL_IMAGE_URL)
        self.setData(QIcon(':/resources/icons8-compact-camera-32.png'), Qt.DecorationRole)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : dict
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        key = self.data(UserRole.OPTICAL_IMAGE_KEY)
        if key in yaml_dict.keys():
            if 'Caption' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Caption'], UserRole.CAPTION)
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class MicroPicItem(TextItem):
    """
    Microscope Picture Item.

    This type is used to store microscope pictures.
    """

    def __init__(self, txt: str = '', img_id: str = '', img_link: str = ''):
        """
        Constructor an instance of MicroPicItem.

        The type of this item is set to MicroPic.

        The DecorationRole is set to an icon.

        Parameters
        ----------
        img_id : str
            The key of the microscope image.

        img_link : str, optional
            The URL where the thumbnail of the image. The default is ''.

        Returns
        -------
        None.

        """
        super().__init__(txt=txt)
        self.setData(ElementType.MICROSCOPE_PIC, UserRole.ITEM_TYPE)
        self.setData(img_id, UserRole.PIC_ID)
        self.setData(img_link, UserRole.IMAGE)
        self.setData(QIcon(':/resources/icons8-optical-microscope-64.png'), Qt.DecorationRole)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : dict
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        pic_id = self.data(UserRole.PIC_ID)
        if pic_id in yaml_dict.keys():
            pass
        else:
            return
        if 'Caption' in yaml_dict[pic_id].keys():
            self.setData(yaml_dict[pic_id]['Caption'], UserRole.CAPTION)
        if 'Description' in yaml_dict[pic_id].keys():
            self.setData(yaml_dict[pic_id]['Description'], UserRole.DESCRIPTION)
        if 'Extra' in yaml_dict[pic_id].keys():
            self.setData(yaml_dict[pic_id]['Extra'], UserRole.EXTRA)


class VideoItem(TextItem):
    """
    Video Item.

    This item type is used to store video.
    """

    def __init__(self, txt: str = '', key: str = '', url: str = '', path: str | Path = ''):
        """
        Build an instance of the VideoItem.

        The DecorationRole is set to an icon.

        Parameters
        ----------
        txt: str
            Set the display role for the item (DisplayRole)
        key: str
            The video key used for retrieving the element from the VideoDict. (UserRole.VIDEO_KEY)
        url: str
            The video url for playback. (UserRole.VIDEO_URL)
        path: str | Path
            The video path (UserRole.VIDEO_PATH)
        """
        super().__init__(txt=txt)
        self.setData(ElementType.VIDEO_FILE, UserRole.ITEM_TYPE)
        self.setData(key, UserRole.VIDEO_KEY)
        self.setData(path, UserRole.VIDEO_PATH)
        self.setData(url, UserRole.VIDEO_URL)
        self.setData(QIcon(':/resources/icons8-video-clip-48.png'), Qt.DecorationRole)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : dict
            YAML Dictionary where the information of the item are stored.

        Returns
        -------
        None.
        """
        key = self.data(UserRole.VIDEO_KEY)
        if key in yaml_dict.keys():
            if 'Caption' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Caption'], UserRole.CAPTION)
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class UserEditor(QDialog, Ui_UserEditor):
    """Dialog window for the user credential editor."""

    def __init__(self, parent=None, username=None, password=None):
        """
        Build a new instance of the user editor.

        Parameters
        ----------
        parent : QObject, optional
            The parent object, very likely the MainWindow. The default is None.
        username : string, optional
            The current username. The default is None
        password : string, optional
            The current password. The default is None

        Returns
        -------
        None.

        """
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.username = username
        self.username_line_edit.setText(username)
        self.password = password
        self.password_line_edit.setText(password)

    @Slot(str)
    def password_edited(self, new_plain_text_pwd):
        """
        React to a password change.

        This slot is called everytime the password field is edited.

        Parameters
        ----------
        new_plain_text_pwd : string
            The newly entered password in plain text.

        Returns
        -------
        None.

        """
        self.password = autotools.encrypt_pass(new_plain_text_pwd)

    @Slot(str)
    def username_edited(self, new_username):
        """
        React to a username change.

        This slot is called everytime the username field is edited.

        Parameters
        ----------
        new_username : string
            The newly entered username in plain text.

        Returns
        -------
        None.

        """
        self.username = new_username


class FileSystemCommand:
    """
    A simple file system command.

    This class represents the basic implementation of a filesystem command, and it is part of the infrastructure to
    modify a protocol. In normal situation the user adds and removes protocol elements in an independent way, just by
    saving a new image in a sample folder. But similarly, one can decide to remove, rename or move an element while
    editing the protocol from the protocol editor.

    When (s)he does so a FileSystemCommand is generated and dispatched to a file system command that is taking care of
    executing the command.

    In other words, when the user asks for the removal of a picture from the ProtocolEditor, a delete file command is
    generated and processed. As a result, the watchdog is reacting to a file removal (including removing the mirror copy
    if any) and the corresponding element is removed from the protocol.
    """

    def __init__(self, command: autotools.FSCommandType, input_path: Path | str, output_path: Path | str = None):
        """
        Initialize a file system command.

        The simple file system commands already implemented are operating on one, maximum two paths.
        Those must be provided during the instance initialization.

        Parameters
        ----------
        command: FSCommandType
            enumerator with all existing and implemented file system commands.
        input_path: Path | str
            the input path on which the command is acting. The parameter is stored in the class member as a Path object.
        output_path: Path | str
            the output path on which the command is acting. The parameter is stored in the class member as a Path
            object.
        """
        if not isinstance(command, autotools.FSCommandType):
            log.error('Unable to process filesystem command. Command %s not available' % command)
            return
        self.command = command
        self.input_path = Path(input_path)
        self.output_path = None if output_path is None else Path(output_path)

    def __str__(self):
        """
        Represent the command as a string.

        Returns
        -------
        The string representation of the class.
        """
        if self.output_path is None:
            return f'Processing {self.command} on {self.input_path}'
        else:
            return f'Processing {self.command} from {self.input_path} to {self.output_path}'


class RenameDialog(QDialog, Ui_RenameDialog):
    """
    Subclass of QDialog to deal with the renaming of an item.
    """

    def __init__(self, parent: QObject = None, text: str = None, original_name: str = None):
        """
        Setup and initialize the dialog.

        Parameters
        ----------
        parent: QObject
            The parent object calling this dialog.
        text: str
            The text to be displayed.
        original_name: str
            The original name of the object being renamed.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        if text is not None:
            self.message.setText(text)
        if original_name is not None:
            self.new_name_field.setText(original_name)


class ChangeSampleDialog(QDialog, Ui_ChangeSampleDialog):
    """
    Subclass of QDialog to deal with the moving of an item from one sample to another.
    """

    def __init__(self, parent: QObject = None, item_name: str | None = None, sample_name: str | None = None,
                 sample_list: list[str] | None = None) -> None:
        """
        Setup and initialize the dialog.

        Parameters
        ----------
        parent: QObject
            The parent object calling this dialog
        item_name: str
            The name of the item being moved.
        sample_name: str
            The sample (full name) where the item is at the moment. In the case of a root sample, use 'Samples' as
            sample name, it is to say the section name.
        sample_list: list[str]
            The list of all samples.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent

        is_root_sample = False
        if item_name is not None:
            self.item_name = item_name
            self.element_label.setText(self.item_name)
        if sample_name is not None:
            self.sample_name = sample_name
            if sample_name == 'Samples':
                # it means we are moving a root sample
                is_root_sample = True
            self.current_sample_label.setText(self.sample_name)
        if sample_list is not None:
            self.sample_list = sample_list  # [sample for sample in sample_list if sample != 'Protocol']
            self.sample_combo.addItems(self.sample_list)
            if not is_root_sample:
                self.sample_combo.model().item(self.sample_combo.findText(self.sample_name)).setEnabled(False)
            else:
                # since it is a root sample, then disable its name from the combo box.
                self.sample_combo.model().item(self.sample_combo.findText(self.item_name)).setEnabled(False)
            for i in range(self.sample_combo.count()):
                if self.sample_combo.model().item(i).isEnabled():
                    self.sample_combo.setCurrentIndex(i)
                    break


class ProtocolEditor(HTMLHelperMixin, QDialog, Ui_tree_viewer_dialog):
    """Dialog window for the protocol editor."""

    # Signal to emit a file system command.
    # When the user is performing an operation on a protocol element, this is actually corresponding to a file system
    # command (rename / move / delete...).
    # The command is generated inside the ProtocolEditor and is transmitted as a signal argument to the MainWindow
    # where the actual command is received and executed.
    execute_filesystem_command = Signal(FileSystemCommand, name='execute_filesystem_command')

    def __init__(self, parent=None, autolog=None):
        """
        Build a new instance of the protocol editor.

        Parameters
        ----------
        parent : QObject, optional
            The parent object, very likely the MainWindow. The default is None.
        autolog : autologbook.Protocol, optional
            An instance of the protocol. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(parent)
        self.parent = parent
        self.autolog = autolog
        self.setupUi(self)

        # prepare the media player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_preview)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.error.connect(self.media_error_handler)

        # set the first page of the previewer stack to be shown
        self.preview_stack.setCurrentIndex(0)

        # connect the signals from MainWindow
        self.parent.added_element.connect(self.add_element)
        self.parent.removed_element.connect(self.remove_element)
        self.parent.change_autolog.connect(self.change_autolog)
        self.parent.reset_content.connect(self.reset_content)

        # prepare the model and get its root node
        self.tree_model = QStandardItemModel()
        self.rootNode = self.tree_model.invisibleRootItem()
        self.autolog_tree_viewer.setHeaderHidden(True)

        # prepare a proxy model and connected it to the model
        self.tree_model_proxy = TreeViewerProxyModel(self)
        self.tree_model_proxy.setSourceModel(self.tree_model)
        self.tree_model_proxy.setRecursiveFilteringEnabled(True)
        self.tree_model_proxy.setDynamicSortFilter(False)

        # now generate the model
        self.generate_model()

        # link the proxy model to the view
        self.autolog_tree_viewer.setModel(self.tree_model_proxy)

        # customize the context menu for the autolog_tree_viewer
        self.autolog_tree_viewer.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_viewer_context_menu = self.generate_tree_view_context_menu()
        self.autolog_tree_viewer.customContextMenuRequested.connect(self.on_tree_context_menu_request)
        self.tree_search_string.textChanged.connect(self.tree_filter)

        # this is the pointer to the last selected item in order to start again from there when reopening the protocol
        # editor window. It has to be a persistent item model because we want to store it
        self.tree_model_last_selected_item = None

        # this is a pointer of the last inserted item
        self.tree_model_last_inserted_item = None

        # prepare the sample_list_view.
        # This is linked to the same model as the autolog_tree_viewer and they share the same selection model.
        # At the beginning we set the root of the sample_list_view to the SectionItem named 'Samples'
        self.sample_list_view.setModel(self.tree_model_proxy)
        self.sample_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sample_list_view_context_menu = self.generate_sample_list_view_context_menu()
        self.sample_list_view.customContextMenuRequested.connect(self.on_sample_list_context_menu_request)
        self.sample_list_view.setSelectionModel(self.autolog_tree_viewer.selectionModel())
        self.sample_list_view.setRootIndex(
            self.tree_model.findItems('Samples', QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)[0].index()
        )

        # connect the inserted new rows signals
        self.tree_model.rowsInserted.connect(self.new_rows_added)

        # connect the selection changed of the selectionModel of the autolog_tree_viewer to the get_and_update_values.
        # This slot is responsible to handle the customization fields (caption, description, extra).
        # The customization values of the previously selected item (if valid) are transferred from the GUI to the item
        # data fields and to the yaml dictionary.
        # The customization values from the newly selected item are transferred to the GUI.
        self.autolog_tree_viewer.selectionModel().selectionChanged.connect(self.get_and_update_values)

        # prepare the model for the metadata with its proxy and connect it to the table view
        self.metadata_model = MetadataModel()
        self.metadata_proxy_model = QSortFilterProxyModel(self)
        self.metadata_proxy_model.setSourceModel(self.metadata_model)
        self.metadata_table.setModel(self.metadata_proxy_model)
        self.metadata_table.setSortingEnabled(True)
        self.metadata_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.metadata_table.verticalHeader().setVisible(False)
        self.metadata_search_string.textChanged.connect(self.metadata_filter)
        # set the metadata context menu
        self.metadata_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.metadata_table_context_menu = self.generate_metadata_context_menu()
        self.metadata_table.customContextMenuRequested.connect(self.on_metadata_context_menu_request)

        # this is an emulation of the clipboard to copy all customization data in one go.
        self.custom_data_dict = {'Caption': '', 'Description': '', 'Extra': ''}
        self.custom_data_dict_available = False

        # initialize a yaml dictionary recycler
        self.yaml_dictionary_recycler = autotools.YAMLRecycler()

        # set the image preview context menu
        self.image_preview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.image_preview_context_menu = self.generate_image_preview_context_menu()
        self.image_preview.customContextMenuRequested.connect(self.on_image_preview_context_menu_request)

        # set the custom fields context menu
        self.caption_field.setContextMenuPolicy(Qt.CustomContextMenu)
        self.caption_field.customContextMenuRequested.connect(self.on_custom_edit_context_menu_request)
        self.description_input.setContextMenuPolicy(Qt.CustomContextMenu)
        self.description_input.customContextMenuRequested.connect(self.on_custom_edit_context_menu_request)
        self.extrainfo_input.setContextMenuPolicy(Qt.CustomContextMenu)
        self.extrainfo_input.customContextMenuRequested.connect(self.on_custom_edit_context_menu_request)
        self.custom_edit_context_menu = self.generate_custom_edit_context_menu()

        # set the menu for the recycle_dropdown_button
        self.recycle_dropdown_button.setMenu(self.generate_recycle_dropdown_menu())
        self.recycle_dropdown_button.setDefaultAction(self.recycle_dropdown_button.menu().actions()[0])
        self.recycle_dropdown_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        # set the menu for the edit_dropdown_button
        self.edit_dropdown_button.setMenu(self.generate_edit_dropdown_menu())
        self.edit_dropdown_button.setDefaultAction(self.edit_dropdown_button.menu().actions()[0])
        self.edit_dropdown_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        # set the menu for the markdown_font_tool_button
        self.markdown_font_tool_button.setMenu(self.generate_markdown_font_tool_button())
        self.markdown_font_tool_button.setDefaultAction(self.markdown_font_tool_button.menu().actions()[0])
        self.markdown_font_tool_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.markdown_font_tool_button.setEnabled(False)

        # set the menu for the markdown_font_tool_button
        self.markdown_paragraph_tool_button.setMenu(self.generate_markdown_paragraph_tool_button())
        self.markdown_paragraph_tool_button.setDefaultAction(self.markdown_paragraph_tool_button.menu().actions()[0])
        self.markdown_paragraph_tool_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.markdown_paragraph_tool_button.setEnabled(False)

        # set the menu for the copy custom
        self.copy_custom_value_button.setMenu(self.generate_copy_custom_value_button())
        self.copy_custom_value_button.setDefaultAction(self.copy_custom_value_button.menu().actions()[0])
        self.copy_custom_value_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.copy_custom_value_button.setEnabled(False)

        # set the menu for the copy custom
        self.paste_custom_value_button.setMenu(self.generate_paste_custom_value_button())
        self.paste_custom_value_button.setDefaultAction(self.paste_custom_value_button.menu().actions()[0])
        self.paste_custom_value_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.paste_custom_value_button.setEnabled(False)

        # install the event filter for some widgets
        self.description_input.installEventFilter(self)
        self.caption_field.installEventFilter(self)
        self.extrainfo_input.installEventFilter(self)
        self.image_preview.installEventFilter(self)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        """
        Overload the event filtering for the customized some specific events.

        In particular, we are taking care of the following events and sources:
            - FocusIn for caption_field, description_input and extrainfo_input:
                -> Used to enable/disable the customization edit / special copy paste tool buttons.
            - MouseButtonDblClick for image_preview
                -> Used to open the image in the external viewer.

        Parameters
        ----------
        object: QObject
            The object emitting the event.
        event: QEvent
            The emitted event.

        Returns
        -------
        bool
        """

        # edit controls
        edit_ctrls = [self.markdown_font_tool_button, self.markdown_paragraph_tool_button]
        adv_copy_ctrls = [self.copy_custom_value_button, self.paste_custom_value_button]
        if event.type() == QEvent.FocusIn and object in [self.description_input, self.extrainfo_input]:
            for ctrl in adv_copy_ctrls:
                ctrl.setEnabled(True)
            if not self.custom_data_dict_available:
                self.paste_custom_value_button.setEnabled(False)
            for ctrl in edit_ctrls:
                ctrl.setEnabled(True)

        if event.type() == QEvent.FocusIn and object in [self.caption_field]:

            for ctrl in edit_ctrls:
                ctrl.setEnabled(False)
            for ctrl in adv_copy_ctrls:
                ctrl.setEnabled(True)
            if not self.custom_data_dict_available:
                self.paste_custom_value_button.setEnabled(False)

        if event.type() == QEvent.MouseButtonDblClick and object == self.image_preview:
            self.open_external_image_viewer()

        return super(ProtocolEditor, self).eventFilter(object, event)

    @Slot(QAction)
    def triggered_copy_custom_action(self, action: QAction):
        """
        React to a change in the copy custom tool button.

        The copy tool button is featuring a menu with several options. When the user selects a specific option for the
        copy, the same option is selected for the paste.

        Parameters
        ----------
        action: QAction
            Action selected in the copy_custom_value_button menu
        """
        for i, a in enumerate(self.copy_custom_value_button.menu().actions()):
            if a.text() == action.text():
                self.paste_custom_value_button.setDefaultAction(self.paste_custom_value_button.menu().actions()[i])
                break

    def generate_copy_custom_value_button(self) -> QMenu:
        """Generate the menu to be attached to the copy custom values button"""
        scheme = {
            'copy_all_custom_fields': {
                'icon': ':/resources/icons8-copy-all-48.png',
                'text': 'Copy all',
                'slot': lambda: self.copy_custom_values('all'),
            },
            'copy_caption': {
                'icon': ':/resources/icons8-copy-caption-48.png',
                'text': 'Copy caption',
                'slot': lambda: self.copy_custom_values('caption'),
            },
            'copy_description': {
                'icon': ':/resources/icons8-copy-description-48.png',
                'text': 'Copy description',
                'slot': lambda: self.copy_custom_values('description'),
            },
            'copy_extra': {
                'icon': ':/resources/icons8-copy-extra-48.png',
                'text': 'Copy extra',
                'slot': lambda: self.copy_custom_values('extra'),
            }
        }
        return generate_tool_button_menu_from_scheme(menu=None, parent=self.copy_custom_value_button,
                                                     menu_scheme=scheme)

    def generate_paste_custom_value_button(self) -> QMenu:
        """Generate the menu to be attached to the paste custom values button"""
        scheme = {
            'copy_all_custom_fields': {
                'icon': ':/resources/icons8-paste-all-48.png',
                'text': 'Paste all',
                'slot': lambda: self.paste_custom_values('all'),
            },
            'copy_caption': {
                'icon': ':/resources/icons8-paste-caption-48.png',
                'text': 'Paste caption',
                'slot': lambda: self.paste_custom_values('caption'),
            },
            'copy_description': {
                'icon': ':/resources/icons8-paste-description-48.png',
                'text': 'Paste description',
                'slot': lambda: self.paste_custom_values('description'),
            },
            'copy_extra': {
                'icon': ':/resources/icons8-paste-extra-48.png',
                'text': 'Paste extra',
                'slot': lambda: self.paste_custom_values('extra'),
            }
        }
        return generate_tool_button_menu_from_scheme(menu=None, parent=self.copy_custom_value_button,
                                                     menu_scheme=scheme)

    def generate_markdown_paragraph_tool_button(self) -> QMenu:
        """Generate the menu to be attached to the markdown paragraph button"""
        scheme = {
            'link': {
                'icon': ':/resources/icons8-hyperlink-48.png',
                'text': 'Insert generic link...',
                'slot': lambda: self.edit_custom_text('link'),
            },
            'bulleted': {
                'icon': ':/resources/icons8-bulleted-list-48.png',
                'text': 'Insert bulleted list...',
                'slot': lambda: self.edit_custom_text('bullet')
            },
            'numbered': {
                'icon': ':/resources/icons8-numbered-list-48.png',
                'text': 'Insert numbered list...',
                'slot': lambda: self.edit_custom_text('number'),
            },
        }
        return generate_tool_button_menu_from_scheme(menu=None, parent=self.markdown_paragraph_tool_button,
                                                     menu_scheme=scheme)

    def generate_markdown_font_tool_button(self) -> QMenu:
        """Generate the menu to be attached to the markdown font button"""
        scheme = {
            'bold_action': {
                'icon': ':/resources/icons8-bold-48.png',
                'text': 'Bold',
                'slot': lambda: self.edit_custom_text('bold')
            },
            'italic_action': {
                'icon': ':/resources/icons8-italic-48.png',
                'text': 'Italic',
                'slot': lambda: self.edit_custom_text('italic')
            },
            'underline_action': {
                'icon': ':/resources/icons8-underline-48.png',
                'text': 'Underline',
                'slot': lambda: self.edit_custom_text('underline')
            },
            'strikeout': {
                'icon': ':/resources/icons8-strikethrough-48.png',
                'text': 'Strikeout',
                'slot': lambda: self.edit_custom_text('strikeout')
            },
            'subscript': {
                'icon': ':/resources/icons8-subscript-48.png',
                'text': 'Subscript',
                'slot': lambda: self.edit_custom_text('subscript')
            },
            'superscript': {
                'icon': ':/resources/icons8-superscript-48.png',
                'text': 'Superscript',
                'slot': lambda: self.edit_custom_text('superscript')
            },
        }

        return generate_tool_button_menu_from_scheme(menu=None, parent=self.markdown_font_tool_button,
                                                     menu_scheme=scheme)

    def generate_edit_dropdown_menu(self) -> QMenu:
        """Generate the menu to be attached to the edit dropdown button"""
        scheme = {
            'rename_action': {
                'icon': ':/resources/icons8-rename-48.png',
                'text': 'Rename element...',
                'slot': self.rename_protocol_element,
            },
            'move_action': {
                'icon': ':/resources/icons8-move-up-row-48.png',
                'text': 'Move to another sample...',
                'slot': self.move_element_to_another_sample,
            },

        }

        return generate_tool_button_menu_from_scheme(menu=None, parent=self.edit_dropdown_button, menu_scheme=scheme)

    def generate_recycle_dropdown_menu(self) -> QMenu:
        """Generate the menu to be attached to the recycle dropdown button"""
        scheme = {
            'recycle_action': {
                'icon': ':/resources/icons8-recycle-48.png',
                'text': 'Recycle element...',
                'slot': self.recycle_protocol_element,
            },
            'delete_action': {
                'icon': ':/resources/icons8-trash-can-48.png',
                'text': 'Delete element...',
                'slot': self.delete_protocol_element,
            },
            'restore_action': {
                'icon': ':/resources/icons8-trash-restore-48.png',
                'text': 'Restore element...',
                'slot': self.restore_element_from_trash,
            },

        }
        return generate_tool_button_menu_from_scheme(menu=None, parent=self.recycle_dropdown_button, menu_scheme=scheme)

    def restore_element_from_trash(self):
        """
        Restore one element from the recycling bin.

        Only Microscope Pictures and Videos can be restored.
        """

        # let's get the sample list (those are sample full names)
        sample_list = [self.sample_selector.itemText(i) for i in range(self.sample_selector.count())]

        # we need the base path to be prepended to the sample full name to have the path.
        protocol_path = self.parent.protocol_folder_path

        # we need the current sample. we can get it from the currently selected item in the tree view.
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        model_item = self.tree_model.itemFromIndex(model_index)
        item_type = model_item.data(UserRole.ITEM_TYPE)
        if item_type in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
            sample_item = model_item.parent()
            sample_full_name = sample_item.data(UserRole.SAMPLE_FULL_NAME)
        elif item_type == ElementType.SAMPLE:
            sample_full_name = model_item.data(UserRole.SAMPLE_FULL_NAME)
        elif item_type in [ElementType.ATTACHMENT_FILE, ElementType.OPTICAL_PIC]:
            if model_item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                sample_full_name = model_item.parent().data(UserRole.SAMPLE_FULL_NAME)
            else:
                sample_full_name = 'Protocol'
        else:
            sample_full_name = None

        # create an instance of the RecoverElementDialog
        dialog = RecoverElementDialog(parent=self, sample_list=sample_list,
                                      protocol_path=protocol_path, current_sample=sample_full_name)

        # execute the dialog
        if dialog.exec_():

            # this is a list of selected items to be restored.
            proxy_indexes = dialog.file_list_view.selectionModel().selectedIndexes()

            # elements in the basket bin are either
            # MICROSCOPE_PIC, VIDEO_FILE, ATTACHMENT or OPTICAL IMAGES but
            # in the bin we cannot check the type from the tree_model.
            # we need the type in order to perform a proper recycling.
            # we can use the type_guessers as in the watchdog.
            type_guessers = {}
            image_file_matching = autoconfig.IMAGEFILE_MATCHING_PATTERNS
            image_file_exclude = None
            type_guessers[str(autotools.ElementType.MICROSCOPE_PIC)] = \
                (autotools.ElementTypeGuesser(image_file_matching, image_file_exclude),
                 autotools.ElementType.MICROSCOPE_PIC)
            video_file_include_pattern = autoconfig.VIDEO_MATCHING_PATTERNS
            video_file_exclude_pattern = None
            type_guessers[str(autotools.ElementType.VIDEO_FILE)] = \
                (autotools.ElementTypeGuesser(video_file_include_pattern, video_file_exclude_pattern),
                 autotools.ElementType.VIDEO_FILE)
            attachment_file_include_pattern = autoconfig.ATTACHMENT_MATCHING_PATTERNS
            attachment_file_exclude_pattern = None
            type_guessers[str(autotools.ElementType.ATTACHMENT_FILE)] = \
                (autotools.ElementTypeGuesser(attachment_file_include_pattern, attachment_file_exclude_pattern),
                 autotools.ElementType.ATTACHMENT_FILE)
            optical_image_include_pattern = autoconfig.OPTICAL_IMAGE_MATCHING_PATTERNS
            optical_image_exclude_pattern = None
            type_guessers[str(autotools.ElementType.OPTICAL_PIC)] = \
                (autotools.ElementTypeGuesser(optical_image_include_pattern, optical_image_exclude_pattern),
                 autotools.ElementType.OPTICAL_PIC)

            # loop over all indexes
            for proxy_index in proxy_indexes:
                model_index = dialog.file_list_model_proxy.mapToSource(proxy_index)
                element_full_path = Path(model_index.data(UserRole.ELEMENT_FULL_PATH))
                old_path = element_full_path.relative_to(protocol_path)
                new_path = old_path.parent.parent / old_path.name

                # use the ElementTypeGuesser to guess the type of what we are restoring.
                item_type = None
                for (guesser, etype) in type_guessers.values():
                    if guesser.is_ok(element_full_path):
                        item_type = etype
                        break
                if item_type in [ElementType.VIDEO_FILE, ElementType.MICROSCOPE_PIC, ElementType.ATTACHMENT_FILE,
                                 ElementType.OPTICAL_PIC]:
                    # we can perform the recycling of the custom values
                    # this is a bit confusing. The basket bin is on the local_path pc, not necessarily on the
                    # image server, while the key in the yaml files are from paths from the image server.
                    # so actually now we cannot use the protocol_folder, but we shall use the mirror folder
                    # if it exists. To avoid this problem just use the autolog.path that is always pointing
                    # to the image server.
                    old_key = str(self.autolog.path / old_path)
                    new_key = str(self.autolog.path / new_path)
                    self.yaml_dictionary_recycler.recycle(self.autolog.yamlDict, item_type, old_key, new_key)
                else:
                    log.warning('Recycling of other protocol elements is not possible.')

                command = FileSystemCommand(FSCommandType.RENAME_FILE, old_path, new_path)
                self.execute_filesystem_command.emit(command)
                autotools.dump_yaml_file(self.autolog.yamlDict, self.autolog.yamlFilename)

    def generate_metadata_context_menu(self) -> QMenu:
        """Generate the context menu for the metadata table view"""

        # Use the standard context menu as a starting point for the customization.
        context_menu = self.description_input.createStandardContextMenu()
        context_menu.addSeparator()

        menu_scheme = {
            'copy_special_menu': {
                'type': QMenu,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'copy_special_menu',
                'obj': None,
                'text': 'Copy special...',
                'icon': ':/resources/icons8-copy-48.png',
                'show_when_flag': MetadataVisibilityFlag.WITH_ITEM,
                'separator_after': True,
            },
            'copy_single_value': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_special_menu',
                'obj': None,
                'name': 'copy_single_value',
                'text': 'Copy current value to clipboard',
                'icon': ':/resources/icons8-copy-single-48.png',
                'slot': lambda: self.copy_metadata_to_clipboard('single_value'),
                'show_when_flag': MetadataVisibilityFlag.WITH_ITEM,
                'separator_after': False,
            },
            'copy_single_pair': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_special_menu',
                'obj': None,
                'name': 'copy_single_pair',
                'text': 'Copy current key/value pair to clipboard',
                'icon': ':/resources/icons8-copy-pair-48.png',
                'slot': lambda: self.copy_metadata_to_clipboard('single_pair'),
                'show_when_flag': MetadataVisibilityFlag.WITH_ITEM,
                'separator_after': False,
            },
            'copy_all_pairs': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_special_menu',
                'obj': None,
                'name': 'copy_all_pairs',
                'text': 'Copy all metadata to clipboard',
                'icon': ':/resources/icons8-copy-all-48.png',
                'slot': lambda: self.copy_metadata_to_clipboard('all'),
                'show_when_flag': MetadataVisibilityFlag.WITH_ITEM,
                'separator_after': False,
            },
            'save_metadata_to_file': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'save_metadata_to_file',
                'text': 'Save metadata to CSV file',
                'icon': ':/resources/icons8-save-as-48.png',
                'slot': lambda: self.save_metadata_to_file('all'),
                'show_when_flag': MetadataVisibilityFlag.WITH_ITEM,
                'separator_after': False,
            },
        }
        return generate_context_menu_from_scheme(context_menu, self.metadata_table, menu_scheme)

    def generate_custom_edit_context_menu(self) -> QMenu:
        """Generate the context menu for the caption/description/extra input fields"""

        # Use the standard context menu as a starting point for the customization.
        context_menu = self.description_input.createStandardContextMenu()
        context_menu.addSeparator()

        menu_scheme = {
            'custom_fields_menu': {
                'type': QMenu,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'custom_fields_menu',
                'obj': None,
                'text': 'Customization fields menu',
                'icon': ':/resources/icons8-design-48.png',
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': True,
            },
            'copy_custom_fields': {
                'type': QMenu,
                'parent_name': 'custom_fields_menu',
                'parent_obj': None,
                'name': 'copy_custom_fields',
                'obj': None,
                'text': 'Copy custom fields',
                'icon': ':/resources/icons8-copy-48.png',
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'copy_all_custom_fields': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_custom_fields',
                'obj': None,
                'name': 'copy_all_custom_fields',
                'text': 'Copy all custom fields to clipboard',
                'icon': ':/resources/icons8-copy-all-48.png',
                'slot': lambda: self.copy_custom_values('all'),
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'copy_caption': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_custom_fields',
                'obj': None,
                'name': 'copy_caption',
                'text': 'Copy caption to clipboard',
                'icon': ':/resources/icons8-copy-caption-48.png',
                'slot': lambda: self.copy_custom_values('caption'),
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'copy_description': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_custom_fields',
                'obj': None,
                'name': 'copy_description',
                'text': 'Copy description to clipboard',
                'icon': ':/resources/icons8-copy-description-48.png',
                'slot': lambda: self.copy_custom_values('description'),
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'copy_extra': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_custom_fields',
                'obj': None,
                'name': 'copy_extra',
                'text': 'Copy extra to clipboard',
                'icon': ':/resources/icons8-copy-extra-48.png',
                'slot': lambda: self.copy_custom_values('extra'),
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'paste_custom_fields': {
                'type': QMenu,
                'parent_name': 'custom_fields_menu',
                'parent_obj': None,
                'name': 'paste_custom_fields',
                'obj': None,
                'text': 'Paste custom fields',
                'icon': ':/resources/icons8-paste-special-48.png',
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'paste_all_custom_fields': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'paste_custom_fields',
                'obj': None,
                'name': 'paste_all_custom_fields',
                'text': 'Paste all custom fields',
                'icon': ':/resources/icons8-paste-special-48.png',
                'slot': lambda: self.paste_custom_values('all'),
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'paste_caption': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'paste_custom_fields',
                'obj': None,
                'name': 'paste_caption',
                'text': 'Paste caption',
                'icon': ':/resources/icons8-paste-special-48.png',
                'slot': lambda: self.paste_custom_values('caption'),
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'paste_description': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'paste_custom_fields',
                'obj': None,
                'name': 'paste_description',
                'text': 'Paste description',
                'icon': ':/resources/icons8-paste-special-48.png',
                'slot': lambda: self.paste_custom_values('description'),
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'paste_extra': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'paste_custom_fields',
                'obj': None,
                'name': 'paste_extra',
                'text': 'Paste extra',
                'icon': ':/resources/icons8-paste-special-48.png',
                'slot': lambda: self.paste_custom_values('extra'),
                'show_when_flag': CustomEditVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'mark_down_menu': {
                'type': QMenu,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'mark_down_menu',
                'obj': None,
                'text': 'Markdown menu',
                'icon': ':/resources/icons8-markdown-48.png',
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': True,
            },
            'mark_down_edit_menu': {
                'type': QMenu,
                'parent_name': 'mark_down_menu',
                'parent_obj': None,
                'name': 'mark_down_edit_menu',
                'obj': None,
                'text': 'Text edit menu',
                'icon': ':/resources/icons8-choose-font-48.png',
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': True,
            },
            'insert_bold_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'mark_down_edit_menu',
                'obj': None,
                'name': 'insert_bold_action',
                'text': 'Insert bold',
                'icon': ':/resources/icons8-bold-48.png',
                'slot': lambda: self.edit_custom_text('bold'),
                'short_cut_key_sequence': 'Ctrl+Shift+B',
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': False,
            },
            'insert_italic_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'mark_down_edit_menu',
                'obj': None,
                'name': 'insert_italic_action',
                'text': 'Insert italic',
                'icon': ':/resources/icons8-italic-48.png',
                'slot': lambda: self.edit_custom_text('italic'),
                'short_cut_key_sequence': 'Ctrl+Shift+I',
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': False,
            },
            'insert_underline_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'mark_down_edit_menu',
                'obj': None,
                'name': 'insert_underline_action',
                'text': 'Insert underline',
                'icon': ':/resources/icons8-underline-48.png',
                'slot': lambda: self.edit_custom_text('underline'),
                'short_cut_key_sequence': 'Ctrl+Shift+U',
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': False,
            },
            'insert_strikeout_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'mark_down_edit_menu',
                'obj': None,
                'name': 'insert_strikeout_action',
                'text': 'Insert strikeout',
                'icon': ':/resources/icons8-strikethrough-48.png',
                'short_cut_key_sequence': 'Ctrl+Shift+T',
                'slot': lambda: self.edit_custom_text('strikeout'),
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': True,
            },
            'insert_subscript_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'mark_down_edit_menu',
                'obj': None,
                'name': 'insert_subscript_action',
                'text': 'Insert subscript',
                'icon': ':/resources/icons8-subscript-48.png',
                'slot': lambda: self.edit_custom_text('subscript'),
                'short_cut_key_sequence': 'Ctrl+Shift+-',
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': False,
            },
            'insert_superscript_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'mark_down_edit_menu',
                'obj': None,
                'name': 'insert_superscript_action',
                'text': 'Insert superscript',
                'icon': ':/resources/icons8-superscript-48.png',
                'short_cut_key_sequence': 'Ctrl+Shift++',
                'slot': lambda: self.edit_custom_text('superscript'),
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': False,
            },
            'insert_link_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'mark_down_menu',
                'obj': None,
                'name': 'insert_link_action',
                'text': 'Insert link',
                'icon': ':/resources/icons8-hyperlink-48.png',
                'slot': lambda: self.edit_custom_text('link'),
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': False,
            },
            'insert_bullet_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'mark_down_menu',
                'obj': None,
                'name': 'insert_bullet_action',
                'text': 'Insert bulleted list',
                'icon': ':/resources/icons8-bulleted-list-48.png',
                'slot': lambda: self.edit_custom_text('bullet'),
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': False,
            },
            'insert_numbered_list_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'mark_down_menu',
                'obj': None,
                'name': 'insert_numbered_list_action',
                'text': 'Insert numbered list',
                'icon': ':/resources/icons8-numbered-list-48.png',
                'slot': lambda: self.edit_custom_text('number'),
                'show_when_flag': CustomEditVisibilityFlag.MARKDOWN,
                'separator_after': False,
            },

        }
        return generate_context_menu_from_scheme(context_menu, self.description_input, menu_scheme)

    def generate_tree_view_context_menu(self) -> QMenu:
        """Generate the context menu for the tree view"""

        context_menu = None

        menu_scheme = {
            'expand_all_action': {
                'type': QAction,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'expand_all',
                'obj': None,
                'text': 'Expand all',
                'icon': ':/resources/icons8-expand-arrow-48.png',
                'slot': self.expand_all_elements,
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },
            'collapse_all_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'collapse_all',
                'text': 'Collapse all',
                'icon': ':/resources/icons8-collapse-arrow-48.png',
                'slot': self.collapse_all_elements,
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },
            'scroll_to_last': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'scroll_to_last',
                'text': 'Go to last inserted item',
                'icon': ':/resources/icons8-sniper-48.png',
                'slot': self.scroll_to_last_inserted_item,
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': True,
            },
            'markdown_menu': {
                'type': QMenu,
                'obj': None,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'markdown_menu',
                'text': 'Markdown tools',
                'icon': ':/resources/icons8-markdown-48.png',
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': True,
            },
            'markdown_link_menu': {
                'type': QMenu,
                'obj': None,
                'parent_name': 'markdown_menu',
                'parent_obj': None,
                'name': 'markdown_link_menu',
                'text': 'Markdown link tools',
                'icon': ':/resources/icons8-tools-48.png',
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },
            'generic_link': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'markdown_link_menu',
                'obj': None,
                'name': 'generic_link',
                'text': 'Copy generic link to clipboard',
                'icon': ':/resources/icons8-hyperlink-48.png',
                'slot': lambda: QApplication.clipboard().setText('[link_text](link_URL)'),
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },
            'specific_link': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'markdown_link_menu',
                'obj': None,
                'name': 'specific_link',
                'text': 'Copy anchor link of this element to clipboard',
                'icon': ':/resources/icons8-hyperlink-48.png',
                'slot': self.copy_anchor_link_markdown_to_clipboard,
                'show_when_flag': ElementTypeVisitiliyFlag.ANCHORABLE_ITEM,
                'separator_after': False,
            },
            'markdown_image_menu': {
                'type': QMenu,
                'obj': None,
                'parent_name': 'markdown_menu',
                'parent_obj': None,
                'name': 'markdown_image_menu',
                'text': 'Markdown image tools',
                'icon': ':/resources/icons8-picture-48.png',
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': True,
            },
            'generic_image': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'markdown_image_menu',
                'obj': None,
                'name': 'generic_link',
                'text': 'Copy generic inline image to clipboard',
                'slot': lambda: QApplication.clipboard().setText('![image_alt_text](image_URL "image_title")'),
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },
            'markdown_selected_image_thumb': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'markdown_image_menu',
                'obj': None,
                'name': 'markdown_selected_image_thumb',
                'text': 'Copy inline thumbnail image to clipboard',
                'icon': ':/resources/icons8-picture-48.png',
                'slot': self.copy_image_markdown_to_clipboard,
                'show_when_flag': ElementTypeVisitiliyFlag.IMAGE_ITEM,
                'separator_after': False,
            },
            'open_browser_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'open_browser',
                'text': 'Open a browser window here...',
                'icon': ':/resources/icons8-folder-48.png',
                'slot': self.open_protocol_folder,
                'show_when_flag': ElementTypeVisitiliyFlag.PROTOCOL_ITEM,
                'separator_after': False,
            },
            'copy_sample_path_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'copy_sample_path',
                'text': 'Copy sample path',
                'icon': ':/resources/icons8-copy-link-48.png',
                'slot': self.copy_sample_path,
                'show_when_flag': ElementTypeVisitiliyFlag.SAMPLE,
                'separator_after': True,
            },
            'copy_full_path_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'copy_element_path',
                'text': 'Copy element path',
                'icon': ':/resources/icons8-copy-link-48.png',
                'slot': self.copy_element_path,
                'show_when_flag': ElementTypeVisitiliyFlag.PROTOCOL_ITEM,
                'separator_after': True,
            },
            'change_sample_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'change_sample',
                'text': 'Move item in another sample...',
                'icon': ':/resources/icons8-move-up-row-48.png',
                'short_cut_key_sequence': 'Ctrl+F2',
                'slot': self.move_element_to_another_sample,
                'show_when_flag': ElementTypeVisitiliyFlag.MOVABLE_ITEM,
                'separator_after': False,
            },
            'rename_item_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'rename_action',
                'text': 'Rename item...',
                'icon': ':/resources/icons8-rename-48.png',
                'short_cut_key_sequence': 'F2',
                'slot': self.rename_protocol_element,
                'show_when_flag': ElementTypeVisitiliyFlag.RENAMEBABLE_ITEM,
                'separator_after': False,
            },
            'recycle_menu': {
                'type': QMenu,
                'obj': None,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'recycle_menu',
                'text': 'Recycle / delete / recover',
                'icon': ':/resources/icons8-recycle-48.png',
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': True,
            },
            'delete_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'recycle_menu',
                'obj': None,
                'name': 'delete_action',
                'text': 'Delete item...',
                'icon': ':/resources/icons8-trash-can-48.png',
                'slot': self.delete_protocol_element,
                'show_when_flag': ElementTypeVisitiliyFlag.DELETABLE_ITEM,
                'separator_after': False,
            },
            'recycle_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'recycle_menu',
                'obj': None,
                'name': 'recycle_action',
                'text': 'Recycle item...',
                'icon': ':/resources/icons8-recycle-48.png',
                'slot': self.recycle_protocol_element,
                'show_when_flag': ElementTypeVisitiliyFlag.RECYCLABLE_ITEM,
                'separator_after': False,
            },
            'recover_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'recycle_menu',
                'obj': None,
                'name': 'recover_action',
                'text': 'Recover item from bin...',
                'icon': ':/resources/icons8-trash-restore-48.png',
                'slot': self.recycle_protocol_element,
                'show_when_flag': ElementTypeVisitiliyFlag.RECOVARABLE_ITEM,
                'separator_after': False,
            },
            'update_protocol_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'update_protocol_action',
                'text': 'Update protocol',
                'icon': ':/resources/icons8-upload-to-cloud-48.png',
                'short_cut_key_sequence': 'Ctrl+S',
                'slot': self.update_protocol,
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },

        }
        return generate_context_menu_from_scheme(context_menu, self.autolog_tree_viewer, menu_scheme)

    def generate_sample_list_view_context_menu(self) -> QMenu:
        """Generate the context menu for the sample list view"""

        context_menu = None

        menu_scheme = {
            'markdown_menu': {
                'type': QMenu,
                'obj': None,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'markdown_menu',
                'text': 'Markdown tools',
                'icon': ':/resources/icons8-markdown-48.png',
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': True,
            },
            'markdown_link_menu': {
                'type': QMenu,
                'obj': None,
                'parent_name': 'markdown_menu',
                'parent_obj': None,
                'name': 'markdown_link_menu',
                'text': 'Markdown link tools',
                'icon': ':/resources/icons8-tools-48.png',
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },
            'generic_link': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'markdown_link_menu',
                'obj': None,
                'name': 'generic_link',
                'text': 'Copy generic link to clipboard',
                'icon': ':/resources/icons8-hyperlink-48.png',
                'slot': lambda: QApplication.clipboard().setText('[link_text](link_URL)'),
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },
            'specific_link': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'markdown_link_menu',
                'obj': None,
                'name': 'specific_link',
                'text': 'Copy anchor link of this element to clipboard',
                'icon': ':/resources/icons8-hyperlink-48.png',
                'slot': self.copy_anchor_link_markdown_to_clipboard,
                'show_when_flag': ElementTypeVisitiliyFlag.ANCHORABLE_ITEM,
                'separator_after': False,
            },
            'markdown_image_menu': {
                'type': QMenu,
                'obj': None,
                'parent_name': 'markdown_menu',
                'parent_obj': None,
                'name': 'markdown_image_menu',
                'text': 'Markdown image tools',
                'icon': ':/resources/icons8-picture-48.png',
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': True,
            },
            'generic_image': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'markdown_image_menu',
                'obj': None,
                'name': 'generic_link',
                'text': 'Copy generic inline image to clipboard',
                'slot': lambda: QApplication.clipboard().setText('![image_alt_text](image_URL "image_title")'),
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },
            'markdown_selected_image_thumb': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'markdown_image_menu',
                'obj': None,
                'name': 'markdown_selected_image_thumb',
                'text': 'Copy inline thumbnail image to clipboard',
                'icon': ':/resources/icons8-picture-48.png',
                'slot': self.copy_image_markdown_to_clipboard,
                'show_when_flag': ElementTypeVisitiliyFlag.IMAGE_ITEM,
                'separator_after': False,
            },
            'open_browser_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'open_browser',
                'text': 'Open a browser window here...',
                'icon': ':/resources/icons8-folder-48.png',
                'slot': self.open_protocol_folder,
                'show_when_flag': ElementTypeVisitiliyFlag.PROTOCOL_ITEM,
                'separator_after': False,
            },
            'copy_sample_path_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'copy_sample_path',
                'text': 'Copy sample path',
                'icon': ':/resources/icons8-copy-link-48.png',
                'slot': self.copy_sample_path,
                'show_when_flag': ElementTypeVisitiliyFlag.SAMPLE,
                'separator_after': True,
            },
            'copy_full_path_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'copy_element_path',
                'text': 'Copy element path',
                'icon': ':/resources/icons8-copy-link-48.png',
                'slot': self.copy_element_path,
                'show_when_flag': ElementTypeVisitiliyFlag.PROTOCOL_ITEM,
                'separator_after': True,
            },
            'change_sample_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'change_sample',
                'text': 'Move item in another sample...',
                'icon': ':/resources/icons8-move-up-row-48.png',
                'slot': self.move_element_to_another_sample,
                'show_when_flag': ElementTypeVisitiliyFlag.MOVABLE_ITEM,
                'separator_after': False,
            },
            'rename_item_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'rename_action',
                'text': 'Rename item...',
                'icon': ':/resources/icons8-rename-48.png',
                'slot': self.rename_protocol_element,
                'show_when_flag': ElementTypeVisitiliyFlag.RENAMEBABLE_ITEM,
                'separator_after': False,
            },
            'recycle_menu': {
                'type': QMenu,
                'obj': None,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'recycle_menu',
                'text': 'Recycle / delete / recover',
                'icon': ':/resources/icons8-recycle-48.png',
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': True,
            },
            'delete_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'recycle_menu',
                'obj': None,
                'name': 'delete_action',
                'text': 'Delete item...',
                'icon': ':/resources/icons8-trash-can-48.png',
                'slot': self.delete_protocol_element,
                'show_when_flag': ElementTypeVisitiliyFlag.DELETABLE_ITEM,
                'separator_after': False,
            },
            'recycle_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'recycle_menu',
                'obj': None,
                'name': 'recycle_action',
                'text': 'Recycle item...',
                'icon': ':/resources/icons8-recycle-48.png',
                'slot': self.recycle_protocol_element,
                'show_when_flag': ElementTypeVisitiliyFlag.RECYCLABLE_ITEM,
                'separator_after': False,
            },
            'recover_action': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'recycle_menu',
                'obj': None,
                'name': 'recover_action',
                'text': 'Recover item from bin...',
                'icon': ':/resources/icons8-trash-restore-48.png',
                'slot': self.recycle_protocol_element,
                'show_when_flag': ElementTypeVisitiliyFlag.RECOVARABLE_ITEM,
                'separator_after': False,
            },
            'update_protocol_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'update_protocol_action',
                'text': 'Update protocol',
                'icon': ':/resources/icons8-upload-to-cloud-48.png',
                'slot': self.update_protocol,
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },

        }
        return generate_context_menu_from_scheme(context_menu, self.sample_list_view, menu_scheme)

    def generate_image_preview_context_menu(self) -> QMenu:
        """Generate the context menu for the image preview"""

        context_menu = None

        menu_scheme = {
            'open_external_viewer': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'open_external_viewer',
                'text': 'Show full screen in another window...',
                'icon': ':/resources/icons8-fullscreen-48.png',
                'slot': self.open_external_image_viewer,
                'show_when_flag': ElementTypeVisitiliyFlag.IMAGE_ITEM,
                'separator_after': False,
            },
            'open_browser_action': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'open_browser',
                'text': 'Open a browser window here...',
                'icon': ':/resources/icons8-folder-48.png',
                'slot': self.open_protocol_folder,
                'show_when_flag': ElementTypeVisitiliyFlag.ALWAYS,
                'separator_after': False,
            },
            'copy_preview': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'copy_preview',
                'text': 'Copy the thumbnail to clipboard',
                'icon': ':/resources/icons8-picture-48.png',
                'slot': self.copy_image_to_clipboard,
                'show_when_flag': ElementTypeVisitiliyFlag.IMAGE_ITEM,
                'separator_after': False,
            },
            'copy_path': {
                'type': QAction,
                'parent_obj': context_menu,
                'parent_name': 'root',
                'obj': None,
                'name': 'copy_path',
                'text': 'Copy image path to clipboard',
                'icon': ':/resources/icons8-copy-48.png',
                'slot': self.copy_element_path,
                'show_when_flag': ElementTypeVisitiliyFlag.IMAGE_ITEM,
                'separator_after': False,
            },
            'copy_image_url': {
                'type': QMenu,
                'obj': None,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'copy_image_url',
                'text': 'Copy image URLs',
                'icon': ':/resources/icons8-copy-link-48.png',
                'show_when_flag': ElementTypeVisitiliyFlag.IMAGE_ITEM,
                'separator_after': True,
            },
            'copy_image_tiff_url': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_image_url',
                'obj': None,
                'name': 'copy_image_tiff_url',
                'text': 'Copy TIFF URL to clipboard',
                'icon': ':/resources/icons8-copy-link-48.png',
                'slot': lambda: self.copy_image_url(autotools.ImageType.TIFF),
                'show_when_flag': ElementTypeVisitiliyFlag.MICROSCOPE_PIC,
                'separator_after': False,
            },
            'copy_image_png_url': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_image_url',
                'obj': None,
                'name': 'copy_image_png_url',
                'text': 'Copy PNG URL to clipboard',
                'icon': ':/resources/icons8-copy-link-48.png',
                'slot': lambda: self.copy_image_url(autotools.ImageType.PNG),
                'show_when_flag': ElementTypeVisitiliyFlag.IMAGE_ITEM,
                'separator_after': False,
            },
            'copy_image_thumb_url': {
                'type': QAction,
                'parent_obj': None,
                'parent_name': 'copy_image_url',
                'obj': None,
                'name': 'copy_image_thumb_url',
                'text': 'Copy thumbnail URL to clipboard',
                'icon': ':/resources/icons8-copy-link-48.png',
                'slot': lambda: self.copy_image_url(autotools.ImageType.THUMBNAIL),
                'show_when_flag': ElementTypeVisitiliyFlag.MICROSCOPE_PIC,
                'separator_after': False,
            },
        }
        return generate_context_menu_from_scheme(context_menu, self.image_preview, menu_scheme)

    def on_custom_edit_context_menu_request(self, pos: QPoint):
        """React to a request for context menu for the customization fields"""

        widget = self.sender()

        if widget.objectName() in ['description_input', 'extrainfo_input']:
            show_flag = CustomEditVisibilityFlag.MARKDOWN
            global_pos = widget.viewport().mapToGlobal(pos)
        elif widget.objectName() in ['caption_field']:
            show_flag = CustomEditVisibilityFlag.CAPTION
            global_pos = widget.mapToGlobal(pos)
        else:
            show_flag = CustomEditVisibilityFlag.NEVER
            global_pos = widget.mapToGlobal(pos)

        filter_context_menu(self.custom_edit_context_menu, show_flag)
        self.custom_edit_context_menu.exec(global_pos)

    def on_tree_context_menu_request(self, pos: QPoint):
        """
        React to a right click on the tree viewer.

        Parameters
        ----------
        pos: QPoint
            The position where the mouse was clicked.

        Returns
        -------

        """
        # this is the item where the mouse was clicked. If the mouse was clicked on the white area, then item will be
        # None.
        item = self.tree_model_proxy.mapToSource(self.autolog_tree_viewer.indexAt(pos))
        if item is None or not item.isValid():
            show_flag = ElementTypeVisitiliyFlag.NO_ITEM
        else:
            show_flag = autotools.get_visibility_from_item_type(item.data(UserRole.ITEM_TYPE))

        filter_context_menu(self.tree_viewer_context_menu, show_flag)
        self.tree_viewer_context_menu.exec(self.autolog_tree_viewer.viewport().mapToGlobal(pos))

    def on_metadata_context_menu_request(self, pos: QPoint):
        """
        React to a right click on the metadata table viewer.

        Parameters
        ----------
        pos: QPoint
            The position where the mouse was clicked.

        Returns
        -------

        """
        item = self.metadata_proxy_model.mapToSource(self.metadata_table.indexAt(pos))
        if item is None or not item.isValid():
            show_flag = MetadataVisibilityFlag.WITHOUT_ITEM
        else:
            show_flag = MetadataVisibilityFlag.WITH_ITEM

        filter_context_menu(self.metadata_table_context_menu, show_flag)
        self.metadata_table_context_menu.exec(self.metadata_table.viewport().mapToGlobal(pos))

    def on_sample_list_context_menu_request(self, pos: QPoint):
        """
        React to a right click on the tree viewer.

        Parameters
        ----------
        pos: QPoint
            The position where the mouse was clicked.

        Returns
        -------

        """
        # this is the item where the mouse was clicked. If the mouse was clicked on the white area, then item will be
        # None.
        item = self.tree_model_proxy.mapToSource(self.sample_list_view.indexAt(pos))
        if item is None or not item.isValid():
            show_flag = ElementTypeVisitiliyFlag.NO_ITEM
        else:
            show_flag = autotools.get_visibility_from_item_type(item.data(UserRole.ITEM_TYPE))

        filter_context_menu(self.sample_list_view_context_menu, show_flag)
        self.sample_list_view_context_menu.exec(self.sample_list_view.viewport().mapToGlobal(pos))

    def on_image_preview_context_menu_request(self, pos: QPoint):
        """React to a request for context menu for the image preview"""

        # get the item
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        if proxy_index.isValid():
            model_index = self.tree_model_proxy.mapToSource(proxy_index)
            current_item = self.tree_model.itemFromIndex(model_index)
        else:
            current_item = None

        if current_item is None:
            show_flag = ElementTypeVisitiliyFlag.NO_ITEM
        else:
            show_flag = autotools.get_visibility_from_item_type(current_item.data(UserRole.ITEM_TYPE))

        filter_context_menu(self.image_preview_context_menu, show_flag)
        self.image_preview_context_menu.exec(self.image_preview.mapToGlobal(pos))

    def copy_metadata_to_clipboard(self, what: str):
        """Copy the currently selected metadata item to the clipboard"""
        text_to_be_copied = self.get_metadata_text(what)
        if text_to_be_copied:
            QApplication.clipboard().setText(text_to_be_copied)

    def save_metadata_to_file(self, what: str = 'all'):
        """Save the currently selected metadata item to a file"""
        text_to_be_copied = self.get_metadata_text(what)
        if text_to_be_copied:
            directory = Path.home() / Path('Documents')
            returnpath = QFileDialog.getSaveFileName(self, 'Metadata file', directory=str(directory),
                                                     filter='CSV file (*.csv)')
            if returnpath:
                csvfile = Path(returnpath[0])
                with open(csvfile, 'w') as f:
                    f.write(text_to_be_copied)

    def get_metadata_text(self, what: str) -> str:
        """
        Get the currently selected metadata item as formatted text

        what: str
            Select what kind of information.
            Possible values:
            'single_value': get only the value of the currently selected row
            'single_pair': get both key and value of the currently selected row
            'all': get all keys and values
        """
        current_proxy_index = self.metadata_table.selectionModel().currentIndex()
        current_index = self.metadata_proxy_model.mapToSource(current_proxy_index)
        if what.lower() == 'single_value':
            if current_index.column() == 0:  # the user selected a key, but we want to have the value
                value_index = self.metadata_model.index(current_index.row(), 1, current_index.parent())
                text_to_be_copied = value_index.data(Qt.DisplayRole)
            else:  # the user was selecting a value.
                text_to_be_copied = current_index.data(Qt.DisplayRole)
        elif what.lower() == 'single_pair':
            if current_index.column() == 0:  # the user is selecting a key
                key_index = current_index
                value_index = self.metadata_model.index(current_index.row(), 1, current_index.parent())
            else:  # the user is selecting a value
                key_index = self.metadata_model.index(current_index.row(), 0, current_index.parent())
                value_index = current_index

            text_to_be_copied = f'{key_index.data(Qt.DisplayRole)}:{chr(9)} {value_index.data(Qt.DisplayRole)}'

        elif what.lower() == 'all':
            text_to_be_copied = ''
            for row in range(self.metadata_model.rowCount()):
                key_index = self.metadata_model.index(row, 0, self.metadata_table.rootIndex())
                value_index = self.metadata_model.index(row, 1, self.metadata_table.rootIndex())
                text_to_be_copied += f'{key_index.data(Qt.DisplayRole)}:{chr(9)} {value_index.data(Qt.DisplayRole)}{chr(10)}'
        else:
            text_to_be_copied = ''

        return text_to_be_copied

    def copy_image_markdown_to_clipboard(self):
        """Copy the markdown template for an image in the clipboard"""

        link = self.get_image_url('thumbnail')
        mark = f'![image_alt_text]({link})'
        QApplication.clipboard().setText(mark)

    def copy_anchor_link_markdown_to_clipboard(self):
        """Copy the markdown template for an anchor link in the clipboard"""

        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        current_item = self.tree_model.itemFromIndex(model_index)
        current_item_type = current_item.data(UserRole.ITEM_TYPE)
        if current_item_type == ElementType.SECTION:
            section_name = current_item.data(Qt.DisplayRole)
            name = section_name
            if section_name == 'Introduction':
                link = '#intro'
            elif section_name == 'Samples':
                link = '#samplelist'
            elif section_name == 'Conclusion':
                link = '#conclusion'
            elif section_name == 'Attachments':
                link = '#attachments'
            else:
                link = '#link'
        elif current_item_type == ElementType.SAMPLE:
            name = current_item.data(UserRole.SAMPLE_FULL_NAME)
            link = f'#{name}'
        elif current_item_type in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
            # anchor is sample_full_name/microscope_pic_filename
            sample_full_name = current_item.parent().data(UserRole.SAMPLE_FULL_NAME)
            element_name = current_item.text()
            name = f'{sample_full_name}/{element_name}'
            link = f'#{name}'
        elif current_item_type in [ElementType.NAVIGATION_PIC, ElementType.ATTACHMENT_FILE]:
            name = current_item.text()
            link = f'#{name}'
        else:
            name = 'name'
            link = '#link'

        QApplication.clipboard().setText(f'[{name}]({link})')

    def edit_custom_text(self, edit_type: str):
        """Edit the text in the QPlainText"""
        widget = QApplication.focusWidget()
        if widget is None:
            return

        # exclude the caption input because this is just a line edit and not a PlainTextEdit
        if widget.objectName() not in ['description_input', 'extrainfo_input']:
            return

        # if we got here, it means that the widget in focus is either the description_input or the extrainfo_input
        # so it is ok to continue with text edit.
        cursor = widget.textCursor()
        if edit_type.lower() == 'subscript':
            left_text = '<sub>'
            right_text = '</sub>'
        elif edit_type.lower() == 'superscript':
            left_text = '<sup>'
            right_text = '</sup>'
        elif edit_type.lower() == 'bold':
            left_text = '**'
            right_text = '**'
        elif edit_type.lower() == 'italic':
            left_text = '*'
            right_text = '*'
        elif edit_type.lower() == 'underline':
            left_text = '<u>'
            right_text = '</u>'
        elif edit_type.lower() == 'strikeout':
            left_text = '<del>'
            right_text = '</del>'
        elif edit_type.lower() == 'bullet':
            left_text = ''
            right_text = (f'{chr(10)}'
                          f'*  Item 1{chr(10)}{chr(10)}'
                          f'*  Item 2{chr(10)}{chr(10)}'
                          f'*  Item 3{chr(10)}{chr(10)}')
        elif edit_type.lower() == 'number':
            left_text = ''
            right_text = (f'{chr(10)}'
                          f'1.  Item 1{chr(10)}{chr(10)}'
                          f'2.  Item 2{chr(10)}{chr(10)}'
                          f'3.  Item 3{chr(10)}{chr(10)}')
        elif edit_type.lower() == 'link':
            left_text = ''
            right_text = '[link_name](link_url)'
        else:
            left_text = ''
            right_text = ''
        if cursor.hasSelection():
            cursor.insertText(f'{left_text}{cursor.selectedText()}{right_text}')
        else:
            widget.insertPlainText(f'{left_text}{right_text}')

    @Slot(str)
    def tree_filter(self, re: str) -> None:
        """Apply the filter to the tree model"""
        self.tree_model_proxy.setFilterRegExp(QRegExp(re, Qt.CaseInsensitive, QRegExp.FixedString))

    @Slot(str)
    def metadata_filter(self, re: str) -> None:
        """
        Slot for filtering the metadata table view.

        The filtering is done using a regular expression in a case-insensitive manner and using a fixed string syntax.
        FixedString means that no wildcards or special matching characters will be used in the matching and the string
        will be matched as it is.

        Parameters
        ----------
        re: str
            The regular expression used for the matching.

        Returns
        -------
        None
        """
        self.metadata_proxy_model.setFilterRegExp(QRegExp(re, Qt.CaseInsensitive, QRegExp.FixedString))

    @Slot(QModelIndex, int, int)
    def new_rows_added(self, parent: QModelIndex, start: int, stop: int) -> None:
        """React to the addition of a new row to the model"""

        for row in range(start, stop + 1):
            new_row = self.tree_model.index(row, 0, parent)

            # Actually we are interested only if the new item is a sample. If so we have to check if the sample is
            # already present in the sample selector, otherwise we need to add it.
            if new_row.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                if self.sample_selector.findText(new_row.data(UserRole.SAMPLE_FULL_NAME)) != -1:
                    self.sample_selector.addItem(new_row.data(UserRole.SAMPLE_FULL_NAME))

    def open_protocol_webpage(self):
        url = self.autolog.get_protocol_url()
        webbrowser.open(url, new=0, autoraise=True)

    def open_protocol_folder(self):
        """
        Open a resource browser pointing to the monitored folder or to the folder where the selected resource is.

        Returns
        -------
        None.

        """
        if isinstance(self.parent, MainWindow):
            # if the protocol editor dialog was called from the MainWindow, then we can take the protocol folder from
            # there without risking confusion about mirroring or not.
            base_path = self.parent.protocol_folder_path
        else:
            # should it not be the case, then just take the path from the autolog instance.
            base_path = self.autolog.path

        # get the item
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        current_item = self.tree_model.itemFromIndex(model_index)

        current_item_type = current_item.data(UserRole.ITEM_TYPE)
        if current_item_type in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
            # its parent must be a sample or a subsample
            parent_sample_item = current_item.parent()
            parent_sample_path = Path(parent_sample_item.data(UserRole.SAMPLE_FULL_NAME))
            path = base_path / parent_sample_path
        elif current_item_type == ElementType.SAMPLE:
            path = base_path / Path(current_item.data(UserRole.SAMPLE_FULL_NAME))
        elif current_item_type in [ElementType.ATTACHMENT_FILE, ElementType.OPTICAL_PIC]:
            if current_item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                path = base_path / Path(current_item.parent().data(UserRole.SAMPLE_FULL_NAME))
            else:
                path = base_path
        else:
            path = base_path

        command = f'explorer {str(path)}'
        subprocess.Popen(command.split())

    def copy_sample_path(self):
        """Copy the path of a sample to the clipboard."""

        if isinstance(self.parent, MainWindow):
            # if the protocol editor dialog was called from the MainWindow, then we can take the protocol folder from
            # there without risking confusion about mirroring or not.
            base_path = self.parent.protocol_folder_path
        else:
            # should it not be the case, then just take the path from the autolog instance.
            base_path = self.autolog.path

        # get the item
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        current_item = self.tree_model.itemFromIndex(model_index)
        current_item_type = current_item.data(UserRole.ITEM_TYPE)
        if current_item_type in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
            # its parent must be a sample or a subsample
            parent_sample_item = current_item.parent()
            parent_sample_path = Path(parent_sample_item.data(UserRole.SAMPLE_FULL_NAME))
            path = base_path / parent_sample_path
        elif current_item_type == ElementType.SAMPLE:
            path = base_path / Path(current_item.data(UserRole.SAMPLE_FULL_NAME))
        else:
            path = base_path

        QApplication.clipboard().setText(str(path))

    def copy_element_path(self):
        """Copy the path of a protocol element to the clipboard."""
        if isinstance(self.parent, MainWindow):
            # if the protocol editor dialog was called from the MainWindow, then we can take the protocol folder from
            # there without risking confusion about mirroring or not.
            base_path = self.parent.protocol_folder_path
        else:
            # should it not be the case, then just take the path from the autolog instance.
            base_path = self.autolog.path

        # get the item
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        current_item = self.tree_model.itemFromIndex(model_index)
        current_item_type = current_item.data(UserRole.ITEM_TYPE)
        if current_item_type in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
            # its parent must be a sample or a subsample
            parent_sample_item = current_item.parent()
            parent_sample_path = Path(parent_sample_item.data(UserRole.SAMPLE_FULL_NAME))
            path = base_path / parent_sample_path / Path(current_item.data(Qt.DisplayRole))
        elif current_item_type == ElementType.SAMPLE:
            path = base_path / Path(current_item.data(UserRole.SAMPLE_FULL_NAME))
        elif current_item_type == ElementType.NAVIGATION_PIC:
            path = base_path / Path(current_item.data(Qt.DisplayRole))
        else:
            path = base_path / Path(current_item.data(Qt.DisplayRole))

        QApplication.clipboard().setText(str(path))

    def get_image_url(self, image_type: str | autotools.ImageType = 'tiff') -> str:
        """Return the image URL"""

        if isinstance(image_type, str):
            try:
                image_type = autotools.ImageType(image_type)
            except ValueError:
                log.warning('The provided image_type is not recognized.')
                return ''

        # get the base path
        base_path = self.autolog.path

        # get the item from the tree viewer
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        current_item = self.tree_model.itemFromIndex(model_index)
        current_item_type = current_item.data(UserRole.ITEM_TYPE)

        # get the link depending on the image_type
        if current_item_type == ElementType.MICROSCOPE_PIC:
            # pic_id = current_item.data(UserRole.PIC_ID)
            parent_item = current_item.parent()
            parent_name = parent_item.data(UserRole.SAMPLE_FULL_NAME)
            parent_path = Path(parent_name)
            path = base_path / parent_path / Path(current_item.data(Qt.DisplayRole))
            if image_type == autotools.ImageType.TIFF:
                link = self.autolog.samples[parent_name].images[str(path)].params['tiffurl']
            elif image_type == autotools.ImageType.PNG:
                link = self.autolog.samples[parent_name].images[str(path)].params['pngurl']
            elif image_type == autotools.ImageType.THUMBNAIL:
                link = self.autolog.samples[parent_name].images[str(path)].params['thumburl']
            else:
                link = ''
        elif current_item_type == ElementType.NAVIGATION_PIC:
            nav_image_name = current_item.data(Qt.DisplayRole)
            nav_image_path = base_path / Path(nav_image_name)
            link = self.convert_path_to_uri(nav_image_path)
        elif current_item_type == ElementType.OPTICAL_PIC:
            link = current_item.data(UserRole.OPTICAL_IMAGE_URL)
        else:
            link = ''

        return link

    def open_external_image_viewer(self):
        """Open the current image in an external viewer"""
        base_path = self.autolog.path
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        current_item = self.tree_model.itemFromIndex(model_index)
        current_item_type = current_item.data(UserRole.ITEM_TYPE)
        if current_item_type == ElementType.MICROSCOPE_PIC:
            parent_item = current_item.parent()
            parent_name = parent_item.data(UserRole.SAMPLE_FULL_NAME)
            parent_path = Path(parent_name)
            path = base_path / parent_path / Path(current_item.data(Qt.DisplayRole))
        elif current_item_type == ElementType.NAVIGATION_PIC:
            nav_image_name = current_item.data(Qt.DisplayRole)
            path = base_path / Path(nav_image_name)
        elif current_item_type == ElementType.OPTICAL_PIC:
            path = current_item.data(UserRole.OPTICAL_IMAGE_PATH)
        else:
            path = None

        if path:
            command = f'explorer "{str(path)}"'
            subprocess.Popen(command)

    def copy_image_url(self, image_type: str | autotools.ImageType = 'tiff'):
        """Copy the current image URL to the clipboard"""
        link = self.get_image_url(image_type)
        QApplication.clipboard().setText(link)

    def copy_image_to_clipboard(self):
        """Copy the current image thumbnail to the clipboard"""
        QApplication.clipboard().setPixmap(self.image_preview.pixmap())

    @Slot(str)
    def change_sample_list_root(self, sample_full_name: str):
        """
        Change the table view root item.

        The sample table view is rooted to the selected sample and this is automatically updated every time the user
        select a new item from the tree viewer or when the sample selector value is changed.

        When an item not belonging to a sample is selected, the sample table is rooted to the protocol root.

        Parameters
        ----------
        sample_full_name: str
            The sample full name to be set as root item of the table view.

        Returns
        -------
        None
        """
        if self.sample_selector.count() == 0:
            items = self.tree_model.findItems("Samples", QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            if len(items) > 1:
                log.error('More than one Samples section found (size %s)', len(items))
            elif len(items) == 0:
                self.sample_list_view.setRootIndex(self.tree_model_proxy.mapFromSource(self.rootNode.index()))
            else:
                self.sample_list_view.setRootIndex(self.tree_model_proxy.mapFromSource(items[0].index()))
        elif sample_full_name == 'Protocol':
            self.sample_list_view.setRootIndex(self.tree_model_proxy.mapFromSource(self.rootNode.index()))
        else:
            sample_last_name = sample_full_name.split('/')[-1]
            items = self.tree_model.findItems(sample_last_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            good_item = None
            for item in items:
                if item.data(UserRole.SAMPLE_FULL_NAME) == sample_full_name:
                    good_item = item
                    break
            if good_item:
                self.sample_list_view.setRootIndex(self.tree_model_proxy.mapFromSource(good_item.index()))

    @Slot()
    def collapse_all_elements(self):
        """
        Collapse all elements in the tree view.

        Returns
        -------
        None
        """
        self.autolog_tree_viewer.collapseAll()

    @Slot()
    def expand_all_elements(self):
        """
        Expand all elements in the tree view.

        Returns
        -------
        None
        """
        self.autolog_tree_viewer.expandAll()

    def media_error_handler(self):
        """
        Handle error with media player
        """
        errors = {QMediaPlayer.NoError: 'No error',
                  QMediaPlayer.ResourceError: 'A media resource could not be resolved',
                  QMediaPlayer.FormatError: 'The format of a media resource is not supported',
                  QMediaPlayer.NetworkError: 'A network_path error occurred',
                  QMediaPlayer.AccessDeniedError: 'There are not the appropriate permissions to play a media resource',
                  QMediaPlayer.ServiceMissingError: 'A valid playback service wa not found, playback cannot proceed'}

        mp_statuses = {QMediaPlayer.StoppedState: 'Stopped',
                       QMediaPlayer.PlayingState: 'Playing',
                       QMediaPlayer.PausedState: 'Paused'}

        md_statuses = {QMediaPlayer.UnknownMediaStatus: 'The status of the media cannot be determined.',
                       QMediaPlayer.NoMedia: 'There is no current media. The player is in the stopped state.',
                       QMediaPlayer.LoadingMedia: 'The current media is being loaded.',
                       QMediaPlayer.LoadedMedia: 'The current media has been loaded. The player is in the stopped '
                                                 'state.',
                       QMediaPlayer.StalledMedia: 'Playback of the current media has stalled.',
                       QMediaPlayer.BufferingMedia: 'The player is buffering but has enough data for playback.',
                       QMediaPlayer.BufferedMedia: 'The player has fully buffered the current media.',
                       QMediaPlayer.EndOfMedia: 'Playback has reached the end of the current media.',
                       QMediaPlayer.InvalidMedia: 'The current media cannot be played.'
                       }

        error_no = self.media_player.error()
        mp_status = self.media_player.state()
        md_status = self.media_player.mediaStatus()
        log.error('There was an error handling the current media.')
        log.error('Error: %s' % errors.get(error_no))
        log.error('Media Player Status: %s' % mp_statuses.get(mp_status))
        log.error('Media status: %s' % md_statuses.get(md_status))
        self.preview_stack.setCurrentIndex(0)
        self.image_preview.setText('There was a problem reproducing the video. See log for more details.')
        if md_status == QMediaPlayer.InvalidMedia:
            log.error('Have you installed the CODEC package?')

    def play(self):
        """
        Start the reproduction of the current media

        Returns
        -------
        None
        """
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def media_state_changed(self, state):
        """
        React to a change in the media player state.

        In case the media player is in playing state, the control button icon will be changed in pause.
        In case the media player is in paused state, the control button icon will be changed in play.

        Parameters
        ----------
        state : QMediaPlayer.State
            There are three possible states:
            1. Stopped.
            2. Playing.
            3. Paused.
        """
        play_icon = QtGui.QIcon()
        play_icon.addPixmap(QtGui.QPixmap(":/resources/icons8-play-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pause_icon = QtGui.QIcon()
        pause_icon.addPixmap(QtGui.QPixmap(":/resources/icons8-pause-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.video_play_button.setIcon(pause_icon)
        else:
            self.video_play_button.setIcon(play_icon)

    def position_changed(self, position):
        """
        React to a change in the media position.

        Parameters
        ----------
        position: float
            The new position
        """
        self.video_slider.setValue(position)

    def duration_changed(self, duration):
        """
        React to a change in the media duration.

        Adapt the slider to the new duration

        Parameters
        ----------
        duration: float
            The duration

        Returns
        -------
        None
        """
        self.video_slider.setRange(0, duration)

    def set_position(self, position):
        """
        React to a change of the slider position.

        Parameters
        ----------
        position:
            The selected position on the slider.
        """
        self.media_player.setPosition(position)

    def clear_fields(self):
        """
        Clear all the fields upon windows opening.

        This method is called just before the ProtocolEditor window is shown.
        It clears the selection on the TreeView and reset the three textual
        fields.

        Returns
        -------
        None.

        """
        self.autolog_tree_viewer.selectionModel().clearSelection()
        self.caption_field.setText('')
        self.description_input.document().setPlainText('')
        self.extrainfo_input.document().setPlainText('')
        self.selected_element_label.setText('No item selected')
        if self.autolog_tree_viewer.selectionModel().currentIndex().isValid():
            self.update_values(self.autolog_tree_viewer.selectionModel().currentIndex())

    @Slot(autoprotocol.Protocol)
    def change_autolog(self, autolog):
        """
        Change the reference to the autolog.

        When new parameters are sent to the worker, it is very likely that a new autolog reference is generated.
        If the protocol editor was already created, then the main window needs to inform it that the autolog reference
        is changed.

        After setting the autolog reference, we need to reset the content of the model.

        Parameters
        ----------
        autolog : autoprotocol.Protocol
            The reference of the current autolog.

        Returns
        -------
        None.

        """
        log.debug('Changing the autolog reference')
        self.autolog = autolog
        self.reset_content()

    def refresh_view(self):
        """
        Regenerate the content of the TreeModel.

        This function is used to assure that the model content is update and
        what is shown in the editor window corresponds to the protocol model.

        Returns
        -------
        None.

        """
        self.tree_model_proxy.sort(0, Qt.AscendingOrder)

    def generate_model(self):
        """
        Generate the data model.

        We use a QStandardItemModel.

        This method generates the whole model standard from the autolog instance

        Returns
        -------
        None.

        """
        introduction_section = SectionItem('Introduction')
        introduction_section.get_data_from_yaml(self.autolog.yamlDict)
        self.rootNode.appendRow(introduction_section)

        # a navigation camera section exists only if the protocol is of a
        # Quattro microscope.
        if isinstance(self.autolog, autoprotocol.QuattroELOGProtocol):
            navcam_section = SectionItem('Navigation images')
            navcam_section.get_data_from_yaml(self.autolog.yamlDict)

            for navpic in self.autolog.navcamimages:
                navpic_item = NavPicItem(Path(navpic).name, str(Path(navpic)))
                navpic_item.get_data_from_yaml(self.autolog.yamlDict)
                navcam_section.appendRow(navpic_item)

            self.rootNode.appendRow(navcam_section)

        optical_images_section = SectionItem('Optical images')
        optical_images_section.get_data_from_yaml(self.autolog.yamlDict)
        for optical_image in self.autolog.optical_images:
            optical_image_item = OpticalImageItem(optical_image)
            optical_image_item.get_data_from_yaml(self.autolog.yamlDict)
            optical_images_section.appendRow(optical_image_item)
        self.rootNode.appendRow(optical_images_section)

        sample_section = SectionItem('Samples')
        sample_section.get_data_from_yaml(self.autolog.yamlDict)
        self.sample_selector.addItem('Protocol')

        # in the sample dictionary, the sample keys are the
        # sample full_name
        for full_name, sample in self.autolog.samples.items():
            if sample.parent is None:
                log.debug('Adding top level sample %s' % full_name)
                # we got a top level sample. add this and process
                # all its child
                entry = SampleItem(full_name)
                entry.get_data_from_yaml(self.autolog.yamlDict)
                for key, image in sample.images.items():
                    pic = MicroPicItem(Path(key).name, image.key, image.params['thumbfilename'])
                    pic.get_data_from_yaml(self.autolog.yamlDict)
                    entry.appendRow(pic)
                for key, video in sample.videos.items():
                    video_item = VideoItem(key=key, path=video.get('path'),
                                           url=video.get('url'), txt=video.get('filename'))
                    video_item.get_data_from_yaml(self.autolog.yamlDict)
                    entry.appendRow(video_item)
                for key, attachment in sample.attachments.items():
                    attach_item = AttachmentItem(key)
                    attach_item.get_data_from_yaml(self.autolog.yamlDict)
                    entry.appendRow(attach_item)
                for key in sample.optical_images.keys():
                    optical_image_item = OpticalImageItem(key)
                    optical_image_item.get_data_from_yaml(self.autolog.yamlDict)
                    entry.appendRow(optical_image_item)

                sample_section.appendRow(entry)
                self.sample_selector.addItem(full_name)
                if len(sample.subsamples) != 0:
                    self.add_subsample_recursively(sample.subsamples, entry)

        self.rootNode.appendRow(sample_section)

        conclusion_section = SectionItem('Conclusion')
        conclusion_section.get_data_from_yaml(self.autolog.yamlDict)
        self.rootNode.appendRow(conclusion_section)

        attachment_section = SectionItem('Attachments')
        last_element = attachment_section
        for key in self.autolog.attachments.keys():
            attachment = AttachmentItem(key)
            last_element = attachment
            attachment.get_data_from_yaml(self.autolog.yamlDict)
            attachment_section.appendRow(attachment)

        attachment_section.get_data_from_yaml(self.autolog.yamlDict)
        self.rootNode.appendRow(attachment_section)

        # since we have regenerated the model the persistent model indexes pointing to the last inserted and last
        # selected items will become invalid, so for the last inserted we just use either the last attachment or the
        # attachment section itself. For the last selected, it makes no sense to have something assign, so we put it to
        # None and wait for the user next selection.
        last_element_index = self.tree_model.indexFromItem(last_element)
        last_element_proxy = self.tree_model_proxy.mapFromSource(last_element_index)
        self.tree_model_last_inserted_item = QPersistentModelIndex(last_element_proxy)
        self.tree_model_last_selected_item = None

    def add_subsample_recursively(self, sample_list, parent_entry):
        """
        Add a subsample list to a parent sample recursively.

        When building the protocol model, all subsample of a parent must be
        registered and this procedure must be repeated recursively.

        Parameters
        ----------
        sample_list : list
            The list of subsamples belonging to the parent sample.
        parent_entry : SectionItem | SampleItem
            The section item where the subsamples must be appended.

        Returns
        -------
        None.

        """
        # sample_list stores sample_full_names
        for sample_full_name in sample_list:
            if sample_full_name in self.autolog.samples.keys():
                sample = self.autolog.samples[sample_full_name]
                log.debug('Adding subsample %s to %s' % (sample_full_name, sample.parent))
                entry = SampleItem(sample_full_name)
                entry.get_data_from_yaml(self.autolog.yamlDict)
                for key, image in sample.images.items():
                    pic = MicroPicItem(Path(key).name, image.key, image.params['thumbfilename'])
                    pic.get_data_from_yaml(self.autolog.yamlDict)
                    entry.appendRow(pic)
                for key, video in sample.videos.items():
                    video_item = VideoItem(key=key, path=video.get('path'),
                                           url=video.get('url'), txt=video.get('filename'))
                    video_item.get_data_from_yaml(self.autolog.yamlDict)
                    entry.appendRow(video_item)
                for key, attach in sample.attachments.items():
                    attach_item = AttachmentItem(key)
                    attach_item.get_data_from_yaml(self.autolog.yamlDict)
                    entry.appendRow(attach_item)
                for key in sample.optical_images.keys():
                    optical_image_item = OpticalImageItem(key)
                    optical_image_item.get_data_from_yaml(self.autolog.yamlDict)
                    entry.appendRow(optical_image_item)
                if len(sample.subsamples) != 0:
                    self.add_subsample_recursively(sample.subsamples, entry)
                parent_entry.appendRow(entry)
                self.sample_selector.addItem(sample_full_name)

    @Slot(ElementType, str, str)
    def add_element(self, element_type, element_name, parent_name):  # noqa: C901
        """
        Add an element to the model.

        Slot function connected to the addition of a new element to the model

        Parameters
        ----------
        element_type : autotools.ElementType
            This enumerator contains all possible element types
        element_name : string
            For NavPic and MicroPic the element name is the full path of the
            image.
            For Sample, it is just the sample name
        parent_name : string
            For MicroPic, the sample name.
            For Sample, the parent name or 'Samples' for top level samples.

        Raises
        ------
        ValueError
            Raised if more than one parent section is found in the model

        Returns
        -------
        None.

        """
        new_item = None
        if element_type == ElementType.NAVIGATION_PIC:
            # element_name must be the full path
            path = Path(element_name)
            name = path.name

            # the parent name must be Navigation images
            items = self.tree_model.findItems('Navigation images',
                                              QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            if len(items) == 1:
                new_item = NavPicItem(name, str(path))
                new_item.get_data_from_yaml(self.autolog.yamlDict)
                items[0].appendRow(new_item)
            else:
                raise ValueError('More than one navigation image section found')

        elif element_type == ElementType.MICROSCOPE_PIC:
            # element_name must be the full path
            if not isinstance(element_name, Path):
                path = Path(element_name)
            else:
                path = element_name

            # take the picture name from the full path
            name = path.name

            # the parent name is a sample_full_name
            sample_full_name = parent_name
            # take the sample_last_name
            sample_last_name = parent_name.split('/')[-1]

            # to build the MicroPicItem we need:
            #   the image reference,
            #   the image_id
            #   the thumbfilename
            image = self.autolog.samples[sample_full_name].images[str(path)]
            image_id = image.key
            thumb = image.params['thumbfilename']

            new_item = MicroPicItem(name, image_id, thumb)
            new_item.get_data_from_yaml(self.autolog.yamlDict)

            # we need to find the sample to append this MicroPicItem
            # the search works on sample_last_name, so there could be many
            items = self.tree_model.findItems(sample_last_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)

            # there might be more than one with the same last name
            # but only one is the good one with the exact full name
            good_item = None
            for item in items:
                if item.data(UserRole.SAMPLE_FULL_NAME) == sample_full_name:
                    good_item = item
                    break
            good_item.appendRow(new_item)

        elif element_type == ElementType.VIDEO_FILE:
            # element_name is the path / key
            # parent_name is the sample_full_name
            parent_last_name = parent_name.split('/')[-1]
            key = str(element_name)
            txt = self.autolog.samples[parent_name].videos[key].get('filename')
            url = self.autolog.samples[parent_name].videos[key].get('url')
            path = self.autolog.samples[parent_name].videos[key].get('path')
            new_item = VideoItem(txt=txt, key=key, url=url, path=path)
            new_item.get_data_from_yaml(self.autolog.yamlDict)

            # we need to find the sample to append this VideoItem
            # the search works on parent_last_name, so there could be many
            items = self.tree_model.findItems(parent_last_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)

            # there might be more than one with the same last name
            # but only one is the good one with the exact full name
            good_item = None
            for item in items:
                if item.data(UserRole.SAMPLE_FULL_NAME) == parent_name:
                    good_item = item
                    break
            good_item.appendRow(new_item)

        elif element_type == ElementType.SAMPLE:
            if parent_name == 'Samples':
                # we are adding a top level sample
                new_item = SampleItem(element_name)
                new_item.get_data_from_yaml(self.autolog.yamlDict)
                items = self.tree_model.findItems(parent_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
                # this must be just one, because we have a top level sample
                if len(items) != 1:
                    log.critical('More than 1 sample main section.')
                    raise ValueError
                else:
                    items[0].appendRow(new_item)
                    self.sample_selector.addItem(new_item.data(UserRole.SAMPLE_FULL_NAME))
            else:
                parent_full_name = parent_name
                parent_last_name = parent_name.split('/')[-1]
                sample_full_name = element_name

                new_item = SampleItem(sample_full_name)
                new_item.get_data_from_yaml(self.autolog.yamlDict)
                items = self.tree_model.findItems(parent_last_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive,
                                                  0)

                # this time items can have more than 1 item because last names are not
                # unique, but full names are!
                good_item = None
                for item in items:
                    if item.data(UserRole.SAMPLE_FULL_NAME) == parent_full_name:
                        good_item = item
                        break
                good_item.appendRow(new_item)
                self.sample_selector.addItem(new_item.data(UserRole.SAMPLE_FULL_NAME))

        elif element_type == ElementType.ATTACHMENT_FILE:
            # the element name is the full path
            # the parent name is "Attachments" for protocol wide attachments
            # or the sample full name for sample attachments
            if parent_name == 'Attachments':
                items = self.tree_model.findItems(parent_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
                if len(items) == 1:
                    new_item = AttachmentItem(element_name)
                    new_item.get_data_from_yaml(self.autolog.yamlDict)
                    items[0].appendRow(new_item)
                else:
                    raise ValueError('More than one attachment section found')
            else:
                sample_full_name = parent_name
                sample_last_name = parent_name.split('/')[-1]

                # build the attachment
                new_item = AttachmentItem(element_name)
                new_item.get_data_from_yaml(self.autolog.yamlDict)

                # search for the sample
                items = self.tree_model.findItems(sample_last_name,
                                                  QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
                good_item = None
                for item in items:
                    if item.data(UserRole.SAMPLE_FULL_NAME) == sample_full_name:
                        good_item = item
                        break
                good_item.appendRow(new_item)

        elif element_type == ElementType.OPTICAL_PIC:
            # the element name is the full path,
            # the parent name if 'Optical images' for protocol wide images
            # or the sample full name for sample wide images
            if parent_name == 'Optical images':
                items = self.tree_model.findItems(parent_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
                if len(items) == 1:
                    new_item = OpticalImageItem(element_name)
                    new_item.get_data_from_yaml(self.autolog.yamlDict)
                    items[0].appendRow(new_item)
                else:
                    raise ValueError('More than one optical image section found')
            else:
                sample_full_name = parent_name
                sample_last_name = parent_name.split('/')[-1]

                # build the attachment
                new_item = OpticalImageItem(element_name)
                new_item.get_data_from_yaml(self.autolog.yamlDict)

                # search for the sample
                items = self.tree_model.findItems(sample_last_name,
                                                  QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
                good_item = None
                for item in items:
                    if item.data(UserRole.SAMPLE_FULL_NAME) == sample_full_name:
                        good_item = item
                        break
                good_item.appendRow(new_item)

        elif element_type == ElementType.YAML_FILE:
            log.debug('new yaml file available')
            # TODO: force refresh all items from file.

        if new_item:
            model_index = self.tree_model.indexFromItem(new_item)
            proxy_index = self.tree_model_proxy.mapFromSource(model_index)
            self.refresh_view()
            self.autolog_tree_viewer.scrollTo(proxy_index)
            self.tree_model_last_inserted_item = QPersistentModelIndex(proxy_index)
            if self.autolog_tree_viewer.selectionModel().currentIndex().isValid():
                self.update_metadata_table(self.autolog_tree_viewer.selectionModel().currentIndex())

    @Slot(ElementType, str, str)
    def remove_element(self, element_type, element_name, parent_name):  # noqa: C901
        """
        Remove an element from the model.

        Slot function connected to the removal of an existing element to the model

        Parameters
        ----------
        element_type : autotools.ElementType
            This enumerator contains all possible element types
        element_name : string
            For NavPic and MicroPic the element name is the full path of the
            image.
            For Sample, it is just the sample name
        parent_name : string
            For MicroPic, the sample name.
            Useless for NavPic and Sample.

        Returns
        -------
        None.

        """
        if element_type in [ElementType.NAVIGATION_PIC, ElementType.MICROSCOPE_PIC]:
            name = Path(element_name).name
            items = self.tree_model.findItems(
                name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            if len(items) == 1:
                item = items[0]
                parent_index = item.parent().index()
                item.model().removeRow(item.row(), parent_index)
            elif len(items) > 1:
                # log.error('Expected only one element with name %s.' % name)
                # log.error('Found instead %s' % len(items))
                # log.warning('Removing all of them and verify the protocol.')
                for item in items:
                    if item.parent().text() == parent_name:
                        parent_index = item.parent().index()
                        item.model().removeRow(item.row(), parent_index)

        elif element_type == ElementType.VIDEO_FILE:
            # element_name is the full path/key
            key = element_name
            name = Path(element_name).name
            sample_full_name = parent_name
            items = self.tree_model.findItems(name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            good_item = None
            for item in items:
                if item.data(UserRole.VIDEO_KEY) == key:
                    good_item = item
                    break
            parent_index = good_item.parent().index()
            good_item.model().removeRow(good_item.row(), parent_index)

        elif element_type == ElementType.SAMPLE:

            sample_full_name = element_name
            sample_last_name = sample_full_name.split('/')[-1]
            items = self.tree_model.findItems(sample_last_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            good_item = None
            for item in items:
                if item.data(UserRole.SAMPLE_FULL_NAME) == sample_full_name:
                    good_item = item
                    break
            parent_index = good_item.parent().index()
            good_item.model().removeRow(good_item.row(), parent_index)
            index = self.sample_selector.findText(sample_full_name, QtCore.Qt.MatchExactly)
            if index != -1:
                self.sample_selector.removeItem(index)

        elif element_type == ElementType.ATTACHMENT_FILE:
            key = element_name
            name = Path(element_name).name

            items = self.tree_model.findItems(name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            good_item = None
            for item in items:
                if item.data(UserRole.ATTACHMENT_PATH) == key:
                    good_item = item
                    break

            parent_index = good_item.parent().index()
            good_item.model().removeRow(good_item.row(), parent_index)

        elif element_type == ElementType.OPTICAL_PIC:
            key = element_name
            name = Path(element_name).name

            items = self.tree_model.findItems(name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            good_item = None
            for item in items:
                if item.data(UserRole.OPTICAL_IMAGE_KEY) == key:
                    good_item = item
                    break

            parent_index = good_item.parent().index()
            good_item.model().removeRow(good_item.row(), parent_index)

        self.refresh_view()

    @Slot(QItemSelection, QItemSelection)
    def get_and_update_values(self, new_item: QItemSelection, old_item: QItemSelection) -> None:
        """
        Get the new item and save the old one.

        This slot is called everytime the selection of the treeview is changed.
        The old_item was the one previously selected, for this item we need to
        save the information inserted by the user in the text edit fields.
        This is accomplished by the update_values method

        The newItem is the currently selected line. For this we need to retrieve
        the information and show them in the text edit fields.
        This is accomplished by the get_values method.


        Parameters
        ----------
        new_item : QItemSelection
            The list of items currently selected.
        old_item : QItemSelection
            The list of items that were previously selected.

        Returns
        -------
        None.

        """
        if old_item:
            old_index = old_item.indexes()[0]
            self.update_values(old_index)
        if new_item:
            new_index = new_item.indexes()[0]
            self.update_metadata_table(new_index)
            self.update_sample_selector(new_index)
            self.get_values(new_index)

    def populate_metadata_table(self, dictionary: dict) -> None:
        """
        Populate the metadata model.

        The metadata pair (property / value)
        """
        self.metadata_model.set_metadata(dictionary)

    def update_metadata_table(self, index: QModelIndex) -> None:
        """
        Slot function to request an update of the metadata table.

        This function is taking the QModelIndex from the tree model (the selection model is shared between the tree
        and the table view) and preparing a dictionary of metadata depending on the item type.

        Parameters
        ----------
        index: QModelIndex
            The model index for which we want to update the metadata table.

        Returns
        -------
        None

        """

        dictionary = {}

        try:

            new_item = self.tree_model.itemFromIndex(self.tree_model_proxy.mapToSource(index))
            if new_item.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                if new_item.data(UserRole.SAMPLE_FULL_NAME) in self.autolog.samples:
                    # it is possible that the sample was removed in the other thread.
                    # if not there, then ignore it.
                    sample = self.autolog.samples[new_item.data(UserRole.SAMPLE_FULL_NAME)]

                    dictionary['Parent'] = sample.parent
                    dictionary['Full Name'] = sample.full_name
                    dictionary['Last Name'] = sample.last_name
                    dictionary['Number of subsamples'] = len(sample.subsamples)
                    dictionary['Number of images'] = len(sample.images)
                    dictionary['Number of videos'] = len(sample.videos)

            elif new_item.data(UserRole.ITEM_TYPE) == ElementType.ATTACHMENT_FILE:
                key = str(new_item.data(UserRole.ATTACHMENT_PATH))
                if new_item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                    sample_full_name = new_item.parent().data(UserRole.SAMPLE_FULL_NAME)
                    dictionary = self.autolog.samples[sample_full_name].attachments[key].params
                elif new_item.parent().data(UserRole.ITEM_TYPE) == ElementType.SECTION:
                    dictionary = self.autolog.attachments[key].params
                else:
                    dictionary = {}
            elif new_item.data(UserRole.ITEM_TYPE) == ElementType.MICROSCOPE_PIC:
                sample_full_name = new_item.parent().data(UserRole.SAMPLE_FULL_NAME)
                picture_name = new_item.text()
                path = self.autolog.path
                key = str(path / Path(sample_full_name) / Path(picture_name))
                dictionary = self.autolog.samples[sample_full_name].images[key].params
            elif new_item.data(UserRole.ITEM_TYPE) == ElementType.VIDEO_FILE:
                key = new_item.data(UserRole.VIDEO_KEY)
                sample_full_name = new_item.parent().data(UserRole.SAMPLE_FULL_NAME)
                dictionary = self.autolog.samples[sample_full_name].videos[key].params

            elif new_item.data(UserRole.ITEM_TYPE) == ElementType.OPTICAL_PIC:
                key = new_item.data(UserRole.OPTICAL_IMAGE_KEY)
                if new_item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                    sample_full_name = new_item.parent().data(UserRole.SAMPLE_FULL_NAME)
                    dictionary = self.autolog.samples[sample_full_name].optical_images[key].params
                elif new_item.parent().data(UserRole.ITEM_TYPE) == ElementType.SECTION:
                    dictionary = self.autolog.optical_images[key].params
                else:
                    dictionary = {}

            dictionary = autotools.convert_to_string(dictionary)

        except KeyError:

            dictionary = {}

        self.populate_metadata_table(dictionary)

    @Slot()
    def show_main_window(self):
        """
        Slot function to hide the editor window.

        By hiding the protocol window, its parent (the main window) will become visible.

        Returns
        -------
        None
        """
        self.hide()

    def update_sample_selector(self, index: QModelIndex) -> None:
        """
        Update the selection of the sample selector combo.

        Based on the ItemType of the index, the selected item in the sample selector will be updated in order to match
        either the currently selected sample or the parent of the currently selected microscope picture or video.
        In general the sample selector contains all subsamples of the current protocol plus the 'Protocol' entry
        corresponding to the root level.


        Parameters
        ----------
        index: QModelIndex
            The index corresponding to the currently selected item in the tree view.

        Returns
        -------
        None
        """
        new_item = self.tree_model.itemFromIndex(self.tree_model_proxy.mapToSource(index))
        if new_item.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
            self.sample_selector.setCurrentText(new_item.data(UserRole.SAMPLE_FULL_NAME))
        elif new_item.data(UserRole.ITEM_TYPE) in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
            self.sample_selector.setCurrentText(new_item.parent().data(UserRole.SAMPLE_FULL_NAME))
        elif (new_item.data(UserRole.ITEM_TYPE) in [ElementType.ATTACHMENT_FILE, ElementType.OPTICAL_PIC]
              and new_item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE):
            self.sample_selector.setCurrentText(new_item.parent().data(UserRole.SAMPLE_FULL_NAME))
        else:
            self.sample_selector.setCurrentText('Protocol')

    @Slot()
    def reset_content(self):
        """
        Trigger a refresh of the view.

        This slot is triggered by the reset of the content of the protocol instance.
        Particularly used when the watchdog is stopped and restarted without changing any parameter in the main window.
        """
        self.tree_model.removeRows(0, self.tree_model.rowCount())
        self.sample_selector.clear()
        self.generate_model()
        self.refresh_view()

    def update_values(self, index):
        """
        Update the values of the item corresponding to index.

        The information contained in the edit fields are transferred to the
        data container of the Item and also to the autolog yaml_dict.
        In this way, the next time the autologbook triggers a regeneration of
        the HTML, the new information saved in the yaml_dict are applied.

        From the GUI to the YAML and to the Data container.

        Parameters
        ----------
        index : QModelIndex
            The index of the item to be updated.

        Returns
        -------
        None.

        """
        if index.data(UserRole.ITEM_TYPE) == ElementType.MICROSCOPE_PIC:
            key = index.data(UserRole.PIC_ID)
        elif index.data(UserRole.ITEM_TYPE) == ElementType.OPTICAL_PIC:
            key = index.data(UserRole.OPTICAL_IMAGE_KEY)
        elif index.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
            key = index.data(UserRole.SAMPLE_FULL_NAME)
        elif index.data(UserRole.ITEM_TYPE) == ElementType.ATTACHMENT_FILE:
            key = index.data(UserRole.ATTACHMENT_PATH)
        elif index.data(UserRole.ITEM_TYPE) == ElementType.VIDEO_FILE:
            key = index.data(UserRole.VIDEO_KEY)
        else:
            key = index.data(Qt.DisplayRole)

        if index.data(UserRole.ITEM_TYPE) in (
        ElementType.NAVIGATION_PIC, ElementType.MICROSCOPE_PIC, ElementType.OPTICAL_PIC):
            dict_entry = self.autolog.yamlDict.get(
                key, {'Caption': '', 'Description': '', 'Extra': ''})
            if self.caption_field.text():
                dict_entry['Caption'] = self.caption_field.text()
            index.model().setData(index, self.caption_field.text(), UserRole.CAPTION)
        elif index.data(UserRole.ITEM_TYPE) == ElementType.VIDEO_FILE:
            dict_entry = self.autolog.yamlDict.get(key, {'Caption': '', 'Description': '', 'Extra': ''})
            dict_entry['Caption'] = self.caption_field.text()
            index.model().setData(index, self.caption_field.text(), UserRole.CAPTION)
        else:
            dict_entry = self.autolog.yamlDict.get(key, {'Description': '', 'Extra': ''})

        dict_entry['Description'] = autotools.literal_str(self.description_input.document().toPlainText())
        index.model().setData(index, self.description_input.document().toPlainText(), UserRole.DESCRIPTION)

        dict_entry['Extra'] = autotools.literal_str(self.extrainfo_input.document().toPlainText())
        index.model().setData(index, self.extrainfo_input.document().toPlainText(), UserRole.EXTRA)

        self.autolog.yamlDict[key] = dict_entry

    @Slot(QModelIndex)
    def get_values(self, index: QModelIndex) -> None:
        """
        Retrieve the data from the item and display them.

        From the data containers to the GUI.

        Parameters
        ----------
        index : QModelIndex
            The index corresponding to the item being displayed.

        Returns
        -------
        None.

        """
        self.tree_model_last_selected_item = QPersistentModelIndex(index)
        self.selected_element_label.setText(f'Element being edited / displayed: {index.data(QtCore.Qt.DisplayRole)}')
        if index.data(UserRole.ITEM_TYPE) in [ElementType.NAVIGATION_PIC, ElementType.MICROSCOPE_PIC,
                                              ElementType.OPTICAL_PIC]:
            self.preview_stack.setCurrentIndex(0)
            self.image_preview.setPixmap(QPixmap(index.data(UserRole.IMAGE)).scaledToWidth(390, 1))
            self.caption_field.setEnabled(True)
            self.caption_field.setText(index.data(UserRole.CAPTION))
            self.description_input.setPlainText(index.data(UserRole.DESCRIPTION))
            self.extrainfo_input.setPlainText(index.data(UserRole.EXTRA))
        elif index.data(UserRole.ITEM_TYPE) == ElementType.VIDEO_FILE:
            self.preview_stack.setCurrentIndex(1)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(str(index.data(UserRole.VIDEO_PATH)))))
            self.media_player.play()
            time.sleep(0.1)
            self.media_player.pause()
            self.caption_field.setEnabled(True)
            self.caption_field.setText(index.data(UserRole.CAPTION))
            self.description_input.setPlainText(index.data(UserRole.DESCRIPTION))
            self.extrainfo_input.setPlainText(index.data(UserRole.EXTRA))
        elif index.data(UserRole.ITEM_TYPE) in [ElementType.TEXT, ElementType.SECTION, ElementType.SAMPLE,
                                                ElementType.ATTACHMENT_FILE]:
            self.preview_stack.setCurrentIndex(0)
            self.image_preview.setText('Image preview not available for this element')
            self.caption_field.clear()
            self.caption_field.setEnabled(False)
            self.description_input.setPlainText(index.data(UserRole.DESCRIPTION))
            self.extrainfo_input.setPlainText(index.data(UserRole.EXTRA))

    @Slot()
    def copy_custom_values(self, what='all'):
        """
        Copy the content of the custom fields to the custom_data_dict dictionary.

        This button is mimicking the copy to clipboard action, but it takes all three customizable texts and made it
        available for the paste_custom_values function.

        This slot is called when the copy button is pressed.

        Returns
        -------

        """
        if what.lower() == 'all':
            self.custom_data_dict = {
                'Caption': self.caption_field.text(),
                'Description': self.description_input.document().toPlainText(),
                'Extra': self.extrainfo_input.document().toPlainText()
            }
        elif what.lower() == 'caption':
            self.custom_data_dict = {'Caption': self.caption_field.text()}
        elif what.lower() == 'description':
            self.custom_data_dict = {'Description': self.description_input.document().toPlainText()}
        elif what.lower() == 'extra':
            self.custom_data_dict = {'Extra': self.extrainfo_input.document().toPlainText()}
        self.paste_custom_value_button.setEnabled(True)
        self.custom_data_dict_available = True

    @Slot()
    def paste_custom_values(self, what='all'):
        """
        Paste the content of the custom_data_dict dictionary to the custom fields.

        This slot is called when the paste button is pressed.

        Returns
        -------

        """
        if what.lower() in ['all', 'caption']:
            if 'Caption' in self.custom_data_dict.keys():
                self.caption_field.setText(self.custom_data_dict['Caption'])
        if what.lower() in ['all', 'description']:
            if 'Description' in self.custom_data_dict.keys():
                self.description_input.document().setPlainText(self.custom_data_dict['Description'])
        if what.lower() in ['all', 'extra']:
            if 'Extra' in self.custom_data_dict.keys():
                self.extrainfo_input.document().setPlainText(self.custom_data_dict['Extra'])

    @Slot()
    def update_protocol(self):
        """
        Update the protocol.

        Slot connected to the Update protocol. When clicked the current item values
        are transferred to the yaml_dict and the whole yaml_dict is dumped to the
        yaml protocol file.

        This filesystem change triggers the watchdog to force the generation of
        the whole HTML and its publication to the ELOG.

        Returns
        -------
        None.

        """
        if self.autolog_tree_viewer.selectionModel().currentIndex().isValid():
            self.update_values(self.autolog_tree_viewer.selectionModel().currentIndex())
            self.tree_model_last_selected_item = QPersistentModelIndex(
                self.autolog_tree_viewer.selectionModel().currentIndex()
            )
        autotools.dump_yaml_file(self.autolog.yamlDict, self.autolog.yamlFilename)

    def scroll_to_last_selected_item(self):
        """
        Scroll the tree viewer down to the last selected item.

        This item is used when the protocol editor window is opened a second time.
        So that the user will be able to continue editing from the same item where he was when he left.

        Returns
        -------
        None.
        """
        self.autolog_tree_viewer.selectionModel().clearSelection()
        if self.tree_model_last_selected_item and self.tree_model_last_selected_item.isValid():
            index = QModelIndex(self.tree_model_last_selected_item)
            self.autolog_tree_viewer.selectionModel().select(index, QItemSelectionModel.SelectCurrent)
            self.autolog_tree_viewer.scrollTo(index, QAbstractItemView.EnsureVisible)
            self.enable_filesystem_command_buttons(index)
        else:
            self.clear_fields()
            self.enable_filesystem_command_buttons(None)

    @Slot()
    def scroll_to_last_inserted_item(self):
        """
        Scroll the tree viewer down to the last inserted item.

        When this slot is called, the tree viewer will automatically scroll and select the last inserted item.

        Returns
        -------
        None
        """
        if self.tree_model_last_inserted_item and self.tree_model_last_inserted_item.isValid():
            self.autolog_tree_viewer.selectionModel().clearSelection()
            index = QModelIndex(self.tree_model_last_inserted_item)
            self.autolog_tree_viewer.selectionModel().select(index, QItemSelectionModel.SelectCurrent)
            self.autolog_tree_viewer.scrollTo(index, QAbstractItemView.EnsureVisible)
            self.enable_filesystem_command_buttons(index)

    @Slot()
    def rename_protocol_element(self):
        """
        Rename the currently selected protocol element.

        This slot is calling the RenameDialog in order to obtain from the user a new name for the currently selected
        item.
        The slot is available only on editable items (so not on SectionItem).

        If the new name is different from the old one, then a FileSystemCommand is prepared and sent via the signal /
        slot mechanism to the commander.

        Custom fields (caption, description, extra) stored in the yaml dictionary will be moved to the renamed item in
        a so-called recycling process.
        In case of renaming a sample or subsamples, also all the customization of all their members will be recycled.

        Returns
        -------
        None
        """
        # if the index is invalid, exit now!
        if not self.autolog_tree_viewer.selectionModel().currentIndex().isValid():
            return

        # get the item
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        item = self.tree_model.itemFromIndex(model_index)

        # if the item is not editable, then exit now!
        if item.data(UserRole.ITEM_TYPE) in [ElementType.SECTION, ElementType.TEXT]:
            return

        # be sure that the custom values of the currently selected item are transferred
        self.update_values(self.autolog_tree_viewer.selectionModel().currentIndex())

        text = f'Enter a new name for element {item.text()} and then click OK'
        original_name = item.text()
        rename_dialog = RenameDialog(self, text, original_name)
        if rename_dialog.exec_():
            new_name = rename_dialog.new_name_field.text()
            if new_name == original_name:
                return
            else:
                if item.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                    original_path = Path(item.data(UserRole.SAMPLE_FULL_NAME))
                    new_path = original_path.parent / Path(new_name)
                    old_key = str(original_path).replace('\\', '/')
                    new_key = str(new_path).replace('\\', '/')
                    self.yaml_dictionary_recycler.recycle(self.autolog.yamlDict, item.data(UserRole.ITEM_TYPE),
                                                          old_key, new_key)
                    command = FileSystemCommand(autotools.FSCommandType.RENAME_DIR, original_path, new_path)

                elif item.data(UserRole.ITEM_TYPE) in [ElementType.VIDEO_FILE, ElementType.MICROSCOPE_PIC]:
                    parent_path = item.parent().data(UserRole.SAMPLE_FULL_NAME)
                    name = item.text()

                    # we recycle the customization elements.
                    old_key = item.data(UserRole.VIDEO_KEY) if item.data(
                        UserRole.ITEM_TYPE) == ElementType.VIDEO_FILE else item.data(UserRole.PIC_ID)
                    new_key = str(Path(old_key).parent / Path(new_name))

                    self.yaml_dictionary_recycler.recycle(self.autolog.yamlDict,
                                                          item.data(UserRole.ITEM_TYPE), old_key, new_key)
                    command = FileSystemCommand(autotools.FSCommandType.RENAME_FILE,
                                                Path(parent_path) / Path(name),
                                                Path(parent_path) / Path(new_name))

                elif item.data(UserRole.ITEM_TYPE) == ElementType.NAVIGATION_PIC:
                    input_path = Path(item.text())
                    output_path = Path(new_name)

                    key = str(input_path)
                    new_key = str(output_path)
                    self.yaml_dictionary_recycler.recycle(self.autolog.yamlDict,
                                                          item.data(UserRole.ITEM_TYPE), key, new_key)
                    command = FileSystemCommand(autotools.FSCommandType.RENAME_FILE, input_path, output_path)

                elif item.data(UserRole.ITEM_TYPE) in [ElementType.ATTACHMENT_FILE, ElementType.OPTICAL_PIC]:
                    if item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                        # it is a sample wide element
                        input_path = Path(item.parent().data(UserRole.SAMPLE_FULL_NAME)) / Path(item.text())
                        output_path = Path(item.parent().data(UserRole.SAMPLE_FULL_NAME)) / Path(new_name)
                    else:
                        # it is a protocol wide element
                        input_path = Path(item.text())
                        output_path = Path(new_name)
                    if item.data(UserRole.ITEM_TYPE) == ElementType.ATTACHMENT_FILE:
                        old_key = str(item.data(UserRole.ATTACHMENT_PATH))
                        new_key = str(Path(old_key).parent / Path(new_name))
                    else:  # ElementType == OPTICAL_PIC
                        old_key = item.data(UserRole.OPTICAL_IMAGE_KEY)
                        new_key = str(item.data(UserRole.OPTICAL_IMAGE_PATH).parent / Path(new_name))
                    self.yaml_dictionary_recycler.recycle(self.autolog.yamlDict,
                                                          item.data(UserRole.ITEM_TYPE), old_key, new_key)
                    command = FileSystemCommand(autotools.FSCommandType.RENAME_FILE, input_path, output_path)

                else:
                    command = None

                if command:
                    self.execute_filesystem_command.emit(command)

                # dump to yaml file
                autotools.dump_yaml_file(self.autolog.yamlDict, self.autolog.yamlFilename)

    def recycle_protocol_element(self):
        """Recycle a protocol element putting it in the bin and out from the protocol"""
        # current index is invalid. exit now
        if not self.autolog_tree_viewer.selectionModel().currentIndex().isValid():
            return

        # get the item from the index
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        item = self.tree_model.itemFromIndex(model_index)

        # be sure that the custom values of the currently selected item are transferred
        self.update_values(self.autolog_tree_viewer.selectionModel().currentIndex())

        # only microscope_picture, videos, optical images and attachments can be recycled
        if item.data(UserRole.ITEM_TYPE) in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:

            sample = item.parent()
            sample_path = Path(sample.data(UserRole.SAMPLE_FULL_NAME))
            old_path = sample_path / Path(item.data(Qt.DisplayRole))
            new_path = sample_path / Path('excluded/') / Path(item.data(Qt.DisplayRole))

            if item.data(UserRole.ITEM_TYPE) == ElementType.VIDEO_FILE:
                old_key = item.data(UserRole.VIDEO_KEY)
                new_key = str(Path(old_key).parent / Path('excluded/') / Path(item.data(Qt.DisplayRole)))
            else:  # ElementType.MICROSCOPE_PIC
                old_key = item.data(UserRole.PIC_ID)
                new_key = str(Path(old_key).parent / Path('excluded/') / Path(item.data(Qt.DisplayRole)))

            command = FileSystemCommand(FSCommandType.MOVE_FILE, old_path, new_path)
        elif item.data(UserRole.ITEM_TYPE) in [ElementType.ATTACHMENT_FILE, ElementType.OPTICAL_PIC]:

            if item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                old_path = Path(item.parent().data(UserRole.SAMPLE_FULL_NAME)) / Path(item.text())
                new_path = Path(item.parent().data(UserRole.SAMPLE_FULL_NAME)) / Path('excluded/') / Path(item.text())
            else:
                old_path = Path(item.text())
                new_path = Path('excluded/') / Path(item.text())

            if item.data(UserRole.ITEM_TYPE) == ElementType.ATTACHMENT_FILE:
                old_key = str(item.data(UserRole.ATTACHMENT_PATH))
                new_key = str(Path(old_key).parent / Path('excluded/') / Path(item.text()))
            else:  # ElementType.OPTICAL_PIC
                old_key = item.data(UserRole.OPTICAL_IMAGE_KEY)
                new_key = str(item.data(UserRole.OPTICAL_IMAGE_PATH).parent / Path('excluded/') / Path(item.text()))

            command = FileSystemCommand(FSCommandType.MOVE_FILE, old_path, new_path)

        else:
            command = None
            log.warning('Only microscope pictures, videos, optical images and attachments can be recycled.')
            QMessageBox.warning(self, 'Element recycle',
                                'Only microscope pictures, videos, optical images and attachments can be recycled.',
                                buttons=QMessageBox.Ok)

        if command:
            reply = QMessageBox.question(self, 'Element recycle',
                                         f'Are you sure you want to recycle {str(command.input_path.name)}?{chr(10)}'
                                         f'A recycled item will be removed from the protocol, but not deleted from the '
                                         f'disk.{chr(10)}'
                                         f'You can still retrieve it from the basket bin in a later stage.',
                                         buttons=(QMessageBox.Yes | QMessageBox.No))
            if reply == QMessageBox.Yes:
                self.execute_filesystem_command.emit(command)

                if old_key:
                    self.yaml_dictionary_recycler.recycle(self.autolog.yamlDict, item.data(UserRole.ITEM_TYPE),
                                                          old_key, new_key)
                # dump to yaml file
                autotools.dump_yaml_file(self.autolog.yamlDict, self.autolog.yamlFilename)

    @Slot()
    def move_element_to_another_sample(self):
        """
        Slot to transfer an editable item from one sample to another.

        In the case of a microscope picture or a video, from a filesystem point of view it is like moving them from a
        directory to another.

        In the case of a sample, the filesystem equivalent is to rename the folder with a different name.

        For sample and videos, the yaml customization is preserved.

        Returns
        -------

        """
        # current index is invalid. exit now
        if not self.autolog_tree_viewer.selectionModel().currentIndex().isValid():
            return

        # get the item from the index
        proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
        model_index = self.tree_model_proxy.mapToSource(proxy_index)
        item = self.tree_model.itemFromIndex(model_index)

        # check if the item could be moved to another sample. if not, just exit
        if item.data(UserRole.ITEM_TYPE) in [ElementType.SECTION, ElementType.TEXT, ElementType.NAVIGATION_PIC]:
            QMessageBox.information(self, 'Move to another sample',
                                    f'This element type {item.data(UserRole.ITEM_TYPE)} cannot be move to another '
                                    f'sample',
                                    buttons=QMessageBox.Ok)
            return

        # be sure that the custom values of the currently selected item are transferred
        self.update_values(self.autolog_tree_viewer.selectionModel().currentIndex())

        item_name = item.text()

        if item.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
            sample_name = item.data(UserRole.SAMPLE_FULL_NAME)
        elif item.data(UserRole.ITEM_TYPE) in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
            sample_name = item.parent().data(UserRole.SAMPLE_FULL_NAME)
        elif item.data(UserRole.ITEM_TYPE) in [ElementType.ATTACHMENT_FILE, ElementType.OPTICAL_PIC]:
            if item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                sample_name = item.parent().data(UserRole.SAMPLE_FULL_NAME)
            else:
                sample_name = 'Protocol'
        else:
            sample_name = None

        sample_list = [self.sample_selector.itemText(i) for i in range(self.sample_selector.count())]
        if item.data(UserRole.ITEM_TYPE) in [ElementType.SAMPLE, ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
            sample_list.remove('Protocol')

        move_sample_dialog = ChangeSampleDialog(self, item_name, sample_name, sample_list)
        if move_sample_dialog.exec_():
            new_sample_full_name = move_sample_dialog.sample_combo.currentText()
        else:
            return

        if item.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
            # we are moving a sample to another sample.
            # from a FS point of view this is equivalent of renaming a directory
            src_dir = item.data(UserRole.SAMPLE_FULL_NAME)
            dest_dir = new_sample_full_name + '/' + item.data(UserRole.SAMPLE_LAST_NAME)

            # recycle the yaml customization
            self.yaml_dictionary_recycler.recycle(self.autolog.yamlDict, item.data(UserRole.ITEM_TYPE),
                                                  src_dir, dest_dir)

            # prepare the command
            command = FileSystemCommand(autotools.FSCommandType.RENAME_DIR, Path(src_dir), Path(dest_dir))

        elif item.data(UserRole.ITEM_TYPE) in [ElementType.VIDEO_FILE, ElementType.MICROSCOPE_PIC]:
            # we are moving a video from one sample to another
            old_path = Path(item.parent().data(UserRole.SAMPLE_FULL_NAME)) / Path(item.text())
            new_path = Path(new_sample_full_name) / Path(item.text())

            # recycle the yaml customization
            old_key = item.data(UserRole.VIDEO_KEY) if item.data(UserRole.ITEM_TYPE) == ElementType.VIDEO_FILE else \
                item.data(UserRole.PIC_ID)
            new_key = str(autotools.strip_path(old_key, old_path) / new_path)
            self.yaml_dictionary_recycler.recycle(self.autolog.yamlDict,
                                                  item.data(UserRole.ITEM_TYPE), old_key, new_key)

            # prepare the command
            command = FileSystemCommand(autotools.FSCommandType.RENAME_FILE, old_path, new_path)

        elif item.data(UserRole.ITEM_TYPE) in [ElementType.ATTACHMENT_FILE, ElementType.OPTICAL_PIC]:
            if item.data(UserRole.ITEM_TYPE) == ElementType.ATTACHMENT_FILE:
                old_key = str(item.data(UserRole.ATTACHMENT_PATH))
            else:
                old_key = item.data(UserRole.OPTICAL_IMAGE_KEY)

            # we are moving an attachment or an optical image.
            if item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                # it is a sample wide element
                old_path = Path(item.parent().data(UserRole.SAMPLE_FULL_NAME)) / Path(item.text())
                if new_sample_full_name == 'Protocol':
                    new_path = Path(item.text())
                else:
                    new_path = Path(new_sample_full_name) / Path(item.text())
            else:
                # it is protocol wide element
                old_path = Path(item.text())
                if new_sample_full_name == 'Protocol':
                    new_path = Path(item.text())
                else:
                    new_path = Path(new_sample_full_name) / Path(item.text())
            new_key = str(autotools.strip_path(old_key, old_path) / new_path)
            self.yaml_dictionary_recycler.recycle(self.autolog.yamlDict,
                                                  item.data(UserRole.ITEM_TYPE), old_key, new_key)

            # prepare the command
            command = FileSystemCommand(autotools.FSCommandType.RENAME_FILE, old_path, new_path)

        else:
            command = None

        if command:
            self.execute_filesystem_command.emit(command)

        # dump to yaml file
        autotools.dump_yaml_file(self.autolog.yamlDict, self.autolog.yamlFilename)

    def delete_protocol_element(self):
        """Delete one protocol element"""
        if self.autolog_tree_viewer.selectionModel().currentIndex().isValid():
            proxy_index = self.autolog_tree_viewer.selectionModel().currentIndex()
            model_index = self.tree_model_proxy.mapToSource(proxy_index)
            item = self.tree_model.itemFromIndex(model_index)
            if item.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                command = FileSystemCommand(autotools.FSCommandType.DELETE_DIR,
                                            Path(item.data(UserRole.SAMPLE_FULL_NAME)))
            elif item.data(UserRole.ITEM_TYPE) in [ElementType.MICROSCOPE_PIC, ElementType.VIDEO_FILE]:
                parent_path = item.parent().data(UserRole.SAMPLE_FULL_NAME)
                name = item.text()
                command = FileSystemCommand(autotools.FSCommandType.DELETE_FILE,
                                            Path(parent_path) / Path(name))
            elif item.data(UserRole.ITEM_TYPE) == ElementType.NAVIGATION_PIC:
                path = Path(item.text())
                command = FileSystemCommand(autotools.FSCommandType.DELETE_FILE, path)
            elif item.data(UserRole.ITEM_TYPE) in [ElementType.ATTACHMENT_FILE, ElementType.OPTICAL_PIC]:
                if item.parent().data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                    path = Path(item.parent().data(UserRole.SAMPLE_FULL_NAME)) / Path(item.text())
                else:
                    path = Path(item.text())
                command = FileSystemCommand(autotools.FSCommandType.DELETE_FILE, path)
            else:
                command = None

            if command:
                reply = QMessageBox.question(self, 'Delete protocol element',
                                             f'Are you sure you want to delete {str(command.input_path)}? This '
                                             f'operation can not be undone.',
                                             buttons=(QMessageBox.Yes | QMessageBox.No))
                if reply == QMessageBox.Yes:
                    self.execute_filesystem_command.emit(command)

    @Slot(QModelIndex)
    def enable_filesystem_command_buttons(self, index: QModelIndex | None):
        """Enable the filesystem dropdown buttons"""
        fs_buttons = [self.recycle_dropdown_button, self.edit_dropdown_button]

        if index is None:
            enable = False
        else:
            item = self.tree_model.itemFromIndex(self.tree_model_proxy.mapToSource(index))

            if item.data(UserRole.ITEM_TYPE) in [ElementType.MICROSCOPE_PIC,
                                                 ElementType.VIDEO_FILE,
                                                 ElementType.SAMPLE,
                                                 ElementType.ATTACHMENT_FILE,
                                                 ElementType.OPTICAL_PIC,
                                                 ElementType.NAVIGATION_PIC]:
                enable = True
            else:
                enable = False

        for button in fs_buttons:
            button.setEnabled(enable)


class MainWindow(QMainWindow, Ui_MainWindow):
    """The main window of the GUI."""

    # Used to have different colors for each logging level.
    COLORS = {
        logging.DEBUG: 'black',
        logging.INFO - 5: 'hotpink',
        logging.INFO: 'blue',
        logging.WARNING: 'orange',
        logging.ERROR: 'red',
        logging.CRITICAL: 'purple'
    }

    # prepare custom signals
    added_element = Signal(ElementType, str, str, name='added_element')
    removed_element = Signal(ElementType, str, str, name='removed_element')
    change_autolog = Signal(autoprotocol.Protocol, name='change_autolog')
    reset_content = Signal(name='reset_content')

    title_modifier = ' *'

    class GUIContent():
        def __init__(self):
            self.protocol_folder = None
            self.mirroring_folder = None
            self.microscope = None
            self.mirroring_switch = False
            self.custom_switch = False
            self.custom_protocolID = None
            self.custom_project = None
            self.custom_responsible = None

        def __eq__(self, other: MainWindow.GUIContent):

            are_the_same = True and self.protocol_folder == other.protocol_folder \
                and self.microscope == other.microscope \
                and self.mirroring_switch == other.mirroring_switch \
                and self.custom_switch == other.custom_switch

            if self.mirroring_switch:
                are_the_same = are_the_same and self.mirroring_folder == other.mirroring_folder

            if self.custom_switch:
                are_the_same = are_the_same and self.custom_protocolID == other.custom_protocolID \
                    and self.custom_project == other.custom_project \
                    and self.custom_responsible == other.custom_responsible

            return are_the_same

        @classmethod
        def from_main_window(cls, main_window: MainWindow) -> MainWindow.GUIContent:
            c = cls()
            c.protocol_folder = main_window.protocol_folder_text.text()
            c.mirroring_folder = main_window.mirroring_folder_text.text()
            c.mirroring_switch = main_window.mirror_checkBox.isChecked()
            c.microscope = main_window.select_microscope_comboBox.currentText()
            c.custom_switch = main_window.custom_ownership_checkbox.isChecked()
            c.custom_protocolID = main_window.projectID_field.text()
            c.custom_project = main_window.project_name_field.text()
            c.custom_responsible = main_window.responsible_field.text()
            return c

        def apply_to_gui(self, gui: MainWindow):
            gui.protocol_folder_text.setText(self.protocol_folder)
            gui.mirroring_folder_text.setText(self.mirroring_folder)
            gui.mirror_checkBox.setChecked(self.mirroring_switch)
            gui.select_microscope_comboBox.setCurrentText(self.microscope)
            gui.custom_ownership_checkbox.setChecked(self.custom_switch)
            gui.projectID_field.setText(self.custom_protocolID)
            gui.project_name_field.setText(self.custom_project)
            gui.responsible_field.setText(self.custom_responsible)

        def transfer_to_config(self, config: configparser.ConfigParser) -> configparser.ConfigParser:
            config.set('GUI', 'src_path', str(Path(self.protocol_folder)))
            config.set('GUI', 'mirror', str(self.mirroring_switch))
            if self.mirroring_switch:
                config.set('GUI', 'mirror_path', str(Path(self.mirroring_folder)))
            else:
                config.set('GUI', 'mirror_path', '')
            config.set('GUI', 'microscope', self.microscope)
            config.set('GUI', 'custom_ownership', str(self.custom_switch))
            if self.custom_switch:
                config.set('GUI', 'projectID', self.custom_protocolID)
                config.set('GUI', 'project_name', self.custom_project)
                config.set('GUI', 'responsible', self.custom_responsible)
            else:
                config.set('GUI', 'projectID', '')
                config.set('GUI', 'project_name', '')
                config.set('GUI', 'responsible', '')
            return config

    def __init__(self, app: QApplication, config: configparser.ConfigParser):
        """
        Build an instance of the GUI main window.

        Setup the user interface as produced by the QtDesigner
        Setup the logging machinery in order to have all logging messages
        redirected to the GUI
        Call the start_thread method and finally do all signal slot connections.

        Parameters
        ----------
        app : QApplication
            The application calling the main window.

        Returns
        -------
        None.

        """
        super().__init__()
        self.app = app
        self.config = config
        self.setupUi(self)

        # set the protocol editor to none
        self.protocol_editor = None

        # create a logging handler with a slot function pointing to update_status
        self.handler = QtHandler(self.update_status)

        # create a formatter and assign it to the handler
        fs = '[%(asctime)s] %(threadName)-15s %(levelname)-8s %(message)s'
        formatter = logging.Formatter(fs, datefmt='%Y%m%d-%H:%M:%S')
        self.handler.setFormatter(formatter)
        log.addHandler(self.handler)

        # create a logging handler to a timed rotated file
        log_filepath = Path.home() / Path('autologbook') / Path('logs')
        log_filepath.mkdir(parents=True, exist_ok=True)
        log_filename = log_filepath / Path('autologbook-gui.log')

        self.file_handler = TimedRotatingFileHandler(filename=log_filename,
                                                     when='D', interval=7, backupCount=7)
        self.file_handler.setFormatter(formatter)
        log.addHandler(self.file_handler)

        # initialize workers and threads dictionaries
        self.workers = {}
        self.worker_threads = {}

        # start the threads and their workers
        self.start_thread()

        self.base_path = Path(autoconfig.IMAGE_SERVER_BASE_PATH)
        self.pattern = '^#*([\\d]+)\\s*[-_]\\s*([\\w\\W]+)\\s*[-_]\\s*([\\w\\W]+)$'
        self.is_watchdog_running = False
        self.is_watchdog_enabled = False

        self.is_ok_to_start = False
        self.are_user_credentials_checked = False
        self.is_mirroring_requested = self.mirror_checkBox.isChecked()
        self.is_custom_ownership_requested = self.custom_ownership_checkbox.isChecked()
        self.protocol_folder_path = None
        self.mirroring_folder_path = None
        self.microscope = self.config.get('GUI_DEFAULT', 'default_microscope', fallback='Quattro')
        self.select_microscope_comboBox.blockSignals(True)
        self.select_microscope_comboBox.setCurrentText(self.microscope)
        self.select_microscope_comboBox.blockSignals(False)
        self.browser_process = ''
        self.projectID = None
        self.project_name = None
        self.project_responsible = None
        self.path = None
        self.connect_signals_slot()
        self.experiment_filename = None
        self.experiment_need_save = False

        self.check_threads_status()
        self.thread_check_timer = QTimer()
        self.thread_check_timer.timeout.connect(self.check_threads_status)
        self.thread_check_timer.start(autoconfig.THREAD_STATUS_UPDATE)

        # create a FS Commander to execute commands received from the protocol editor
        self.file_system_commander = FileSystemCommander()

        self.log_message_box.setContextMenuPolicy(Qt.CustomContextMenu)
        self.log_context_menu = self.generate_log_context_menu()
        self.log_message_box.customContextMenuRequested.connect(self.show_log_context_menu)

        # store the current GUI content
        self.current_gui_content = MainWindow.GUIContent.from_main_window(self)

        # store the GUI content as from the last loaded experiment
        self.last_loaded_gui_content = MainWindow.GUIContent.from_main_window(self)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if self.is_watchdog_running:
            event.ignore()
        else:
            if event.mimeData().hasUrls():
                event.accept()
            else:
                event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if len(files) > 1:
            log.warning('You have dropped more than one file, but only 1 experiment file can be loaded.')
            log.warning('Loading file %s', files[0])
        gui_content = MainWindow.GUIContent.from_main_window(self)
        try:
            self._load_experiment(files[0])
        except (UnicodeError, configparser.Error):
            log.error('Error loading experiment file %s' % files[0])
            gui_content.apply_to_gui(self)

    def show_log_context_menu(self, pos: QPoint):
        visibility_flag = autotools.LogMessageBoxVisibilityFlag.NO_SELECTION
        if self.log_message_box.textCursor().hasSelection():
            visibility_flag = autotools.LogMessageBoxVisibilityFlag.SELECTION

        filter_context_menu(self.log_context_menu, visibility_flag)
        self.log_context_menu.exec(self.log_message_box.viewport().mapToGlobal(pos))

    def generate_log_context_menu(self) -> QMenu:

        context_menu = self.log_message_box.createStandardContextMenu()
        context_menu.addSeparator()

        menu_scheme = {
            'clear': {
                'type': QAction,
                'obj': None,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'clear',
                'text': 'Clear logger',
                'icon': ':/resources/icons8-cancel-48.png',
                'slot': self.clear_logger,
                'show_when_flag': autotools.LogMessageBoxVisibilityFlag.ALWAYS,
                'separator_after': False,
            },
            'save': {
                'type': QAction,
                'obj': None,
                'parent_name': 'root',
                'parent_obj': context_menu,
                'name': 'save',
                'text': 'Save logger as...',
                'icon': ':/resources/icons8-save-as-48.png',
                'slot': self.save_logger,
                'show_when_flag': autotools.LogMessageBoxVisibilityFlag.ALWAYS,
                'separator_after': False,
            }
        }

        return generate_context_menu_from_scheme(context_menu, self.log_message_box, menu_scheme)

    def show(self, loglevel: int = logging.INFO):
        """
        Show the main window.

        Overload of the parent show method adding a message in the log window.

        Params:
        loglevel: int
            Change the Main Window appearance depending on the logging level.
            If loglevel >= logging.INFO, the standard GUI will be rendered, otherwise
            debug widgets will be shown.

        """
        log.info('Welcome to the autologbook GUI!')
        if loglevel >= logging.INFO:
            self.hide_debug_elements(True)

        super().show()

    def start_thread(self):
        """
        Start all the needed threads.

        The program is using a separate thread for each of the three workers plus
        another one executing the GUI.

        A reference of all workers and threads are stored in the self.workers
        and self.worker_threads dictionaries.

        Returns
        -------
        None.

        """

        worker_list = {
            'SingleWatchdog': {
                'WorkerClassType': 'SingleWatchdogWorker',
                'WorkerObjectName': 'SingleWatchdog',
                'WorkerThreadName': 'WatchThread'
            }
        }

        for key, worker in worker_list.items():
            new_worker = globals()[worker['WorkerClassType']]()
            new_worker.parent = self
            new_worker_thread = QtCore.QThread()
            new_worker.setObjectName(worker['WorkerObjectName'])
            new_worker_thread.setObjectName(worker['WorkerThreadName'])
            new_worker.moveToThread(new_worker_thread)

            # connect the worker signals to the MainWindow slots
            new_worker.worker_is_running.connect(self.disable_inputs)

            # this start an event loop on the thread, not the Worker!
            new_worker_thread.start()

            # add references of the worker and of the thread to the MainWindow
            # to avoid garbage collection
            self.workers[key] = new_worker
            self.worker_threads[worker['WorkerThreadName']] = new_worker_thread

    def connect_signals_slot(self):
        """Connect Qt Signals to corresponding slots."""
        self.actionClose.triggered.connect(self.close)
        self.watchdog_pushbutton.clicked.connect(self.workers['SingleWatchdog'].toggle)
        self.action_toggle_watchdog.triggered.connect(self.workers['SingleWatchdog'].toggle)
        self.action_toggle_watchdog.triggered.connect(self.toggled_watchdog)
        self.action_Load_experiment.triggered.connect(self.load_experiment)
        self.actionSave_experiment.triggered.connect(self.save_experiment)
        self.actionSave_logger.triggered.connect(self.save_logger)
        self.actionClear_logger.triggered.connect(self.clear_logger)
        self.actionLoad_configuration_file.triggered.connect(self.load_conffile)
        self.actionAbout_Autologbook.triggered.connect(self.show_about)
        self.actionReset_to_default.triggered.connect(self.reset_conf)
        self.actionEdit_configuration.triggered.connect(self.edit_conf)
        self.actionChange_user_credentials.triggered.connect(self.edit_user_credentials)
        self.app.aboutToQuit.connect(self.force_quit)

    def edit_conf(self):
        """
        Open the configuration editor window.

        After closing the window the following actions are processed:
            1. The configuration information from the window are transferred to
               the local_path dictionary
            2. The autotools.init function is called in order to initialize all
               sub-modules global variables.
            3. Inputs of the main window are validated.

        Returns
        -------
        None.

        """
        dialog = ConfigurationEditorDialog(parent=self)
        dialog.set_all_values(self.config)
        if dialog.exec_():
            self.config = dialog.get_conf()
            autotools.init(self.config)
            log.info('Configuration updated')
            self.are_user_credentials_checked = False
            self.validate_inputs()

    def load_conffile(self):
        """
        Load a configuration file.

        This function is called from the GUI and allows the user to load presets
        from a configuration file.

        It opens a file selection dialog restricted to *.ini file.
        If the user click on open, the following actions are processed:
            1. A configuration parser is created and the configuration file is parsed
            2. The autotools.init function is called
            3. The configuration object is assigned to the local_path configuration
            4. The inputs of the main window are validated.

        Returns
        -------
        None.

        """
        directory = Path.home() / Path('Documents')
        returnpath = QFileDialog.getOpenFileName(
            self, 'Configuration file', directory=str(directory), filter='Conf file (*.ini)')
        if returnpath:
            conffile = Path(returnpath[0])
            conf = configparser.ConfigParser()
            conf.read(conffile)
            autotools.init(conf)
            self.config = conf
            log.info('Loading configuration file %s' % (str(conffile)))
            self.are_user_credentials_checked = False
            self.validate_inputs()

    def reset_conf(self):
        """
        Reset the configuration to the default.

        A new configuration object is created using the autotools.generate_default_conf()
        The autotools.init function is called.
        The local_path configuration object is reassigned.

        Returns
        -------
        None.

        """
        conf = autotools.generate_default_conf()
        autotools.init(conf)
        self.config = conf
        log.info('Loading default configuration')
        self.are_user_credentials_checked = False
        self.validate_inputs()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.experiment_need_save:
            ans = QMessageBox.question(self, 'Save experiment',
                                       'The current experiment was not saved. Would you like to save before exiting?',
                                       buttons=(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel))
            if ans == QMessageBox.Yes:
                self.save_experiment()
                event.accept()
            elif ans == QMessageBox.No:
                event.accept()
            elif ans == QMessageBox.Cancel:
                event.ignore()
            else:
                event.ignore()

    def force_quit(self):
        """
        Force quit the application.

        This function is called by the about to quit signal. It allows to
        quit as clean as possible all the open and running threads.

        Returns
        -------
        None.

        """
        for worker in self.workers.values():
            try:
                if worker.observer.is_alive():
                    worker.stop()
            except AttributeError:
                log.debug('Trying to quit an observer that was not created yet.')
        for thread in self.worker_threads.values():
            if thread.isRunning():
                thread.quit()
                thread.wait()

    @Slot(str, logging.LogRecord)
    def update_status(self, status, record):
        """
        Update the status window.

        This is the Qt Slot connected to the QtHandler Signaller.

        Parameters
        ----------
        status : STRING
            The formatted string to be appended to the message window.
        record : logging.LogRecord
            The LogRecord as transmitted by the logging module.

        Returns
        -------
        None.

        """
        color = self.COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.log_message_box.appendHtml(s)

    def watchdog_pushbutton_facelift(self):
        """
        Adapt the main window appearance.

        Depending on the fact that the watchdog is running or not, the main window
        has to look differently. This function is performing a facelift of the main window

        Returns
        -------
        None.

        """

        if self.is_watchdog_running:
            self.watchdog_pushbutton.setText('Stop watchdog')
            self.watchdog_pushbutton.setToolTip('Stop the watchdog')
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap(":/resources/icons8-stop-sign-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.watchdog_pushbutton.setIcon(icon3)
            self.action_toggle_watchdog.setText('Stop watchdog')
            self.action_toggle_watchdog.setIcon(icon3)
            self.menuSettings.setEnabled(False)
            self.open_explorer_pushbuttom.setEnabled(True)
            self.open_browser_button.setEnabled(True)
            self.edit_custom_html_file_pushbutton.setEnabled(True)
            self.action_Load_experiment.setEnabled(False)
        else:
            self.watchdog_pushbutton.setText('Start watchdog')
            self.watchdog_pushbutton.setToolTip('Start the watchdog')
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap(":/resources/icons8-play-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.watchdog_pushbutton.setIcon(icon3)
            self.menuSettings.setEnabled(True)
            self.action_toggle_watchdog.setText('Start watchdog')
            self.action_toggle_watchdog.setIcon(icon3)
            self.open_explorer_pushbuttom.setEnabled(False)
            self.open_browser_button.setEnabled(False)
            self.edit_custom_html_file_pushbutton.setEnabled(False)
            if self.protocol_editor:
                self.protocol_editor.hide()
            self.action_Load_experiment.setEnabled(True)

    def changed_microscope(self, microscope):
        """
        Change the microscope.

        Parameters
        ----------
        microscope : name of the microscope
            For the moment the following microscopes are accepted:
                1. Quattro.
                2. Versa.
                3. Vega.
                4. XL40-GB
                5. XL40-Cold
            If an invalid name is provided, the microscope is set back to Quattro

        Returns
        -------
        None.

        """
        log.info('Setting protocol parameters for microscope %s', microscope)
        self.microscope = microscope
        if microscope not in ['Quattro', 'Versa', 'Vega', 'XL40-GB', 'XL40-Cold']:
            self.microscope = 'Quattro'
            log.error('Microscope %s not yet implemented, reverting to default Quattro' % microscope)
            self.select_microscope_comboBox.setCurrentText('Quattro')
            self.microscope = 'Quattro'
        self.validate_inputs()

    @Slot(bool)
    def disable_inputs(self, set_disable: bool = True) -> None:
        """
        Disable the main window inputs.

        As soon as the watchdog is started, it is important to disable the
        input fields to avoid possible problems.

        Parameters
        ----------
        set_disable : bool, optional
            If set to False, the inputs will be enabled. The default is True.

        Returns
        -------
        None.

        """
        self.protocol_folder_text.setEnabled(not set_disable)
        self.select_protocol_folder.setEnabled(not set_disable)
        if self.is_mirroring_requested:
            self.mirroring_folder_text.setEnabled(not set_disable)
        if self.is_custom_ownership_requested:
            self.projectID_field.setEnabled(not set_disable)
            self.project_name_field.setEnabled(not set_disable)
            self.responsible_field.setEnabled(not set_disable)
        self.select_mirroring_folder.setEnabled(not set_disable)
        self.mirror_checkBox.setEnabled(not set_disable)
        self.select_microscope_comboBox.setEnabled(not set_disable)
        self.custom_ownership_checkbox.setEnabled(not set_disable)

    @Slot(bool)
    def toggled_mirroring(self, toggled):
        """
        Act upon a change in the mirror_checkBok.

        TODO: understand if we can remove the toggled argument, because it is not used.

        Parameters
        ----------
        toggled : bool
            the status.

        Returns
        -------
        None.

        """
        if self.mirror_checkBox.isChecked():
            self.is_mirroring_requested = True
        else:
            self.is_mirroring_requested = False
        self.validate_inputs()

    @Slot(bool)
    def toggled_custom_ownership(self, toggled):
        """
        Act upon a change in the custom_ownership_checkbox.

        TODO: understand if we can remove the toggled argument, because it is not used.

        Parameters
        ----------
        toggled : bool
            the status.

        Returns
        -------
        None.
        """
        if self.custom_ownership_checkbox.isChecked():
            self.is_custom_ownership_requested = True
        else:
            self.is_custom_ownership_requested = False
        self.validate_inputs()

    @Slot()
    def toggled_watchdog(self):
        """
        Emulate the behavior of a toggle button.

        The watchdog pushbutton has to work like a toggle switch.
        You press it once and the process starts, you press it again and
        it stops.

        We can perform also a facelift to the push button to change its
        text and the icon.

        Returns
        -------
        None.

        """
        # first change the status of the watchdog
        self.is_watchdog_running = not self.is_watchdog_running

        # update the pushbutton appearance
        self.watchdog_pushbutton_facelift()

    def open_browser(self):
        """
        Open a resource browser pointing to the monitored folder.

        Returns
        -------
        None.

        """
        command = f'explorer {str(self.protocol_folder_path)}'
        self.browser_process = subprocess.Popen(command.split())

    def open_protocol_webpage(self):
        """Open the protocol webpage using the default browser."""
        url = self.workers['SingleWatchdog'].autoprotocol_instance.get_protocol_url()
        webbrowser.open(url, new=0, autoraise=True)

    def open_yaml_editor(self):
        """
        Open the protocol editor.

        Returns
        -------
        None.

        """
        if not self.protocol_editor:
            self.protocol_editor = ProtocolEditor(parent=self,
                                                  autolog=self.workers['SingleWatchdog'].autoprotocol_instance)
            self.protocol_editor.execute_filesystem_command.connect(self.receive_filesystem_command)

        self.protocol_editor.scroll_to_last_selected_item()
        self.protocol_editor.show()
        self.protocol_editor.raise_()
        self.protocol_editor.activateWindow()

    @Slot(FileSystemCommand)
    def receive_filesystem_command(self, command: FileSystemCommand):
        patched_command = self.patch_command_path(command)
        self.file_system_commander.execute(patched_command)

    def patch_command_path(self, command: FileSystemCommand) -> FileSystemCommand:

        if command.input_path.is_absolute():
            log.warning('Unable to patch command path because it is absolute')
            log.warning('The command will be applied to the original path (%s)' % str(command.input_path))
            return command
        else:
            input_path = self.protocol_folder_path / command.input_path
            output_path = None if command.output_path is None else self.protocol_folder_path / command.output_path
            return FileSystemCommand(command.command, input_path, output_path)

    @Slot()
    def open_protocol_folder(self):
        """Open a file dialog for the protocol folder."""
        directory = self.protocol_folder_text.text()
        if not directory:
            directory = str(Path(autoconfig.DEFAULT_PROTOCOL_FOLDER))
        returnpath = QFileDialog.getExistingDirectory(
            self, 'Select a protocol folder', directory=directory)
        if returnpath:
            returnpath = Path(returnpath)
            self.protocol_folder_path = returnpath
            self.protocol_folder_text.setText(str(returnpath))
            self.validate_inputs()

    @Slot()
    def open_mirroring_folder(self):
        """Open a file dialog for the mirroring folder."""
        directory = self.mirroring_folder_text.text()
        if not directory:
            directory = str(Path(autoconfig.DEFAULT_MIRRORING_FOLDER))
        returnpath = QFileDialog.getExistingDirectory(self, 'Select a mirroring folder',
                                                      directory=directory)
        if returnpath:
            returnpath = Path(returnpath)
            self.mirroring_folder_path = returnpath
            self.mirroring_folder_text.setText(str(returnpath))
            self.validate_inputs()

    def _strip_spaces(self):
        line_edit_list = [self.protocol_folder_text,
                          self.mirroring_folder_text,
                          self.projectID_field,
                          self.project_name_field,
                          self.responsible_field]

        for line in line_edit_list:
            if line.isEnabled():
                line.setText(line.text().strip())

    def validate_inputs(self):  # noqa: C901
        """
        Validate all inputs.

        The input_folder can be local_path on the microscope PC or directly on the
        image server, while the mirroring_folder must be on the image server.

        We need to check that:
            1. The protocol folder is not Invalid. If Invalid just quit.
            2. If the mirroring switch is selected then:
                2.1 Check that the Mirroring folder is not Invalid
                2.2 If the custom ownership is requested:
                    2.2.1 Are the custom ownership fields ok?
                        2.2.1.1 If yes: The mirroring can be Acceptable or
                                AcceptableIfCustomOwnership
                        2.2.1.2 If No: The mirroring must be Acceptable
                2.3 If the custom ownership is not requested:
                    2.3.1 The mirroring must be Acceptable
            3. If the mirroring switch is not selected then:
                3.1 If the custom ownership is requested:
                    3.1.1 Are the custom ownership fields ok?
                        3.1.1.1 If yes: the protocol folder can be Acceptable or
                                AcceptableIfCustomOwnership
                        3.1.1.2 If no: the protocol folder must be Acceptable.
                3.2 If the custom ownership is not requested:
                    3.2.1 The protocol folder must be Acceptable

        Returns
        -------
        None.

        """
        present_gui_content = MainWindow.GUIContent.from_main_window(self)
        if self.current_gui_content == present_gui_content:
            # nothing changed.
            # no need to continue
            return

        self.current_gui_content = present_gui_content

        if self.current_gui_content != self.last_loaded_gui_content:
            self.experiment_need_save = True
            if not self.windowTitle().endswith(self.title_modifier):
                self.setWindowTitle(f'{self.windowTitle()}{self.title_modifier}')
        else:
            self.experiment_need_save = False
            if self.windowTitle().endswith(self.title_modifier):
                self.setWindowTitle(self.windowTitle().rstrip(self.title_modifier))

        self._strip_spaces()

        protocol_folder = PathValidator(self.protocol_folder_text.text(),
                                        autoconfig.IMAGE_SERVER_BASE_PATH, self.pattern)
        protocol_folder_validity = protocol_folder.validate()
        protocol_ownership_variables = protocol_folder.get_ownership_parameters()

        mirroring_folder = PathValidator(self.mirroring_folder_text.text(),
                                         autoconfig.IMAGE_SERVER_BASE_PATH, self.pattern)
        mirroring_folder_validity = mirroring_folder.validate()
        mirroring_ownership_variables = mirroring_folder.get_ownership_parameters()

        custom_ownership_validity = self.projectID_field.text() and self.project_name_field.text() \
            and self.responsible_field.text()

        # Condition 1
        if protocol_folder_validity != PathValidator.Invalid:
            # transfer the field text to the variable
            self.protocol_folder_path = Path(self.protocol_folder_text.text())
        else:
            # check if the field text is not empty
            if self.protocol_folder_text.text():
                # print a warning message
                log.warning('Protocol input folder is invalid')
            self.enable_watchdog(False)
            # stop here, it doesn't make sense to continue
            return

        # Condition 2
        if self.is_mirroring_requested:
            # if we get here the protocol_folder_validity is for sure not Invalid

            # Condition 2.1
            if mirroring_folder_validity != PathValidator.Invalid:
                # the mirroring folder is either Acceptable, AccetableIfMirroring or
                # AcceptableIfCustomOwnership

                # Condition 2.2
                if self.is_custom_ownership_requested:

                    # Condition 2.2.1
                    if custom_ownership_validity:
                        self.projectID = self.projectID_field.text()
                        self.project_name = self.project_name_field.text()
                        self.project_responsible = self.responsible_field.text()

                        # Condition 2.2.1.1
                        if mirroring_folder_validity in (PathValidator.Acceptable,
                                                         PathValidator.AcceptableIfCustomOwnership):
                            # we are good to go
                            # transfer the field texts to the parameters and enable the
                            # watchdog
                            self.mirroring_folder_path = Path(self.mirroring_folder_text.text())
                            self.enable_watchdog(True and self.are_user_credentials_ok()
                                                 and self.is_elog_entry_editable(self.projectID)
                                                 )

                            if mirroring_folder_validity == PathValidator.Acceptable:
                                # inform the user that the custom ownership variables
                                # will be used
                                log.info('Custom parameters will be used (#=%s, Project=%s, Responsible=%s)' %
                                         (self.projectID, self.project_name, self.project_responsible))

                            return
                        else:
                            if mirroring_folder_validity == PathValidator.AcceptableIfCustomOwnership:
                                log.warning('Please specify all three custom parameters')
                            self.enable_watchdog(False)

                    else:
                        # the three ownership fields are empty
                        self.projectID = None
                        self.project_name = None
                        self.project_responsible = None

                        # Condition 2.2.1.2
                        if mirroring_folder_validity == PathValidator.Acceptable:

                            # we are good to go
                            # transfer the field texts to the parameters and enable the
                            # watchdog
                            self.mirroring_folder_path = Path(
                                self.mirroring_folder_text.text())
                            self.projectID_field.setText(
                                mirroring_ownership_variables[0])
                            self.project_name_field.setText(
                                mirroring_ownership_variables[1])
                            self.responsible_field.setText(
                                mirroring_ownership_variables[2])
                            self.enable_watchdog(
                                True and self.are_user_credentials_ok()
                                and self.is_elog_entry_editable(mirroring_ownership_variables[0]))

                            return

                        else:
                            log.warning(
                                'Please specify all three custom parameters')
                            self.enable_watchdog(False)
                            # stop here, it doesn't make sense to continue
                            return

                # Condition 2.3
                else:
                    self.projectID = None
                    self.project_name = None
                    self.project_responsible = None

                    # Condition 2.3.1
                    if mirroring_folder_validity == PathValidator.Acceptable:
                        # we are good to go
                        # transfer the field texts to the parameters and enable the
                        # watchdog
                        self.mirroring_folder_path = Path(
                            self.mirroring_folder_text.text())

                        self.projectID_field.setText(mirroring_ownership_variables[0])
                        self.project_name_field.setText(mirroring_ownership_variables[1])
                        self.responsible_field.setText(mirroring_ownership_variables[2])
                        self.enable_watchdog(True and self.are_user_credentials_ok()
                                             and self.is_elog_entry_editable(mirroring_ownership_variables[0]))
                        return

                    else:
                        if mirroring_folder_validity == PathValidator.AcceptableIfCustomOwnership:
                            log.warning('Please activate Use custom parameters')
                            log.warning('Please specify all three custom parameters')
                        else:
                            if self.mirroring_folder_text.text():
                                # print the error message only if the input field is
                                # not empty
                                log.error('Mirroring folder is invalid')
                        self.enable_watchdog(False)

            else:
                # the mirroring folder is Invalid.
                # check if the field text is not empty
                if self.mirroring_folder_text.text():
                    # print the error message only if the input field is
                    # not empty
                    log.error('Mirroring folder is invalid')
                self.enable_watchdog(False)

        # Condition 3
        # the mirroring is not requested.
        else:

            # Condition 3.1
            if self.is_custom_ownership_requested:

                # Condition 3.1.1
                if custom_ownership_validity:
                    self.projectID = self.projectID_field.text()
                    self.project_name = self.project_name_field.text()
                    self.project_responsible = self.responsible_field.text()

                    # Condition 3.1.1.1
                    if protocol_folder_validity in (PathValidator.Acceptable,
                                                    PathValidator.AcceptableIfCustomOwnership):
                        # we are good to go
                        # transfer the field texts to the parameters and enable the
                        # watchdog
                        self.protocol_folder_path = Path(self.protocol_folder_text.text())
                        self.enable_watchdog(True and self.are_user_credentials_ok()
                                             and self.is_elog_entry_editable(self.projectID))
                        return
                    else:
                        # all other cases should be already analyzed
                        log.warning('The protocol folder is valid only if mirroring is selected')
                        self.enable_watchdog(False)
                else:
                    # the three ownership fields are empty
                    self.projectID = None
                    self.project_name = None
                    self.project_responsible = None

                    # Condition 3.1.1.2
                    if protocol_folder_validity == PathValidator.Acceptable:
                        # we are good to go
                        # transfer the field texts to the parameters and enable the
                        # watchdog
                        self.protocol_folder_path = Path(
                            self.protocol_folder_text.text())
                        # display the ownership variables in the disable field
                        self.projectID_field.setText(
                            protocol_ownership_variables[0])
                        self.project_name_field.setText(
                            protocol_ownership_variables[1])
                        self.responsible_field.setText(
                            protocol_ownership_variables[2])
                        self.enable_watchdog(
                            True and self.are_user_credentials_ok()
                            and self.is_elog_entry_editable(protocol_ownership_variables[0]))
                        return
                    else:
                        # all other cases should be already analyzed
                        log.warning('The protocol folder is valid only if mirroring is selected')
                        if protocol_ownership_variables:
                            self.projectID_field.setText(
                                protocol_ownership_variables[0])
                            self.project_name_field.setText(
                                protocol_ownership_variables[1])
                            self.responsible_field.setText(
                                protocol_ownership_variables[2])
                        self.enable_watchdog(False)

            # Condition 3.2
            else:

                self.projectID = None
                self.project_name = None
                self.project_responsible = None

                # Condition 3.2.1
                if protocol_folder_validity == PathValidator.Acceptable:
                    # we are good to go
                    # transfer the field texts to the parameters and enable the
                    # watchdog
                    self.protocol_folder_path = Path(
                        self.protocol_folder_text.text())
                    # fill in the ownership field with the guessed values
                    self.projectID_field.setText(
                        protocol_ownership_variables[0])
                    self.project_name_field.setText(
                        protocol_ownership_variables[1])
                    self.responsible_field.setText(
                        protocol_ownership_variables[2])
                    self.enable_watchdog(
                        True and self.are_user_credentials_ok()
                        and self.is_elog_entry_editable(protocol_ownership_variables[0]))
                    return
                else:
                    # all other cases should be already analyzed
                    log.warning(
                        'The protocol folder is valid only if mirroring is selected')
                    if protocol_ownership_variables:
                        self.projectID_field.setText(
                            protocol_ownership_variables[0])
                        self.project_name_field.setText(
                            protocol_ownership_variables[1])
                        self.responsible_field.setText(
                            protocol_ownership_variables[2])
                    self.enable_watchdog(False)

    @retry(retry=retry_if_exception_type(LogbookServerTimeout),
           reraise=True, stop=stop_after_attempt(autoconfig.ELOG_TIMEOUT_MAX_RETRY),
           wait=wait_fixed(autoconfig.ELOG_TIMEOUT_WAIT),
           after=after_log(log, logging.WARNING))
    def is_elog_entry_editable(self, protocol_id):
        """
        Check if the entry with protocol_id is editable.

        This method is checking if there is an entry with Protocol ID exactly
        matching the protocol_id of the current protocol.

        If this is found, then it is checking if this is read-only. In this case
        the handle_readonly_entry function is called in order to give the
        possibility to the user to resolve the issue.

        Parameters
        ----------
        protocol_id : string
            The protocol ID of the current protocol. It is either guessed from
            the folder name or from the custom ownership method.

        Returns
        -------
        editable_flag : bool
            True if there are no entries with Protocol ID exactly matching the
            protocol_id.
            True if an entry with the exact matching Protocol ID is found and
            it is editable
            True if the user decided to override the read-only flag or to make
            a backup.
            False if the user decided to manually edit the protocol ID of the
            current experiment.

        """
        elog_instance = elog.open(
            hostname=self.config['elog']['elog_hostname'],
            port=self.config['elog']['elog_port'],
            user=self.config['elog']['elog_user'],
            password=self.config['elog']['elog_password'],
            use_ssl=True,
            encrypt_pwd=False,
            logbook=self.config[self.select_microscope_comboBox.currentText(
            )]['logbook']
        )
        msg_ids = elog_instance.search({'Protocol ID': protocol_id}, timeout=autoconfig.ELOG_TIMEOUT)
        real_ids = []
        for ID in msg_ids:
            message, attributes, attachments = elog_instance.read(
                ID, timeout=autoconfig.ELOG_TIMEOUT)
            if attributes['Protocol ID'] == protocol_id:
                real_ids.append(ID)

        # TODO: handle the case in which more than one entry has an exactly matching protocol ID
        if real_ids:
            message, attributes, attchments = elog_instance.read(real_ids[0])
            if attributes.get('Edit Lock', 'Unprotected') == 'Protected':
                log.error('An entry with protocol ID %s already exists and it is read-only' % protocol_id)
                # we need to ask the user how to recover this situation
                return self.handle_readonly_entry(protocol_id, elog_instance, msg_ids[0])
            else:
                # the entry is not locked
                return True
        # there are no entries with this number
        return True

    def handle_readonly_entry(self, protocol_id, elog_instance, msg_id):
        """
        Handle the case of a read only entry.

        This method is called by the is_elog_entry_editable to handle the
        user interaction as a response to the fact that the entry is read-only.

        It will open a dialog window explaining the problem and offering the
        three solutions:
            Overwrite: the edit-lock is switched off and the read-only entry is
                turned editable.

            Backup: the read-only entry is backed up in another entry with the same
                content but where the protocol number has been edited inserting
                a backup tag.

            Edit: the user has the possibility to modify the protocol number of
                the current entry hopefully not corresponding to another
                read-only entry.

        Parameters
        ----------
        protocol_id : string
            The protocol ID of the current protocol. It is either guessed from
            the folder name or from the custom ownership method.
        elog_instance : elog.Logbook
            The elog instance to be quiered.
        msg_id : int
            The message ID of the read-only entry.

        Returns
        -------
        editable_flag : bool
            True if the user decides to override the read-only flag or to make
            a backup.
            False if the user decides to manually edit the protocol ID of the
            current experiment.

        """
        dialog = ReadOnlyEntryDialog(self)
        dialog.set_message(protocol_id)
        if dialog.exec_():
            if dialog.decision == ReadOnlyDecision.Overwrite:
                self.force_overwrite_readonly(elog_instance, msg_id)
                return True
            elif dialog.decision == ReadOnlyDecision.Backup:
                self.backup_readonly(elog_instance, msg_id)
                return True
            else:
                # ReadOnlyDecision.Edit
                log.warning('Manually change the protocol ID to a new value')
                self.manual_edit_protocol()
                return False
        else:
            # dialog cancel.
            log.warning(
                'Cancel dialog: manually change the protocol ID to a new value')
            self.manual_edit_protocol()
            return False

    @staticmethod
    def force_overwrite_readonly(elog_instance, msg_id):
        """
        Override the read-only flag of an entry.

        This method takes message msg_id from elog_instance and turns the
        read-only flag to Unprotected.

        Parameters
        ----------
        elog_instance : elog.Logbook
            The elog instance to be quiered.
        msg_id : int
            The message ID of the read-only entry.

        Returns
        -------
        None.

        """
        message, attributes, attachments = elog_instance.read(msg_id)
        attributes['Edit Lock'] = 'Unprotected'
        elog_instance.post(
            message, msg_id=msg_id, attributes=attributes, attachments=attachments, encoding='HTML',
            timeout=autoconfig.ELOG_TIMEOUT)
        log.info('Set protocol ID %s entry to editable' %
                 attributes['Protocol ID'])

    @staticmethod
    def backup_readonly(elog_instance, msg_id):
        """
        Execute a backup of a read-only entry.

        It takes from elog_instance the entry number msg_id and duplicate it
        renaming the ProtocolID by adding a timestamp.

        Parameters
        ----------
        elog_instance : elog.Logbook
            The elog instance to be quiered.
        msg_id : int
            The message ID of the read-only entry.

        Returns
        -------
        None.

        """
        message, attributes, attachments = elog_instance.read(msg_id)
        attributes['Protocol ID'] = f'{attributes["Protocol ID"]}-{datetime.now():%Y%m%d-%H%M%S} (backup)'
        elog_instance.post(
            message, msg_id, attributes=attributes, attachments=attachments, encoding='HTML',
            timeout=autoconfig.ELOG_TIMEOUT)
        log.info('Previous read-only entry renamed in %s' %
                 attributes['Protocol ID'])

    def manual_edit_protocol(self):
        """
        Allow manual editing of protocol ID.

        The user wants to preserve the existing entry as read-only and prefers
        to change the protocol ID number to a something different.

        To accomplish this, the custom ownership switch is turned on and the
        three custom ownership fields are enabled.

        Returns
        -------
        None.

        """
        self._sleep_input(True)
        self.custom_ownership_checkbox.setChecked(True)
        self.is_custom_ownership_requested = True
        wl = [self.projectID_field, self.project_name_field, self.responsible_field]
        for w in wl:
            w.setEnabled(True)
        self.projectID_field.setFocus()
        self._sleep_input(False)

    def are_user_credentials_ok(self):
        """
        Check whether the user credentials are ok.

        If the credentianls were never checked before, perform a validity check
        trying to connect to the elog and download some numbers.

        If the check fails, the user is prompted with a dialog window to re-introduce
        the credentials. This occurs in a loop with a maximum number of repetition
        defined by the configuration variable max_auth_error.

        Returns
        -------
        bool
            The status of the user credentials..

        """
        if not self.are_user_credentials_checked:
            log.info('Verifying user credentials')

            for i in range(self.config.getint('elog', 'max_auth_error')):
                if self._are_user_credentials_ok():
                    return True
                else:
                    self._edit_user_credentials()

            log.error('Wrong user name and password.')
            log.error('Use Settings/Change User credentials to correct the problem and continue.')
            return False
        else:
            self.are_user_credentials_checked = True
            return True

    @retry(retry=retry_if_exception_type(LogbookServerTimeout),
           reraise=True, stop=stop_after_attempt(autoconfig.ELOG_TIMEOUT_MAX_RETRY),
           wait=wait_fixed(autoconfig.ELOG_TIMEOUT_WAIT),
           after=after_log(log, logging.WARNING))
    def _are_user_credentials_ok(self):
        try:
            elog_instance = elog.open(
                hostname=self.config['elog']['elog_hostname'],
                port=self.config['elog']['elog_port'],
                user=self.config['elog']['elog_user'],
                password=self.config['elog']['elog_password'],
                use_ssl=True,
                encrypt_pwd=False,
                logbook=self.config[self.select_microscope_comboBox.currentText(
                )]['logbook']
            )

            elog_instance.get_message_ids(timeout=autoconfig.ELOG_TIMEOUT)
        except elog.LogbookAuthenticationError:
            return False
        return True

    def edit_user_credentials(self):
        """Open the user credentials dialog."""
        self._edit_user_credentials()
        self.validate_inputs()

    def _edit_user_credentials(self):
        dialog = UserEditor(self, username=self.config['elog']['elog_user'],
                            password=self.config['elog']['elog_password'])
        if dialog.exec_():
            self.config['elog']['elog_user'] = dialog.username
            self.config['elog']['elog_password'] = dialog.password
            autotools.init(self.config)
            self.are_user_credentials_checked = False

    def enable_watchdog(self, is_ok):
        """
        Make the watchdog able to start.

        This method is called after the input validation.

        Parameters
        ----------
        is_ok : BOOL
            If True, the watchdog is enabled and the relevant parameters are
            transferred to the Worker

        Returns
        -------
        None.

        """
        self.watchdog_pushbutton.setEnabled(is_ok)
        self.actionSta_rt_watchdog.setEnabled(is_ok)
        self.is_watchdog_enabled = is_ok
        self.actionSave_experiment.setEnabled(is_ok)

        params_to_be_sent = dict()
        if is_ok and not self.is_watchdog_running:
            params_to_be_sent['original_path'] = self.protocol_folder_path
            params_to_be_sent['is_mirroring_requested'] = self.mirror_checkBox.isChecked()
            if params_to_be_sent['is_mirroring_requested']:
                params_to_be_sent['destination_path'] = self.mirroring_folder_path
            else:
                params_to_be_sent['destination_path'] = self.protocol_folder_path
            params_to_be_sent['microscope'] = self.select_microscope_comboBox.currentText()
            params_to_be_sent['projectID'] = self.projectID
            params_to_be_sent['project_name'] = self.project_name
            params_to_be_sent['responsible'] = self.project_responsible

            # send all parameters to the worker
            self.workers['SingleWatchdog'].update_parameters(**params_to_be_sent)

            # inform the rest of the software about the new autoprotocol_instance
            self.change_autolog.emit(self.workers['SingleWatchdog'].autoprotocol_instance)

            log.info('Folder selection is ok. Ready to start the watchdog')

    @Slot()
    def clear_logger(self):
        """
        Clear the logger message box.

        This slot is called by the clear logger button clicked event

        Returns
        -------
        None.

        """
        self.log_message_box.clear()

    @Slot()
    def save_logger(self):
        """
        Save the content of the logger message box.

        The user has the possibility to save the content as a simple plain text
        or as a formatted HTML document, since the document is actually originally
        formatted as HTML.

        Returns
        -------
        None.

        """
        directory = Path.home() / Path('Documents')
        logger_file = QFileDialog.getSaveFileName(self, 'Logger file name',
                                                  filter='HTML file (*.html);;Text file (*.txt)',
                                                  directory=str(directory))
        if logger_file[0]:
            if logger_file[1] == 'HTML file (*.html)':
                text = str(self.log_message_box.document().toHtml())
            elif logger_file[1] == 'Text file (*.txt)':
                text = str(self.log_message_box.toPlainText())
            else:
                text = 'Wrong format'
            with open(Path(logger_file[0]), 'w') as lf:
                lf.write(text)

    def show_about(self):
        """
        Show the about dialog.

        Returns
        -------
        None.

        """
        dialog = AboutDialog(self)
        dialog.exec_()

    def load_experiment(self):
        """
        Load an experiment file.

        An experiment file is a modified version of a configuration file with a
        dedicated section to the GUI. In this way, all GUI fields are preset
        to the values stored in the file.

        After loading, the validate_inputs method is called so that if everything
        is ok, the Start Watchdog is enabled and all parameters are sent to the
        workers.

        Returns
        -------
        None.

        """
        if self.experiment_need_save:
            ans = QMessageBox.question(self, 'Save current experiment file',
                                       'Before loading a new experiment, would you like to save the current one?',
                                       buttons=QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if ans == QMessageBox.Yes:
                self.save_experiment()
            elif ans == QMessageBox.No:
                pass
            else:  # ans = QMessageBox.Cancel
                return
        if self.experiment_filename:
            directory = self.experiment_filename.parent
        else:
            directory = Path.home() / 'Documents'
        returnpath = QFileDialog.getOpenFileName(self, 'Open experiment file',
                                                 directory=str(directory),
                                                 filter='Experiments (*.exp)')
        if returnpath[0]:
            self._load_experiment(returnpath[0])
            self.experiment_filename = Path(returnpath[0])

    def _sleep_input(self, sleep):
        widget_list = [self.protocol_folder_text,
                       self.mirroring_folder_text,
                       self.mirror_checkBox,
                       self.select_microscope_comboBox,
                       self.custom_ownership_checkbox,
                       self.projectID_field,
                       self.project_name_field,
                       self.responsible_field
                       ]
        for widget in widget_list:
            widget.blockSignals(sleep)

    def _load_experiment(self, path):
        config = autotools.safe_configread(path)
        self.experiment_filename = str(path)
        self.config = config
        autotools.init(config)
        self._sleep_input(True)
        self.protocol_folder_text.setText(str(Path(config['GUI']['src_path'])))
        if config['GUI']['mirror_path']:
            self.mirroring_folder_text.setText(str(Path(config['GUI']['mirror_path'])))
        else:
            self.mirroring_folder_text.clear()
        self.mirror_checkBox.setChecked(config.getboolean('GUI', 'mirror'))
        self.is_mirroring_requested = self.mirror_checkBox.isChecked()
        self.mirroring_folder_text.setEnabled(self.mirror_checkBox.isChecked())
        self.select_microscope_comboBox.setCurrentText(config['GUI']['microscope'])
        self.custom_ownership_checkbox.setChecked(config.getboolean('GUI', 'custom_ownership', fallback=False))
        self.is_custom_ownership_requested = self.custom_ownership_checkbox.isChecked()
        self.projectID_field.setEnabled(self.custom_ownership_checkbox.isChecked())
        self.project_name_field.setEnabled(self.custom_ownership_checkbox.isChecked())
        self.responsible_field.setEnabled(self.custom_ownership_checkbox.isChecked())
        self.projectID_field.setText(config.get('GUI', 'projectID', fallback=''))
        self.project_name_field.setText(config.get('GUI', 'project_name', fallback=''))
        self.responsible_field.setText(config.get('GUI', 'responsible', fallback=''))
        log.info('Loaded experiment %s and updated configuration' % str(Path(path)))
        self.are_user_credentials_checked = False
        self.last_loaded_gui_content = MainWindow.GUIContent.from_main_window(self)
        self.validate_inputs()
        self.watchdog_pushbutton.setFocus()
        self._sleep_input(False)
        self.experiment_need_save = False
        if self.windowTitle().endswith(self.title_modifier):
            self.setWindowTitle(self.windowTitle().rstrip(self.title_modifier))

    def save_experiment(self):
        """
        Save the experiment file.

        An experiment file is a modified version of a configuration file with a
        dedicated section to the GUI. In this way, all GUI fields are preset
        to the values stored in the file.

        Returns
        -------
        None.

        """
        if self.experiment_filename:
            directory = self.experiment_filename
        else:
            directory = Path.home() / 'Documents'
            # let's try to see if from the protocol parameters we can build up the experiment filename.
            # the three protocol customization fields contain their values even if they are not active.
            # we need to check if they are not empty, because maybe the user is saving the file before having set the path.
            custom_projects_info = [self.projectID_field.text(), self.project_name_field.text(),
                                    self.responsible_field.text()]

            if all(custom_projects_info):
                filename = '-'.join(custom_projects_info) + '.exp'
                directory = directory / Path(filename)

        returnpath = QFileDialog.getSaveFileName(self, 'Save experiment file',
                                                 directory=str(directory), filter='Experiments (*.exp)')
        if returnpath[0]:
            self._save_experiment_file(returnpath[0])
            log.info('Experiment file save to %s' % str(Path(returnpath[0])))
            self.experiment_filename = Path(returnpath[0])
            self.experiment_need_save = False
            if self.windowTitle().endswith(self.title_modifier):
                self.setWindowTitle(self.windowTitle().rstrip(self.title_modifier))

            self.update_remote_experiment_file()

    def _save_experiment_file(self, filename):
        self.current_gui_content.transfer_to_config(self.config)
        autotools.write_conffile(self.config, filename)

    def update_remote_experiment_file(self):

        elog_instance = elog.open(
            hostname=self.config['elog']['elog_hostname'],
            port=self.config['elog']['elog_port'],
            user=self.config['elog']['elog_user'],
            password=self.config['elog']['elog_password'],
            use_ssl=True,
            encrypt_pwd=False,
            logbook=self.config['elog']['microscopy_protocol_list']
        )

        # search if there is an entry with exactly this protocol id
        msg_ids = elog_instance.search({'Protocol number': self.projectID_field.text()},
                                       timeout=autoconfig.ELOG_TIMEOUT)
        real_ids = list()
        for msg_id in msg_ids:
            message, attributes, attachments = elog_instance.read(msg_id, timeout=autoconfig.ELOG_TIMEOUT)
            if attributes['Protocol number'] == self.projectID_field.text():
                real_ids.append(msg_id)

        if len(real_ids) == 0:
            log.info(
                'Unable to update the remote protocol experiment because an entry with the current protocol number (%s) could not be found.' % self.projectID_field.text())
        elif len(real_ids) > 1:
            log.info(
                'Unable to update the remote protocol experiment because more than one entry with the current protocol number (%s) was found.' % self.projectID_field.text())
            log.warning('Please review the protocol list because there is ')
        else:
            # we have only one entry, so we update it
            message, attributes, attachments = elog_instance.read(msg_ids[0], timeout=autoconfig.ELOG_TIMEOUT)
            attachments = [str(self.experiment_filename), ]
            elog_instance.post(message, msg_id=msg_ids[0], attributes=attributes, attachments=attachments,
                               timeout=autoconfig.ELOG_TIMEOUT)

    def check_threads_status(self):
        """
        Check the status of the various threads.

        When called, this method will check if the expected threads are alive or
        not and change the icon of a label in the GUI.
        """
        red_led = QtGui.QPixmap(":/resources/icons8-red-circle-48.png")
        green_led = QtGui.QPixmap(":/resources/icons8-green-circle-48.png")
        thread_names = [t.name for t in threading.enumerate()]
        thread_name_to_check = {'GUIThread': self.gui_thread_status,
                                'WatchThread': self.auto_thread_status,
                                'WatchThreadObs': self.auto_obs_status,
                                'WatchThreadEmi0': self.auto_emi_status}
        for name, label in thread_name_to_check.items():
            if name in thread_names:
                label.setPixmap(green_led)
            else:
                label.setPixmap(red_led)

    def hide_debug_elements(self, switch: bool):
        """
        Hide debug elements from the GUI.

        Parameters
        ----------
        switch: bool
            If True, the debug elements will be set hidden.
        """
        debug_elements = [self.gui_thread_status,
                          self.auto_thread_status,
                          self.auto_obs_status,
                          self.auto_emi_status,
                          self.GUIThreadLabel,
                          self.AutoThreadLabel
                          ]
        for element in debug_elements:
            element.setHidden(switch)


class FileSystemCommander(QObject):
    def __init__(self):
        super().__init__()

    def execute(self, command: FileSystemCommand):
        self.on_any_command(command)
        {
            autotools.FSCommandType.DELETE_FILE: self.on_delete_file,
            autotools.FSCommandType.DELETE_DIR: self.on_delete_dir,
            autotools.FSCommandType.RENAME_FILE: self.on_rename_file,
            autotools.FSCommandType.RENAME_DIR: self.on_rename_dir,
            autotools.FSCommandType.MOVE_FILE: self.on_move_file,
        }[command.command](command)

    @staticmethod
    def on_any_command(command):
        # log.vipdebug(str(command))
        pass

    @staticmethod
    def on_rename_file(command):
        try:
            command.input_path.rename(command.output_path)
        except FileExistsError:
            log.error('A file with name %s already exists. Delete this first!' % command.input_path.name)

    @staticmethod
    def on_rename_dir(command):
        try:
            command.input_path.rename(command.output_path)
        except FileExistsError:
            log.error('A directory with name %s already exists. Delete this first!' % command.input_path.name)

    @staticmethod
    def on_delete_file(command):
        command.input_path.unlink()
        log.info('Removed file %s' % str(command.input_path))

    @staticmethod
    def on_delete_dir(command):
        shutil.rmtree(command.input_path, ignore_errors=True)
        log.info('Removed directory %s' % str(command.input_path))

    @staticmethod
    def on_move_file(command):
        # be sure that the destination folder exists.
        command.output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            command.input_path.rename(command.output_path)
        except FileExistsError:
            log.error('A file with name %s already exists. Delete this first!' % command.input_path.name)


def override_credentials(args, config):
    """
    Override configuration file provided user credentials.

    If the user provides username and/or password from the command line,
    these have the priority over credentials stored in configuration files.

    **NOTE**
    Credentials saved in experiment files are **NOT** overridden!

    Parameters
    ----------
    args : namespace
        The namespace of command line arguments as obtained from the
        parse_arguments.
    config : dictionary
        The configuration dictionary as provided by the configuration parser.

    Returns
    -------
    None.

    """
    if args.username:
        config['elog']['elog_user'] = args.username
        # if username is provided, check if password is provided as well.
        # if no password is provided, set it to None so that the dialog window
        # will show up
        if args.password:
            config['elog']['elog_password'] = autotools.encrypt_pass(
                args.password)
        else:
            config['elog']['elog_password'] = ''
    else:
        # this is strange but possible: the user just wants to override the password,
        # but not the username.
        if args.password:
            config['elog']['elog_password'] = autotools.encrypt_pass(
                args.password)


def generate_tool_button_menu_from_scheme(menu: QMenu | None, parent: QObject, menu_scheme: dict) -> QMenu():
    if menu is None:
        menu = QMenu(parent)

    icon = QIcon()
    for element in menu_scheme.values():
        new_action = QAction(element['text'], menu)
        icon.addPixmap(QPixmap(element['icon']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        new_action.setIcon(icon)
        new_action.triggered.connect(element['slot'])
        menu.addAction(new_action)

    return menu


def generate_context_menu_from_scheme(context_menu: QMenu | None, parent: QObject, menu_scheme: dict) -> QMenu:
    if context_menu is None:
        # the context_menu passed by the user is empty. it means that we need to create one.
        context_menu = QMenu(parent)
        for element in menu_scheme.values():
            # we need to replace the context_menu object to the scheme
            if element['parent_name'] == 'root':
                element['parent_obj'] = context_menu

    icon = QIcon()

    for key, element in menu_scheme.items():
        new_item = element['type'](element['text'], element['parent_obj'])
        new_item.setObjectName(element['name'])

        # use the set property method of the QObject to store the show_when_flag
        # this can be done for QMenus and QActions
        new_item.setProperty('visibility', element['show_when_flag'])
        element['obj'] = new_item

        if isinstance(new_item, QAction):
            new_item.setText(element['text'])
            # noinspection PyUnresolvedReferences
            new_item.triggered.connect(element['slot'])
            element['parent_obj'].addAction(new_item)
            # new_item.setData(element['show_when_flag'])
            if element.get('short_cut_key_sequence', None):
                sc = QShortcut(element['short_cut_key_sequence'], parent, member=element['slot'])
                new_item.setShortcut(sc.key())

        else:  # if isinstance(new_item, QMenu):
            new_item.setTitle(element['text'])
            element['parent_obj'].addMenu(new_item)

        if element.get('icon', None):
            icon.addPixmap(QtGui.QPixmap(element['icon']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            new_item.setIcon(icon)

        if element['separator_after']:
            element['parent_obj'].addSeparator()

        # I need to reloop in order to update its child.
        for e in menu_scheme.values():
            if key == e['parent_name']:
                e['parent_obj'] = new_item
    return context_menu


def filter_context_menu(menu: QMenu, visibility: VisibilityFlag):
    for element in menu.actions():
        if element.isSeparator():
            pass
        elif element.menu():
            filter_context_menu(element.menu(), visibility)
            if 'visibility' in element.dynamicPropertyNames():
                element.setVisible(bool(element.property('visibility') & visibility))
            else:
                element.setVisible(True)
        else:  # element is action
            if 'visibility' in element.dynamicPropertyNames():
                element.setVisible(bool(element.property('visibility') & visibility))
            else:
                element.setVisible(True)

    for element in menu.actions():
        if element.menu():
            item_visibility = [sub_el.isVisible() for sub_el in element.menu().actions() if not sub_el.isSeparator()]
            element.setVisible(any(item_visibility))


def main_gui(args):
    """
    Open the main window and start the Qt Event loop.

    Parameters
    ----------
    args : system arguments
        The system arguments can be provided when starting the app.

    Returns
    -------
    None.

    """
    # give a name at the main thread
    threading.current_thread().name = 'GUIThread'

    # prepare the logging machinery
    loglevel = autoconfig.LEVELS.get(args.loglevel.lower())
    log.setLevel(level=loglevel)

    # check if the specified configuration file exists and loaded
    if not args.conffile.exists():
        # it looks like that the specified configuration file doesn't exist,
        # so we need to create one
        autotools.write_default_conffile(args.conffile)
    config = autotools.safe_configread(args.conffile)

    # if user provided username and password from the command line,
    # they must override the configuration file ones.
    override_credentials(args, config)

    # configure the whole package
    autotools.init(config)

    # start the Qt App
    if args.noapp:
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)
    win = MainWindow(app, config)

    # if the user preloaded an experiment file, then do it here
    if args.expfile:
        try:
            win._load_experiment(args.expfile)
            # if the user wants to start the watchdog right away,
            # do it, but before check that it is ok to do it.
            if win.is_watchdog_enabled and args.autoexec:
                timer = QtCore.QTimer()
                timer.setSingleShot(True)
                timer.timeout.connect(win.watchdog_pushbutton.clicked.emit)
                timer.start(100)
        except elog.LogbookServerProblem as err:
            log.critical('Logbook server problem')
            log.exception(err)
        except elog.LogbookAuthenticationError:
            log.error('Wrong user name and password.')
            log.error(
                'Use Settings/Change User credentials to correct the problem and continue.')

    # show the main window
    win.show(loglevel=loglevel)
    if args.noapp and args.autoexec and win.is_watchdog_enabled:
        win.watchdog_pushbutton.clicked.emit()

    # execute the main window and eventually exit when done!
    if not args.noapp:
        sys.exit(app.exec())


def main():
    parser = autotools.main_parser()
    parser.prog = 'autologbook-gui'
    args = parser.parse_args(sys.argv[1:])

    # to set the icon on the window task bar
    myappid = u'ecjrc.autologook.gui.v0.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    main_gui(args)
