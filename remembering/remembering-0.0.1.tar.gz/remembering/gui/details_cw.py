import logging

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import remembering.gui.launch_actions
import remembering.model_old
import remembering.rg_global
import remembering.timer

DEFAULT_FREQ_VALUE_SECS_IF_ACTIVE_INT = 30 * 60


class DetailsCw(QtWidgets.QWidget):
    update_signal = QtCore.Signal(int)  # -id for the updated row/item

    def __init__(self, i_id: int):
        super().__init__()

        self.id_int = i_id

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.updating_gui = True

        self.title_qle = QtWidgets.QLineEdit()
        self.title_qle.setPlaceholderText("Title")
        new_font = self.title_qle.font()
        new_font.setPointSize(new_font.pointSize() + 4)
        self.title_qle.setFont(new_font)
        self.title_qle.textChanged.connect(self.on_title_changed)
        vbox_l2.addWidget(self.title_qle)

        # Content area
        self.shared_content_area_qsw = QtWidgets.QStackedWidget()
        vbox_l2.addWidget(self.shared_content_area_qsw)
        # , stretch=5

        self.text_content_area_cw = TextContentCgbw()
        self.shared_content_area_qsw.addWidget(self.text_content_area_cw)
        self.image_content_area_cw = ImageContentCgbw()
        self.shared_content_area_qsw.addWidget(self.image_content_area_cw)
        self.appl_content_area_cw = ApplicationContentCgbw()
        self.shared_content_area_qsw.addWidget(self.appl_content_area_cw)
        self.web_page_content_area_cw = WebPageContentCgbw()
        self.shared_content_area_qsw.addWidget(self.web_page_content_area_cw)
        self.breathing_content_area_cw = BreathingContentCgbw()
        self.shared_content_area_qsw.addWidget(self.breathing_content_area_cw)
        # -Please note that the order of adding is important

        # vbox_l2.addStretch(1)

        self.test_content_qpb = QtWidgets.QPushButton("Test Content")
        self.test_content_qpb.clicked.connect(self.on_test_content_clicked)
        vbox_l2.addWidget(self.test_content_qpb)

        vbox_l2.addWidget(HLine())
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.dyn_stat_qbg = QtWidgets.QButtonGroup()
        self.dynamic_qpb = QtWidgets.QPushButton("Dynamic")
        self.dynamic_qpb.setCheckable(True)
        hbox_l3.addWidget(self.dynamic_qpb)
        self.dyn_stat_qbg.addButton(self.dynamic_qpb)
        self.static_qpb = QtWidgets.QPushButton("Static")
        self.static_qpb.setCheckable(True)
        hbox_l3.addWidget(self.static_qpb)
        self.dyn_stat_qbg.addButton(self.static_qpb)
        self.dyn_stat_qbg.buttonClicked.connect(self.on_dyn_stat_btn_clicked)

        self.dyn_stat_area_qsw = QtWidgets.QStackedWidget()
        vbox_l2.addWidget(self.dyn_stat_area_qsw)

        self.stat_qll = QtWidgets.QLabel(
            "Static - always shown (when activated) in the system tray menu")
        new_font = self.stat_qll.font()
        new_font.setItalic(True)
        self.stat_qll.setFont(new_font)
        self.stat_qll.setWordWrap(True)
        self.stat_qll.setContentsMargins(10, 10, 10, 10)
        # self.stat_qll.setAlignment(QtCore.Qt.AlignCenter)
        self.dyn_stat_area_qsw.addWidget(self.stat_qll)

        self.dyn_times_qgb = QtWidgets.QGroupBox("Times for notifications")
        self.dyn_stat_area_qsw.addWidget(self.dyn_times_qgb)
        # vbox_l2.addWidget(self.dyn_times_qgb)
        vbox_l3 = QtWidgets.QVBoxLayout()
        self.dyn_times_qgb.setLayout(vbox_l3)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)

        self.spec_times_qlw = QtWidgets.QListWidget()
        # TODO: self.notifications_in_a_day_qlw.changed.connect
        hbox_l4.addWidget(self.spec_times_qlw)
        self.spec_times_qlw.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Maximum)

        vbox_l5 = QtWidgets.QVBoxLayout()
        hbox_l4.addLayout(vbox_l5)

        self.delete_spec_time_qpb = QtWidgets.QPushButton("del")
        self.delete_spec_time_qpb.clicked.connect(self.on_del_spec_time_clicked)
        vbox_l5.addWidget(self.delete_spec_time_qpb)
        self.now_qpb = QtWidgets.QPushButton("Now")
        self.now_qpb.clicked.connect(self.on_now_clicked)
        vbox_l5.addWidget(self.now_qpb)
        self.time_of_day_qte = QtWidgets.QTimeEdit()
        vbox_l5.addWidget(self.time_of_day_qte)
        self.add_time_of_day_qpb = QtWidgets.QPushButton("Add new")
        self.add_time_of_day_qpb.clicked.connect(self.on_add_spec_time_clicked)
        vbox_l5.addWidget(self.add_time_of_day_qpb)

        vbox_l3.addWidget(HLine())

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)
        self.freq_active_qcb = QtWidgets.QCheckBox("Frequency")
        self.freq_active_qcb.toggled.connect(self.on_freq_toggled)
        hbox_l4.addWidget(self.freq_active_qcb)
        self.frequency_qsb = QtWidgets.QSpinBox()
        self.frequency_qsb.setMinimum(1)
        self.frequency_qsb.setMaximum(999)
        self.frequency_qsb.setValue(DEFAULT_FREQ_VALUE_SECS_IF_ACTIVE_INT)
        self.frequency_qsb.valueChanged.connect(self.on_frequency_changed)
        hbox_l4.addWidget(self.frequency_qsb)
        hbox_l4.addWidget(QtWidgets.QLabel(" minutes"))

        self.update_gui()

        self.updating_gui = False

    def on_dyn_stat_btn_clicked(self):
        if self.updating_gui:
            return
        new_permanent_value_bool = False
        if self.dynamic_qpb.isChecked():
            new_permanent_value_bool = False
        elif self.static_qpb.isChecked():
            new_permanent_value_bool = True
        remembering.model_old.Remembrances.update_permanent(
            remembering.rg_global.current_item_id_int,
            new_permanent_value_bool
        )
        self.update_gui()
        self.update_signal.emit(self.id_int)

    def on_freq_toggled(self, i_checked: bool):
        if self.updating_gui:
            return
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)
        if i_checked:
            if remembrance.notif_freq_secs_int == remembering.model_old.NO_VALUE_SET_INT:
                new_value_secs_int = DEFAULT_FREQ_VALUE_SECS_IF_ACTIVE_INT
                remembering.model_old.Remembrances.update_notif_freq(
                    remembering.rg_global.current_item_id_int,
                    new_value_secs_int
                )
            else:
                pass
        else:
            remembering.model_old.Remembrances.update_notif_freq(
                remembering.rg_global.current_item_id_int,
                remembering.model_old.NO_VALUE_SET_INT
            )

        self.update_notification_time()
        self.update_gui()
        self.update_signal.emit(self.id_int)

    def on_now_clicked(self):
        self.time_of_day_qte.setTime(QtCore.QTime.currentTime())

    def on_del_spec_time_clicked(self):
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)
        new_spec_times_secs_list = remembrance.notif_spec_secs_list
        new_spec_times_secs_list.pop(self.spec_times_qlw.currentRow())
        remembering.model_old.Remembrances.update_spec_times(
            remembering.rg_global.current_item_id_int,
            new_spec_times_secs_list
        )
        self.time_of_day_qte.clear()

        self.update_notification_time()
        self.update_gui()
        self.update_signal.emit(self.id_int)

    def on_add_spec_time_clicked(self):
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)
        new_spec_times_secs_list = remembrance.notif_spec_secs_list
        qtime = self.time_of_day_qte.time()
        qtime.setHMS(qtime.hour(), qtime.minute(), 0)
        new_spec_times_secs_list.append(
            qtime.msecsSinceStartOfDay() // 1000
        )
        remembering.model_old.Remembrances.update_spec_times(
            remembering.rg_global.current_item_id_int,
            new_spec_times_secs_list
        )
        self.time_of_day_qte.clear()

        self.update_notification_time()
        self.update_gui()
        self.update_signal.emit(self.id_int)

    def update_notification_time(self):
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)
        next_notification_time_ts_secs = remembering.model_old.NO_VALUE_SET_INT
        if remembrance.notif_active_bool:
            next_notification_time_ts_secs = remembrance.get_next_notification_time()
        remembering.model_old.Remembrances.update_next_notif(
            int(remembering.rg_global.current_item_id_int),
            next_notification_time_ts_secs
        )

    def on_title_changed(self):
        remembering.model_old.Remembrances.update_title(
            remembering.rg_global.current_item_id_int,
            self.title_qle.text()
        )
        self.update_signal.emit(self.id_int)

    def on_frequency_changed(self):
        if self.updating_gui:
            return
        remembering.model_old.Remembrances.update_notif_freq(
            remembering.rg_global.current_item_id_int,
            int(self.frequency_qsb.value()) * 60
        )

        self.update_notification_time()
        self.update_gui()
        self.update_signal.emit(self.id_int)

    def on_test_content_clicked(self):
        remembering.gui.launch_actions.launch_action(remembering.rg_global.current_item_id_int,
            True)

    def update_gui(self):
        self.updating_gui = True
        if remembering.rg_global.current_item_id_int == remembering.model_old.NO_VALUE_SET_INT:
            return
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)

        self.title_qle.setText(remembrance.title_str)

        active_widget = None
        if remembrance.content_type_enum == remembering.model_old.ContentType.text:
            active_widget = self.text_content_area_cw
        elif remembrance.content_type_enum == remembering.model_old.ContentType.image:
            active_widget = self.image_content_area_cw
        elif remembrance.content_type_enum == remembering.model_old.ContentType.web_page:
            active_widget = self.web_page_content_area_cw
        elif remembrance.content_type_enum == remembering.model_old.ContentType.custom:
            active_widget = self.appl_content_area_cw
        elif remembrance.content_type_enum == remembering.model_old.ContentType.breathing:
            active_widget = self.breathing_content_area_cw
        else:
            pass

        self.shared_content_area_qsw.setCurrentWidget(active_widget)
        self.shared_content_area_qsw.currentWidget().update_gui()

        active_dyn_stat_widget = None
        if remembrance.permanent_bool:
            self.static_qpb.setChecked(True)
            active_dyn_stat_widget = self.stat_qll
        else:
            self.dynamic_qpb.setChecked(True)
            active_dyn_stat_widget = self.dyn_times_qgb
        self.dyn_stat_area_qsw.setCurrentWidget(active_dyn_stat_widget)

        times_during_day_secs_list = remembrance.notif_spec_secs_list
        times_qdate_list = [
            QtCore.QTime.fromMSecsSinceStartOfDay(time_during_day_ts_secs * 1000) for
            time_during_day_ts_secs in
            times_during_day_secs_list
        ]  # TODO: making this code nicer, maybe moving it out?
        self.spec_times_qlw.clear()
        self.spec_times_qlw.addItems([qtime.toString("HH:mm") for qtime in times_qdate_list])

        freq_active_bool = False
        if remembrance.notif_freq_secs_int != remembering.model_old.NO_VALUE_SET_INT:
            freq_active_bool = True
        self.freq_active_qcb.setChecked(freq_active_bool)
        self.frequency_qsb.setEnabled(freq_active_bool)

        self.frequency_qsb.setValue(remembrance.notif_freq_secs_int // 60)

        self.updating_gui = False


class ContentCgbw(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("Groupbox title")
        # i_content_type: rg.model.ContentType
        # self.content_type_enum = i_content_type
        self.updating_gui = False

    def update_gui(self):
        pass


class WebPageContentCgbw(ContentCgbw):
    def __init__(self):
        super().__init__()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.content_qle = QtWidgets.QLineEdit()
        self.content_qle.setPlaceholderText("Content")
        self.content_qle.textChanged.connect(self.on_content_qle_changed)
        vbox_l2.addWidget(self.content_qle)

    def on_content_qle_changed(self):
        remembering.model_old.Remembrances.update_content(
            remembering.rg_global.current_item_id_int,
            self.content_qle.text()
        )

    # overridden
    def update_gui(self):
        if remembering.rg_global.current_item_id_int == remembering.model_old.NO_VALUE_SET_INT:
            return
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)

        self.setTitle(remembrance.content_type_enum.name)

        self.content_qle.setText(remembrance.content_str)


class ApplicationContentCgbw(ContentCgbw):
    def __init__(self):
        super().__init__()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.content_qle = QtWidgets.QLineEdit()
        self.content_qle.setPlaceholderText("Content")
        self.content_qle.textChanged.connect(self.on_content_qle_changed)
        hbox_l3.addWidget(self.content_qle)
        self.appl_file_dialog_qpb = QtWidgets.QPushButton("Select")
        self.appl_file_dialog_qpb.clicked.connect(self.on_appl_file_dlg_clicked)
        hbox_l3.addWidget(self.appl_file_dialog_qpb)

    def on_content_qle_changed(self):
        remembering.model_old.Remembrances.update_content(
            remembering.rg_global.current_item_id_int,
            self.content_qle.text()
        )

    def on_appl_file_dlg_clicked(self):
        appl_name_str, _ = QtWidgets.QFileDialog.getOpenFileName()
        # qfiledlg = QtWidgets.QFileDialog()
        self.content_qle.setText(appl_name_str)

    # overridden
    def update_gui(self):
        if remembering.rg_global.current_item_id_int == remembering.model_old.NO_VALUE_SET_INT:
            return
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)

        self.setTitle(remembrance.content_type_enum.name)

        self.content_qle.setText(remembrance.content_str)


class ImageContentCgbw(ContentCgbw):
    def __init__(self):
        super().__init__()
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.content_qle = QtWidgets.QLineEdit()
        self.content_qle.setPlaceholderText("Content")
        self.content_qle.textChanged.connect(self.on_content_qle_changed)
        hbox_l3.addWidget(self.content_qle)
        self.image_file_dialog_qpb = QtWidgets.QPushButton("Select")
        self.image_file_dialog_qpb.clicked.connect(self.on_image_file_dlg_clicked)
        hbox_l3.addWidget(self.image_file_dialog_qpb)

        self.image_preview_qll = QtWidgets.QLabel()
        # self.image_preview_qll.setDisabled(True)
        vbox_l2.addWidget(self.image_preview_qll)

    def on_content_qle_changed(self):
        if self.updating_gui:
            return
        remembering.model_old.Remembrances.update_content(
            remembering.rg_global.current_item_id_int,
            self.content_qle.text()
        )
        self.update_gui()

    def on_image_file_dlg_clicked(self):
        file_name_str, _ = QtWidgets.QFileDialog.getOpenFileName(
            filter="Images (*.png *.xpm *.jpg)")
        # qfiledlg = QtWidgets.QFileDialog()
        self.content_qle.setText(file_name_str)

        self.image_preview_qll.setScaledContents(True)
        self.image_preview_qll.setPixmap(QtGui.QPixmap(file_name_str))
        remembering.rg_global.resize_image(self.image_preview_qll, 150)

    # overridden
    def update_gui(self):
        self.updating_gui = True

        if remembering.rg_global.current_item_id_int == remembering.model_old.NO_VALUE_SET_INT:
            return
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)

        self.setTitle(remembrance.content_type_enum.name)

        self.content_qle.setText(remembrance.content_str)

        self.image_preview_qll.setScaledContents(True)
        self.image_preview_qll.setPixmap(QtGui.QPixmap(remembrance.content_str))
        logging.debug(f"{remembrance.content_str=}")
        remembering.rg_global.resize_image(self.image_preview_qll, 150)

        self.updating_gui = False


class TextContentCgbw(ContentCgbw):
    def __init__(self):
        super().__init__()

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.content_qpte = QtWidgets.QPlainTextEdit()
        self.content_qpte.setPlaceholderText("Content")
        self.content_qpte.textChanged.connect(self.on_content_qpte_changed)
        vbox_l2.addWidget(self.content_qpte)

    def on_content_qpte_changed(self):
        remembering.model_old.Remembrances.update_content(
            remembering.rg_global.current_item_id_int,
            self.content_qpte.toPlainText()
        )
        # rg.nn_global.current_item_id_int

    # overridden
    def update_gui(self):
        if remembering.rg_global.current_item_id_int == remembering.model_old.NO_VALUE_SET_INT:
            return
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)

        self.setTitle(remembrance.content_type_enum.name)

        self.content_qpte.setPlainText(remembrance.content_str)


class BreathingContentCgbw(ContentCgbw):
    def __init__(self):
        super().__init__()

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.in_phrase_qle = QtWidgets.QLineEdit()
        self.in_phrase_qle.setPlaceholderText("In-breath phrase")
        self.in_phrase_qle.textChanged.connect(self.on_content_changed)
        vbox_l2.addWidget(self.in_phrase_qle)

        self.out_phrase_qle = QtWidgets.QLineEdit()
        self.out_phrase_qle.setPlaceholderText("Out-breath phrase")
        self.out_phrase_qle.textChanged.connect(self.on_content_changed)
        vbox_l2.addWidget(self.out_phrase_qle)

    def on_content_changed(self):
        combined_str = self.in_phrase_qle.text() + \
                       remembering.rg_global.BREATHING_PHRASE_SEPARATOR + self.out_phrase_qle.text()
        remembering.model_old.Remembrances.update_content(
            remembering.rg_global.current_item_id_int,
            combined_str
        )

    # overridden
    def update_gui(self):
        if remembering.rg_global.current_item_id_int == remembering.model_old.NO_VALUE_SET_INT:
            return
        remembrance = remembering.model_old.RememberItem.get_item(
            remembering.rg_global.current_item_id_int)

        self.setTitle(remembrance.content_type_enum.name)

        io_phrases_list = remembrance.content_str.split(
            remembering.rg_global.BREATHING_PHRASE_SEPARATOR)
        ib_phrase_str = io_phrases_list[0].strip()
        ob_phrase_str = ""
        if len(io_phrases_list) > 1:
            ob_phrase_str = io_phrases_list[1].strip()
        self.in_phrase_qle.setText(ib_phrase_str)
        self.out_phrase_qle.setText(ob_phrase_str)


class HLine(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.show()
