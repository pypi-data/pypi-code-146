import logging
import os

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import matc.constants
import matc.gui.breathing
import matc.shared
import matc.state

NEW_ROW: int = -1
NEW_IBP_DEFAULT = "Breathing in"
NEW_OBP_DEFAULT = "Breathing out"


class SettingsDlg(QtWidgets.QDialog):
    br_timer_change_signal = QtCore.Signal()
    notif_audio_test_signal = QtCore.Signal()
    br_audio_test_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 64, 400, 540)
        self.setWindowTitle(f"Settings Dialog - {matc.constants.APPLICATION_PRETTY_NAME}")
        self.setWindowIcon(QtGui.QIcon(matc.shared.get_app_icon_path()))
        self.setStyleSheet(
            f"selection-background-color: {matc.shared.LIGHT_GREEN_COLOR};"
            f"selection-color:#000000;"
        )
        self.updating_gui: bool = True

        hbox_l2 = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_l2)
        vbox_l2 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(vbox_l2)

        hbox_br_time_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_br_time_l3)
        hbox_br_time_l3.addWidget(QtWidgets.QLabel("Breathing break time"))
        self.breathing_break_time_qsb = QtWidgets.QSpinBox()
        self.breathing_break_time_qsb.setMinimum(1)
        self.breathing_break_time_qsb.setMaximum(99)
        hbox_br_time_l3.addWidget(self.breathing_break_time_qsb)
        self.breathing_break_time_qsb.valueChanged.connect(self.on_br_time_value_changed)
        hbox_br_time_l3.addWidget(QtWidgets.QLabel("minutes"))

        self.phrases_qgb_l3 = QtWidgets.QGroupBox("Breathing phrases")
        vbox_l2.addWidget(self.phrases_qgb_l3)
        vbox_l4 = QtWidgets.QVBoxLayout()
        self.phrases_qgb_l3.setLayout(vbox_l4)
        self.breathing_phrases_qlw = MyListWidget()
        vbox_l4.addWidget(self.breathing_phrases_qlw)
        self.breathing_phrases_qlw.setSpacing(2)
        # self.breathing_phrases_qlw.itemDoubleClicked.connect(self.on_bp_double_clicked)
        self.breathing_phrases_qlw.drop_signal.connect(self.on_bp_item_dropped)
        self.populate_bp_list()
        hbox_buttons_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(hbox_buttons_l5)
        self.edit_bp_qpb = QtWidgets.QPushButton("Edit")
        hbox_buttons_l5.addWidget(self.edit_bp_qpb)
        self.edit_bp_qpb.clicked.connect(self.on_edit_bp_clicked)
        self.add_bp_qpb = QtWidgets.QPushButton("Add")
        hbox_buttons_l5.addWidget(self.add_bp_qpb)
        self.add_bp_qpb.clicked.connect(self.on_add_bp_clicked)
        self.del_bp_qpb = QtWidgets.QPushButton("Del")
        hbox_buttons_l5.addWidget(self.del_bp_qpb)
        self.del_bp_qpb.clicked.connect(self.on_del_bp_clicked)
        self.list_help_qll = QtWidgets.QLabel(
            '<p>The list items can be reordered using drag-and-drop.</p>'
            '<p>The topmost item is always the first to be shown at application start.</p>'
            '<p>You can change the active phrase from the systray menu (sub-section '
            '"phrases").</p>')
        self.list_help_qll.setWordWrap(True)
        vbox_l4.addWidget(self.list_help_qll)
        """
        self.set_active_bp_qpb = QtWidgets.QPushButton("Set Active")
        hbox_buttons_l5.addWidget(self.set_active_bp_qpb)
        self.set_active_bp_qpb.clicked.connect(self.on_set_active_bp_clicked)
        """

        self.audio_qgb_l3 = QtWidgets.QGroupBox("Audio")
        vbox_l2.addWidget(self.audio_qgb_l3)
        vbox_audio_l4 = QtWidgets.QVBoxLayout()
        self.audio_qgb_l3.setLayout(vbox_audio_l4)
        hbox_master_volume_l5 = QtWidgets.QHBoxLayout()
        vbox_audio_l4.addLayout(hbox_master_volume_l5)
        hbox_master_volume_l5.addWidget(QtWidgets.QLabel("Master volume"))
        self.volume_qsr = QtWidgets.QSlider()
        hbox_master_volume_l5.addWidget(self.volume_qsr)
        self.volume_qsr.valueChanged.connect(self.on_volume_changed)
        self.volume_qsr.setMinimum(0)
        self.volume_qsr.setMaximum(100)
        self.volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.notification_audio_cw = AudioCw("Notification",
            matc.state.SK_NOTIFICATION_AUDIO_FILE_PATH,
            matc.state.SK_NOTIFICATION_AUDIO_VOLUME)
        vbox_audio_l4.addWidget(self.notification_audio_cw)
        self.notification_audio_cw.test_clicked_signal.connect(self.notif_audio_test_signal.emit)
        self.breathing_audio_cw = AudioCw("Breathing",
            matc.state.SK_BREATHING_AUDIO_FILE_PATH,
            matc.state.SK_BREATHING_AUDIO_VOLUME)
        vbox_audio_l4.addWidget(self.breathing_audio_cw)
        self.breathing_audio_cw.test_clicked_signal.connect(self.br_audio_test_signal.emit)

        self.visualizations_qgb_l3 = QtWidgets.QGroupBox("Breathing visualizations")
        hbox_l2.addWidget(self.visualizations_qgb_l3)
        vbox_l4 = QtWidgets.QVBoxLayout()
        self.visualizations_qgb_l3.setLayout(vbox_l4)
        self.bv_group_qbg = QtWidgets.QButtonGroup()
        self.bar_bv_option_cw = BrVisOptionCw(matc.shared.BrVis.bar)
        vbox_l4.addWidget(self.bar_bv_option_cw)
        self.bv_group_qbg.addButton(self.bar_bv_option_cw.qrb, matc.shared.BrVis.bar.value)
        self.circle_bv_option_cw = BrVisOptionCw(matc.shared.BrVis.circle)
        vbox_l4.addWidget(self.circle_bv_option_cw)
        self.bv_group_qbg.addButton(self.circle_bv_option_cw.qrb, matc.shared.BrVis.circle.value)
        self.line_bv_option_cw = BrVisOptionCw(matc.shared.BrVis.line)
        vbox_l4.addWidget(self.line_bv_option_cw)
        self.bv_group_qbg.addButton(self.line_bv_option_cw.qrb, matc.shared.BrVis.line.value)
        self.columns_bv_option_cw = BrVisOptionCw(matc.shared.BrVis.columns)
        vbox_l4.addWidget(self.columns_bv_option_cw)
        self.bv_group_qbg.addButton(self.columns_bv_option_cw.qrb, matc.shared.BrVis.columns.value)
        self.bv_group_qbg.idClicked.connect(self.on_br_vis_id_clicked)

        self.auto_move_mouse_cursor_qcb = QtWidgets.QCheckBox(
            "Auto-move mouse cursor to breathing dialog")
        vbox_l2.addWidget(self.auto_move_mouse_cursor_qcb)
        # self.auto_move_mouse_cursor_qcb.
        self.auto_move_mouse_cursor_qcb.clicked.connect(self.on_auto_move_mouse_cursor_clicked)
        self.auto_move_mouse_cursor_qcb.setToolTip(
            "Automatically move the mouse cursor to the breathing dialog when the breathing "
            "dialog is opened from the system tray menu (convenient if you are using a touchpad)")

        self.update_gui()

    def populate_bp_list(self):  # -right now only called in __init__
        self.breathing_phrases_qlw.clear()
        phrases: list[matc.state.BreathingPhrase] = matc.state.settings[
            matc.state.SK_BREATHING_PHRASES]
        for p in phrases:
            self._add_bp_to_gui(p.id)

    def on_bp_item_dropped(self):
        """
        After any item has been dropped we re-write all the phrases in the model/settings (based on
        the new order in the GUI)
        """
        new_order_phrase_list = []
        for item_row in range(self.breathing_phrases_qlw.count()):
            item = self.breathing_phrases_qlw.item(item_row)
            item_id = item.data(QtCore.Qt.UserRole)
            phrase = matc.state.get_breathing_phrase(item_id)
            new_order_phrase_list.append(phrase)
        matc.state.settings[matc.state.SK_BREATHING_PHRASES] = new_order_phrase_list

    """
    def on_bp_double_clicked(self, i_item: QtWidgets.QListWidgetItem):
        matc.shared.active_phrase_id = i_item.data(QtCore.Qt.UserRole)
        self.update_gui_active_bold()
    """

    def on_auto_move_mouse_cursor_clicked(self, i_checked: bool):
        if self.updating_gui:
            return
        matc.state.settings[matc.state.SK_MOVE_MOUSE_CURSOR] = i_checked

    def on_br_vis_id_clicked(self, i_id: int):
        if self.updating_gui:
            return
        matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION] = i_id

    """
    def on_show_br_phrase_toggled(self, i_checked: bool):
        logging.debug("on_show_br_phrase_toggled")
        if i_checked:
            top_qlwi = self.breathing_phrases_qlw.item(0)
            matc.shared.active_phrase_id = top_qlwi.data(QtCore.Qt.UserRole)
        else:
            matc.shared.active_phrase_id = matc.shared.BREATHING_PHRASE_NOT_SET
        self.update_gui_active_bold()

    def on_set_active_bp_clicked(self):
        current_qlwi = self.breathing_phrases_qlw.currentItem()
        matc.shared.active_phrase_id = current_qlwi.data(QtCore.Qt.UserRole)
        self.update_gui_active_bold()

    def update_gui_active_bold(self):
        for item_row in range(self.breathing_phrases_qlw.count()):
            item = self.breathing_phrases_qlw.item(item_row)
            item_font = item.font()
            if item.data(QtCore.Qt.UserRole) == matc.shared.active_phrase_id:
                item_font.setBold(True)
                item.setFont(item_font)
            elif item_font.bold():
                item_font.setBold(False)
                item.setFont(item_font)

            self.show_breathing_phrase_qcb.setChecked(
                matc.shared.active_phrase_id != matc.shared.BREATHING_PHRASE_NOT_SHOWN
            )
    """

    def on_volume_changed(self, i_new_value: int):
        if self.updating_gui:
            return
        matc.state.settings[matc.state.SK_MASTER_VOLUME] = i_new_value

    def on_add_bp_clicked(self):
        """
        The end result will be that the breathing phrase is that the breathing phrase is not
        added if the user presses cancel in the modal dialog
        """
        new_id: int = matc.state.add_breathing_phrase(NEW_IBP_DEFAULT, NEW_OBP_DEFAULT)
        result = BreathingPhraseEditDialog.start(new_id)
        if result:
            self._add_bp_to_gui(new_id)
        else:
            matc.state.remove_breathing_phrase(new_id)

    def _update_bp_in_gui(self, i_id: int, i_row: int):
        phrase = matc.state.get_breathing_phrase(i_id)
        phrase_text: str = f"{phrase.in_breath}\n{phrase.out_breath}"

        qlwi = QtWidgets.QListWidgetItem(phrase_text)
        self.breathing_phrases_qlw.takeItem(i_row)
        self.breathing_phrases_qlw.insertItem(i_row, qlwi)
        self.breathing_phrases_qlw.setCurrentRow(i_row)

    def _add_bp_to_gui(self, i_id: int, i_row: int = NEW_ROW):
        """
        if i_id == matc.constants.BREATHING_PHRASE_NOT_SET:
            new_font = qlwi.font()
            new_font.setItalic(True)
            qlwi.setFont(new_font)
        if i_id == matc.constants.BREATHING_PHRASE_NOT_SET:
            # phrase_text: str = "nothing"
            raise Exception("BREATHING_PHRASE_NOT_SET --- this should not be possible")
        else:
        """
        phrase = matc.state.get_breathing_phrase(i_id)
        phrase_text: str = f"{phrase.in_breath}\n{phrase.out_breath}"
        qlwi = QtWidgets.QListWidgetItem(phrase_text)
        qlwi.setData(QtCore.Qt.UserRole, i_id)
        if i_row == NEW_ROW:
            self.breathing_phrases_qlw.addItem(qlwi)
            new_row: int = self.breathing_phrases_qlw.count() - 1
            self.breathing_phrases_qlw.setCurrentRow(new_row)
        else:
            self.breathing_phrases_qlw.insertItem(i_row, qlwi)
            self.breathing_phrases_qlw.setCurrentRow(i_row)

    def on_del_bp_clicked(self):
        if self.breathing_phrases_qlw.count() == 0:
            QtWidgets.QMessageBox.information(self, "Cannot remove last item",
                "It's not possible to remove the last item")
            return

        current_item = self.breathing_phrases_qlw.currentItem()
        current_row: int = self.breathing_phrases_qlw.currentRow()
        id_: int = current_item.data(QtCore.Qt.UserRole)

        if matc.state.active_phrase_id == id_:
            QtWidgets.QMessageBox.information(self, "Cannot remove active item",
                "It's not possible to remove the active item. Please switch to another item "
                "before removing this one")
            return
        brp = matc.state.get_breathing_phrase(id_)
        standard_button = QtWidgets.QMessageBox.question(self,
            "Removing br phrase",
            f"Are you sure you want to remove this item:\n\n{brp.in_breath}\n{brp.out_breath}")
        if standard_button == QtWidgets.QMessageBox.Yes:
            matc.state.remove_breathing_phrase(id_)
            self.breathing_phrases_qlw.takeItem(current_row)

    def on_edit_bp_clicked(self):
        current_item = self.breathing_phrases_qlw.currentItem()
        current_row: int = self.breathing_phrases_qlw.currentRow()
        id_: int = current_item.data(QtCore.Qt.UserRole)
        result = BreathingPhraseEditDialog.start(id_)
        if result:
            self._update_bp_in_gui(id_, current_row)

    def on_br_time_value_changed(self, i_new_value: int):
        if self.updating_gui:
            return
        matc.state.settings[matc.state.SK_BREATHING_BREAK_TIMER_SECS] = 60 * i_new_value
        self.br_timer_change_signal.emit()

    # noinspection PyPep8Naming
    def closeEvent(self, i_QCloseEvent):
        matc.state.save_settings_to_json_file()
        super().closeEvent(i_QCloseEvent)

    def update_gui(self):
        self.updating_gui = True

        br_time_value: int = matc.state.settings[matc.state.SK_BREATHING_BREAK_TIMER_SECS]
        self.breathing_break_time_qsb.setValue(br_time_value // 60)

        volume: int = matc.state.settings[matc.state.SK_MASTER_VOLUME]
        self.volume_qsr.setValue(volume)

        # self.update_gui_active_bold()

        active_br_vis_id: int = matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION]
        for btn in self.bv_group_qbg.buttons():
            if self.bv_group_qbg.id(btn) == active_br_vis_id:
                # self.updating_gui = False
                btn.click()
                # self.updating_gui = True

        move_mouse_cursor: bool = matc.state.settings[matc.state.SK_MOVE_MOUSE_CURSOR]
        self.auto_move_mouse_cursor_qcb.setChecked(move_mouse_cursor)

        self.updating_gui = False


class PreviewLabel(QtWidgets.QLabel):
    mouse_press_signal = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, i_qmouseevent: QtGui.QMouseEvent) -> None:
        self.mouse_press_signal.emit()


class ToggleSwitchWt(QtWidgets.QWidget):
    toggled_signal = QtCore.Signal(bool)

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        self.turn_on_off_qcb = QtWidgets.QCheckBox()
        self.turn_on_off_qcb.toggled.connect(self._on_toggled)
        on_off_qhl = QtWidgets.QHBoxLayout()
        on_off_qhl.setContentsMargins(0, 0, 0, 0)
        on_off_qhl.addWidget(
            QtWidgets.QLabel(self.tr("Turn the dialog and notifications on or off")))
        on_off_qhl.addStretch(1)
        on_off_qhl.addWidget(self.turn_on_off_qcb)
        self.setLayout(on_off_qhl)

    def _on_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        self.toggled_signal.emit(i_checked)

    def update_gui(self, i_checked: bool):
        self.updating_gui_bool = True

        self.turn_on_off_qcb.setChecked(i_checked)

        self.updating_gui_bool = False


class BreathingPhraseEditDialog(QtWidgets.QDialog):
    def __init__(self, i_id: int, i_parent=None):
        super().__init__(parent=i_parent)
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setWindowTitle("Edit Breathing Phrase")
        vbox = QtWidgets.QVBoxLayout(self)

        """
        # If a phrase is not selected, default to phrase with id 1
        if matc.shared.active_phrase_id_it == matc.shared.NO_PHRASE_SELECTED_INT:
            matc.shared.active_phrase_id_it = 1
        """

        bp_obj = matc.state.get_breathing_phrase(i_id)

        """
        self.breath_title_qle = QtWidgets.QLineEdit(str(bp_obj.id))
        hbox.addWidget(QtWidgets.QLabel("ID"))
        hbox.addWidget(self.breath_title_qle)
        """

        self.ib_title_qll = QtWidgets.QLabel("In-breath phrase")
        vbox.addWidget(self.ib_title_qll)
        self.in_breath_phrase_qle = QtWidgets.QLineEdit(bp_obj.in_breath)
        vbox.addWidget(self.in_breath_phrase_qle)

        self.ob_title_qll = QtWidgets.QLabel("Out-breath phrase")
        vbox.addWidget(self.ob_title_qll)
        self.out_breath_phrase_qle = QtWidgets.QLineEdit(bp_obj.out_breath)
        vbox.addWidget(self.out_breath_phrase_qle)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

        self.adjustSize()

    @staticmethod
    def start(i_id) -> bool:
        dlg = BreathingPhraseEditDialog(i_id)
        dlg.exec()
        if dlg.result() == QtWidgets.QDialog.Accepted:
            logging.debug("Dialog accepted, updating application settings")
            bp = matc.state.get_breathing_phrase(i_id)
            bp.in_breath = dlg.in_breath_phrase_qle.text()
            bp.out_breath = dlg.out_breath_phrase_qle.text()
            return True
        return False


class MyListWidget(QtWidgets.QListWidget):
    drop_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

    def dropEvent(self, QDropEvent):
        super().dropEvent(QDropEvent)
        self.drop_signal.emit()
        # self.update_db_sort_order_for_all_rows()


class BrVisOptionCw(QtWidgets.QWidget):
    def __init__(self, item: matc.shared.BrVis):
        super().__init__()
        self.hbox = QtWidgets.QHBoxLayout()
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.setLayout(self.hbox)
        self.qrb = QtWidgets.QRadioButton()
        self.setContentsMargins(4, 4, 4, 4)
        self.preview_qll = PreviewLabel()
        pixmap = matc.gui.breathing.BreathingGraphicsView.get_preview_pixmap(item)
        self.preview_qll.setPixmap(pixmap)
        self.preview_qll.mouse_press_signal.connect(self.qrb.click)
        self.hbox.addWidget(self.qrb)
        self.hbox.addSpacing(16)
        self.hbox.addWidget(self.preview_qll)


class AudioCw(QtWidgets.QWidget):
    test_clicked_signal = QtCore.Signal()

    def __init__(self, i_title: str, i_file_path_settings_key: str, i_volume_settings_key: str):
        super().__init__()
        self.file_path_settings_key = i_file_path_settings_key
        self.volume_settings_key = i_volume_settings_key
        self.updating_gui: bool = True

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        hbox = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox)

        self.title_qll = QtWidgets.QLabel(i_title)
        hbox.addWidget(self.title_qll)
        new_font = self.title_qll.font()
        new_font.setBold(True)
        new_font.setPointSize(new_font.pointSize() + 1)
        self.title_qll.setFont(new_font)
        hbox.addStretch(1)
        self.test_qpb = QtWidgets.QPushButton("Test")
        hbox.addWidget(self.test_qpb)
        self.test_qpb.clicked.connect(self.test_clicked_signal.emit)

        hbox = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox)
        self.file_name_qll = QtWidgets.QLabel("File:")
        hbox.addWidget(self.file_name_qll)
        self.file_qcb = QtWidgets.QComboBox()
        hbox.addWidget(self.file_qcb)
        self.file_qcb.currentIndexChanged.connect(self.on_file_index_changed)
        # self.file_qcb.clicked.connect(self.on_change_file_clicked)
        """
        self.change_file_qpb = QtWidgets.QPushButton("Change")
        hbox.addWidget(self.change_file_qpb)
        self.change_file_qpb.clicked.connect(self.on_change_file_clicked)
        """

        hbox = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox)
        self.volume_qll = QtWidgets.QLabel("Volume")
        hbox.addWidget(self.volume_qll)
        self.volume_qsr = QtWidgets.QSlider()
        hbox.addWidget(self.volume_qsr)
        self.volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.volume_qsr.setRange(0, 100)
        self.volume_qsr.setValue(50)
        self.volume_qsr.valueChanged.connect(self.on_volume_value_changed)

        self.update_gui()
        self.updating_gui: bool = False

    def on_volume_value_changed(self, i_new_value: int):
        if self.updating_gui:
            return
        matc.state.settings[self.volume_settings_key] = i_new_value

    def on_file_index_changed(self, i_new_index: int):
        if self.updating_gui:
            return
        audio_file_path: str = self.file_qcb.itemData(i_new_index)
        logging.debug(f"{audio_file_path=}")
        matc.state.settings[self.file_path_settings_key] = audio_file_path

    def update_gui(self):
        self.updating_gui = True

        active_audio_path: str = matc.state.settings[self.file_path_settings_key]

        def add_files_from_dir(i_dir_path) -> int:
            if not os.path.isdir(i_dir_path):
                return 0
            audio_dir_items = [x for x in os.listdir(i_dir_path) if x.endswith(".wav")]
            for audio_fn in sorted(audio_dir_items):
                audio_path = os.path.join(i_dir_path, audio_fn)
                self.file_qcb.addItem(audio_fn, userData=audio_path)
                if audio_path == active_audio_path:
                    index_of_last: int = self.file_qcb.count() - 1
                    self.file_qcb.setCurrentIndex(index_of_last)
            return len(audio_dir_items)

        res_audio_dir = matc.shared.get_audio_path()
        nr_added_res_audio = add_files_from_dir(res_audio_dir)
        config_dir = matc.shared.get_config_path()
        nr_added_config = add_files_from_dir(config_dir)
        if nr_added_config > 0:
            self.file_qcb.insertSeparator(nr_added_res_audio)

        volume: int = matc.state.settings[self.volume_settings_key]
        self.volume_qsr.setValue(volume)

        self.updating_gui = False


if __name__ == "__main__":  # pragma no cover
    import sys

    matc_qapplication = QtWidgets.QApplication(sys.argv)
    win = SettingsDlg()
    win.show()
    sys.exit(matc_qapplication.exec_())
