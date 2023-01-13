import os
import tempfile

import pyforms
from pyforms_gui.controls.control_checkbox import ControlCheckBox
from pyforms_gui.controls.control_textarea import ControlTextArea
from scipy.io import wavfile
import numpy as np
from AnyQt import QtGui
from AnyQt.QtWidgets import QFileDialog, QStatusBar
from confapp import conf
from pybpod_soundcard_module.utils.generate_sound import generate_sound, WindowConfiguration
from pyforms_gui.basewidget import BaseWidget
from pyforms_gui.controls.control_button import ControlButton
from pyforms_gui.controls.control_combo import ControlCombo
from pyforms_gui.controls.control_emptywidget import ControlEmptyWidget
from pyforms_gui.controls.control_label import ControlLabel
from pyforms_gui.controls.control_number import ControlNumber
from pyforms_gui.controls.control_text import ControlText

from .module_api import SoundCardModule, SampleRate, DataType


class SoundGenerationPanel(BaseWidget):

    def __init__(self, parent_win=None, win_flag=None):
        BaseWidget.__init__(self, 'Sound Generation panel', parent_win=parent_win, win_flag=win_flag)

        self._generated = False

        self._save_file_checkbox = ControlCheckBox('Write sound to file',
                                                   default=False,
                                                   changed_event=self.__save_file_checkbox_evt)

        self._filename = ControlText('Sound filename', '', changed_event=self.__filename_changed_evt, enabled=False)
        self._saveas_btn = ControlButton('Save As...', default=self.__prompt_save_file_evt, enabled=False)

        self._freq_label = ControlLabel('Frequency (Hz)', style='margin-left:0')
        self._freq_left = ControlNumber('Left channel', default=1000, minimum=0, maximum=20000)
        self._freq_right = ControlNumber('Right channel', default=1000, minimum=0, maximum=20000)
        self._duration = ControlNumber('Duration (s)', default=1, minimum=0, maximum=10000, decimals=2)

        self._sample_rate = ControlCombo('Sample rate')
        self._sample_rate.add_item('96 KHz', SampleRate._96000HZ)
        self._sample_rate.add_item('192 KHz', SampleRate._192000HZ)

        self._create_window = ControlCheckBox('Create window',
                                              default=True,
                                              changed_event=self.__create_window_checkbox_evt)

        self._left_window_duration = ControlNumber(default=100, minimum=0, maximum=20000)
        self._right_window_duration = ControlNumber(default=100, minimum=0, maximum=20000)
        self._left_apply_window_start = ControlCheckBox(default=True)
        self._right_apply_window_start = ControlCheckBox(default=True)
        self._left_apply_window_end = ControlCheckBox(default=True)
        self._right_apply_window_end = ControlCheckBox(default=True)

        self._left_window_functions = ControlCombo('Left channel window')
        self._left_window_functions.add_item('Hanning', 'Hanning')
        self._left_window_functions.add_item('Hamming', 'Hamming')
        self._left_window_functions.add_item('Blackman', 'Blackman')
        self._left_window_functions.add_item('Bartlett', 'Bartlett')

        self._right_window_functions = ControlCombo('Right channel window')
        self._right_window_functions.add_item('Hanning', 'Hanning')
        self._right_window_functions.add_item('Hamming', 'Hamming')
        self._right_window_functions.add_item('Blackman', 'Blackman')
        self._right_window_functions.add_item('Bartlett', 'Bartlett')

        self._gen_btn = ControlButton('Generate sound',
                                      default=self.__generate_sound_and_save)

        self._wave_int = []

        # Define the organization of the forms
        self.formset = [
            (
                ['_save_file_checkbox',
                    ('_filename', '_saveas_btn'),
                    ['_duration', '_sample_rate'],
                    ('h5:Frequency',  ['_freq_left', '_freq_right'])],
                '    ',
                ['_create_window',
                    ('', 'Left channel', 'Right channel'),
                    ('Duration (ms)', '_left_window_duration', '_right_window_duration'),
                    ('Apply window to start', '_left_apply_window_start', '_right_apply_window_start'),
                    ('Apply window to end', '_left_apply_window_end', '_right_apply_window_end'),
                    '_left_window_functions',
                    '_right_window_functions']
            ),
            '_gen_btn'
        ]

        self.set_margin(10)

    @property
    def sample_rate(self):
        return self._sample_rate.value

    @property
    def filename(self):
        return self._filename.value

    @property
    def wave_int(self):
        return self._wave_int

    @property
    def generated(self):
        return self._generated

    def sound_generated(self):
        pass

    def __create_window_checkbox_evt(self):
        # enable or disable the the window configuration according to the checkbox
        status = self._create_window.value
        self._left_window_duration.enabled = status
        self._left_apply_window_start.enabled = status
        self._left_apply_window_end.enabled = status
        self._left_window_functions.enabled = status
        self._right_window_duration.enabled = status
        self._right_apply_window_start.enabled = status
        self._right_apply_window_end.enabled = status
        self._right_window_functions.enabled = status

    def __filename_changed_evt(self):
        if not self._filename.value:
            self._gen_btn.enabled = False
        else:
            self._gen_btn.enabled = True

    def __prompt_save_file_evt(self):
        """
        Opens a window for the user to select where to save the Harp sound file (.bin extension by default)
        """
        self._filename.value, _ = QFileDialog.getSaveFileName()
        if self._filename.value:
            self._gen_btn.enabled = True
        else:
            self._gen_btn.enabled = False

    def __save_file_checkbox_evt(self):
        self._filename.enabled = self._saveas_btn.enabled = self._save_file_checkbox.value
        if self._filename.value:
            self._gen_btn.enabled = True
        else:
            self._gen_btn.enabled = not self._save_file_checkbox.value

    def __generate_sound_and_save(self):
        if self._save_file_checkbox.value and not self._filename.value:
            self.warning("Please select a destination file for the generated sound", "No sound file selected")
            return

        window_config = WindowConfiguration(left_duration=int(self._left_window_duration.value) / 1000,
                                            left_apply_window_start=self._left_apply_window_start.value,
                                            left_apply_window_end=self._left_apply_window_end.value,
                                            left_window_function=self._left_window_functions.value,
                                            right_duration=int(self._right_window_duration.value) / 1000,
                                            right_apply_window_start=self._right_apply_window_start.value,
                                            right_apply_window_end=self._right_apply_window_end.value,
                                            right_window_function=self._right_window_functions.value)

        self._wave_int = generate_sound(self._filename.value,
                                        # _sample_rate.value is an Enum so we need to get the value from it
                                        self._sample_rate.value.value,
                                        self._duration.value,
                                        int(self._freq_left.value),
                                        int(self._freq_right.value),
                                        window_config)

        self.sound_generated()
        self._generated = True


class LoadSoundPanel(BaseWidget):

    def __init__(self, parent_win=None, win_flag=None):
        BaseWidget.__init__(self, 'Load sound panel', parent_win=parent_win, win_flag=win_flag)

        self._loaded = False

        self._filename = ControlText('Sound file', '')
        self._read_btn = ControlButton('Browse', default=self.__prompt_read_file_evt)

        self._wave_int = []

        self.formset = [
            ('_filename', '_read_btn')
        ]

        self.set_margin(10)

    def __prompt_read_file_evt(self):
        """
        Opens a window for user to select where to save the sound .bin file
        """
        self._filename.value, _ = QFileDialog.getOpenFileName(caption='Choose sound file',
                                                              filter='Harp sound file(*.bin);;WAV(*.wav)')
        if self._filename.value:
            # assume that if the file extension ends .wav is a wave file, otherwise just try to read as a Harp sound
            if self._filename.value.endswith('.wav'):
                try:
                    fs, data = wavfile.read(self._filename.value)
                except Exception:
                    self.critical("Error while opening the WAV file. Please try again or try loading another file.")
                    return
                self._wave_int = np.array(data, dtype=np.int32)
            else:
                self._wave_int = np.fromfile(self._filename.value, dtype=np.int32)

            self.sound_loaded()
            self._loaded = True

    @property
    def wave_int(self):
        return self._wave_int

    @property
    def loaded(self):
        return self._loaded

    def sound_loaded(self):
        pass


class SoundCardModuleGUI(SoundCardModule, BaseWidget):
    TITLE = 'Sound Card module'

    def __init__(self, parent_win=None):
        BaseWidget.__init__(self, self.TITLE, parent_win=parent_win)

        self._msg_duration = 3000

        self._usb_port = ControlCombo('USB port', changed_event=self.__combo_usb_ports_changed_evt)
        self._refresh_usb_ports = ControlButton('',
                                                icon=QtGui.QIcon(conf.REFRESH_SMALL_ICON),
                                                default=self.__refresh_usb_ports_btn_pressed,
                                                helptext="Press here to refresh the list of available devices.")
        self._connect_btn = ControlButton('Connect', default=self.__connect_btn_pressed)

        # Send data
        self._send_btn = ControlButton('Send to sound card', default=self.__send_btn_pressed, enabled=False)
        self._index_to_send = ControlNumber('Index to send', default=2, minimum=2, maximum=32)
        self._user_metadata_send = ControlTextArea('User metadata (optional)')
        self._description_send = ControlTextArea('Description (optional)')

        self._send_panel = ControlEmptyWidget()
        self._send_panel.value = [self._index_to_send,
                                  self._user_metadata_send,
                                  self._description_send,
                                  self._send_btn]
        self._send_panel.setContentsMargins(10, 10, 10, 10)

        # Receive data
        self._index_to_read = ControlNumber('Index to read', default=2, minimum=2, maximum=32)
        self._read_all_checkbox = ControlCheckBox('Read all indexes',
                                                  default=False,
                                                  changed_event=self.__read_all_checkbox_evt)
        self._clear_folder_checkbox = ControlCheckBox('Clear destination folder', default=False)
        self._dest_folder = ControlText('Destination folder', '', changed_event=self.__folder_changed_evt)
        self._browse_btn = ControlButton('Browse', default=self.__prompt_browse_file_evt)
        self._read_btn = ControlButton('Read data', default=self.__read_btn_pressed, enabled=False)

        self._receive_panel = ControlEmptyWidget()
        self._receive_panel.value = [self._read_all_checkbox,
                                     self._index_to_read,
                                     self._clear_folder_checkbox,
                                     self._dest_folder,
                                     self._browse_btn,
                                     self._read_btn]

        self._receive_panel.setContentsMargins(10, 10, 10, 10)

        self._sound_generation = SoundGenerationPanel(parent_win=self)
        self._sound_generation.sound_generated = self._sound_generated_evt
        self._sound_gen_panel = ControlEmptyWidget()
        self._sound_gen_panel.value = self._sound_generation

        self._sound_load = LoadSoundPanel(parent_win=self)
        self._sound_load.sound_loaded = self._sound_loaded_evt
        self._sound_load_panel = ControlEmptyWidget()
        self._sound_load_panel.value = self._sound_load

        self._sound_card = SoundCardModule()
        self._wave_int = []

        self.formset = [
            ('_usb_port', '_refresh_usb_ports', '_connect_btn'),
            {
                'a:Generate sound': ['_sound_gen_panel'],
                'b:Load sound from disk': ['_sound_load_panel'],
            },
            ' ',
            {
                'a:Send data': ['_send_panel'],
                'b:Receive data': ['_receive_panel']
            }
        ]

        self._fill_usb_ports()

        self.set_margin(10)

        self._status_bar = QStatusBar(parent=self)

    def init_form(self):
        super(SoundCardModuleGUI, self).init_form()
        self.layout().addWidget(self._status_bar)

    def _fill_usb_ports(self):
        self._usb_port.add_item('', '')
        if self._sound_card:
            usb_devices = self._sound_card.devices
            for n, item in enumerate(usb_devices):
                if item.port_number:
                    item_str = item.product + ' {n} (port={port})'.format(n=n, port=item.port_number)
                else:
                    item_str = item.product + ' {n}'.format(n=n)

                self._usb_port.add_item(item_str, item)

    def _sound_generated_evt(self):
        if self._sound_generation.filename:
            self._status_bar.showMessage("Sound generated successfully and saved to '{file}'.".format(
                file=self._sound_generation.filename),
                self._msg_duration)
        else:
            self._status_bar.showMessage("Sound generated successfully.", self._msg_duration)
        if not self._connect_btn.enabled:
            self._send_btn.enabled = True

    def _sound_loaded_evt(self):
        self._status_bar.showMessage("Sound loaded successfully from disk.", self._msg_duration)
        if not self._connect_btn.enabled:
            self._send_btn.enabled = True

    def __read_all_checkbox_evt(self):
        self._index_to_read.enabled = not self._read_all_checkbox.value

    def __read_btn_pressed(self):
        if self._sound_card and not self._sound_card.connected:
            self.warning("Please connect to the sound card before proceeding.", "Not connected to the sound card")
            return

        # check if read all or read a specific index
        index_to_read = None if self._read_all_checkbox.value is True else int(self._index_to_read.value)

        # check if the folder exists
        if not os.path.isdir(self._dest_folder.value):
            self.critical("Folder doesn't exist. Please correct the path to an existing folder and try again",
                          "Path not found")
            return

        # read sound
        self._sound_card.read_sounds(self._dest_folder.value, index_to_read, self._clear_folder_checkbox.value)
        self._status_bar.showMessage("Data read successfully from the sound card", self._msg_duration)

    def __combo_usb_ports_changed_evt(self):
        if self._sound_card:
            self._sound_card.close()
        self._connect_btn.enabled = True
        self._send_btn.enabled = False

    def __refresh_usb_ports_btn_pressed(self):
        tmp = self._usb_port.value
        self._usb_port.clear()
        self._fill_usb_ports()
        self._usb_port.value = tmp

    def __folder_changed_evt(self):
        if not self._dest_folder.value:
            self._read_btn.enabled = False
        else:
            self._read_btn.enabled = True

    def __prompt_browse_file_evt(self):
        self._dest_folder.value = QFileDialog.getExistingDirectory()

        if self._dest_folder.value:
            self._read_btn.enabled = True
        else:
            self._read_btn.enabled = False

    def __connect_btn_pressed(self):
        if not self._usb_port.value:
            self.warning("Please select a USB connected device before proceeding.", "No USB device selected")
            return

        if self._sound_card is not None:
            self._sound_card.close()

        self._sound_card = SoundCardModule(device=self._usb_port.value)

        # update visual elements
        self._connect_btn.enabled = False

        if self._sound_generation.generated or self._sound_load.loaded:
            self._send_btn.enabled = True

    def __send_btn_pressed(self):
        if self._sound_card and not self._sound_card.connected:
            self.warning("Please connect to the sound card before proceeding",
                         "No connection to the sound card established.")
            return

        if (self._sound_generation.generated or self._sound_load.loaded) and self._sound_card.connected:
            wave_int = self._sound_generation.wave_int if self._sound_generation.generated else self._sound_load.wave_int

            # process Filename, metadata info and description data (optional parameters)
            temp_dir = tempfile.gettempdir()
            usr_metadata_file = None
            if self._user_metadata_send:
                usr_metadata_file = os.path.join(temp_dir, 'user_metadata.bin')
                with open(usr_metadata_file, 'w') as f:
                    f.write(self._user_metadata_send.value)

            description_file = None
            if self._description_send:
                description_file = os.path.join(temp_dir, 'description.bin')
                with open(description_file, 'w') as f:
                    f.write(self._description_send.value)

            self._sound_card.send_sound(wave_int,
                                        int(self._index_to_send.value),
                                        self._sound_generation.sample_rate,
                                        DataType.INT32,
                                        os.path.basename(self._sound_generation.filename) if self._sound_generation.filename else "Sound{id:02d}".format(id=int(self._index_to_send.value)),
                                        usr_metadata_file,
                                        description_file
                                        )
            self._status_bar.showMessage("Sound sent successfully to the sound card.", self._msg_duration)

            # delete the temp files
            if usr_metadata_file is not None:
                os.unlink(usr_metadata_file)
            if description_file is not None:
                os.unlink(description_file)


if __name__ == '__main__':
    pyforms.start_app(SoundCardModuleGUI, geometry=(0, 0, 600, 500))
