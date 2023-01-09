import logging
import os
import subprocess
import webbrowser

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import remembering.gui.breathing_dlg
import remembering.gui.details_cw
import remembering.model_old
import remembering.model_old
import remembering.rg_global
import remembering.rg_global
import remembering.timer

MAX_SLIDER_VAL_INT = 8


class MyDialog(QtWidgets.QDialog):
    """
    The dialog which holds the (1) text, (2) image, or (3) breathing widget

    """

    def __init__(self, i_id: int, i_testing_content: bool):
        super().__init__()

        self.setSizeGripEnabled(True)

        self.nr_of_timeouts_int = 0
        self.short_interval_qtimer = None
        self.start_timer()

        self.id_int = i_id
        self.testing_content_bool = i_testing_content

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.main_area_sw = CustomStackedWidget()
        # self.main_area_sw.clicked_signal.connect(self.on_main_area_clicked)
        vbox_l2.addWidget(self.main_area_sw)

        self.text_cw = TextCw()
        self.text_int = self.main_area_sw.addWidget(self.text_cw)
        self.image_cw = ImageCw(self)
        self.image_int = self.main_area_sw.addWidget(self.image_cw)
        self.breathing_cw = BreathingCw()
        self.breathing_int = self.main_area_sw.addWidget(self.breathing_cw)

        # Buttons

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        # hbox_l3.addStretch(1)

        self.slowing_down_qpb = QtWidgets.QProgressBar()
        self.slowing_down_qpb.setMaximumWidth(400)
        self.slowing_down_qpb.setMinimum(0)
        self.slowing_down_qpb.setMaximum(MAX_SLIDER_VAL_INT)
        self.slowing_down_qpb.setFormat("Please slow down and take this in slowly")
        # self.slowing_down_qpb.setTextVisible(False)
        # valueChanged
        hbox_l3.addWidget(self.slowing_down_qpb)

        self.done_qcb = QtWidgets.QCheckBox("Done")
        self.done_qcb.toggled.connect(self.on_done_toggled)
        hbox_l3.addWidget(self.done_qcb)

        """
        self.mini_breathing_area = MiniBreathingArea()
        hbox_l3.addWidget(self.mini_breathing_area)
        """

        self.edit_qpb = QtWidgets.QPushButton("Edit")
        # -TODO: using an icon here instead?
        self.edit_qpb.setDisabled(True)
        hbox_l3.addWidget(self.edit_qpb)

        self.delay_qsb = QtWidgets.QSpinBox()
        # self.delay_qsb.setValue(0)
        self.delay_qsb.setMinimum(0)
        self.delay_qsb.setMaximum(1000)  # -minutes
        self.delay_qsb.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum,
            self.delay_qsb.sizePolicy().verticalPolicy()
        )
        self.delay_qsb.setDisabled(False)
        hbox_l3.addWidget(self.delay_qsb)

        """
        self.delay_qpb = QtWidgets.QPushButton("Delay")
        hbox_l3.addWidget(self.delay_qpb)
        """

        self.close_qpb = QtWidgets.QPushButton("<b>Close</b>")
        self.close_qpb.clicked.connect(self.on_close_clicked)
        hbox_l3.addWidget(self.close_qpb)

        self.next_qpb = QtWidgets.QPushButton("Next")
        self.next_qpb.clicked.connect(self.on_next_clicked)
        hbox_l3.addWidget(self.next_qpb)

        # hbox_l3.addStretch(1)

        # self.showMaximized()
        self.showFullScreen()

        # hashtags

        self.update_gui()

    def on_done_toggled(self, i_checked: bool):
        self.delay_qsb.setDisabled(i_checked)

    def start_timer(self):
        self.stop_timer()
        self.short_interval_qtimer = QtCore.QTimer(self)
        self.short_interval_qtimer.timeout.connect(self.timer_timeout)
        self.short_interval_qtimer.start(1000)  # -one tenth of a second

    def stop_timer(self):
        if self.short_interval_qtimer is not None and self.short_interval_qtimer.isActive():
            self.shared_minute_qtimer.stop()
            self.nr_of_timeouts_int = 0

    def timer_timeout(self):
        # logging.debug("short_interval_timer_timeout")
        self.nr_of_timeouts_int += 1

        if self.nr_of_timeouts_int >= MAX_SLIDER_VAL_INT:
            self.done_qcb.setChecked(True)
        self.slowing_down_qpb.setValue(self.nr_of_timeouts_int)

    def on_close_clicked(self):
        self.close()

    def on_edit_clicked(self):
        pass

    def on_next_clicked(self):
        fired_notifications_list = \
            remembering.model_old.RememberItem.get_sorted_ids_of_fired_notifications(
            [
                remembering.model_old.ContentType.text,
                remembering.model_old.ContentType.image
            ])
        if len(fired_notifications_list) > 0:
            self.id_int = fired_notifications_list[0]
            self.update_gui()
        else:
            self.close()

    def update_gui(self):
        remembrance = remembering.model_old.RememberItem.get_item(self.id_int)
        if remembrance.content_type_enum == remembering.model_old.ContentType.text:
            self.main_area_sw.setCurrentIndex(self.text_int)
            self.text_cw.update_gui(remembrance.content_str)
        elif remembrance.content_type_enum == remembering.model_old.ContentType.image:
            self.main_area_sw.setCurrentIndex(self.image_int)
            self.image_cw.update_gui(remembrance.content_str)
        elif remembrance.content_type_enum == remembering.model_old.ContentType.breathing:
            self.main_area_sw.setCurrentIndex(self.breathing_int)
            self.breathing_cw.update_gui(remembrance.content_str)

        ############################
        if not self.testing_content_bool:
            remembering.model_old.Remembrances.update_notif_fired(self.id_int, False)


class TextCw(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox_l2)

        self.text_qll = QtWidgets.QLabel()
        self.text_qll.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard
        )
        self.text_qll.setWordWrap(True)
        new_font = self.text_qll.font()
        new_font.setPointSize(20)
        self.text_qll.setFont(new_font)

        self.text_qll.setFixedWidth(750)
        # -the combination of point size 20 and width 750 gives approx. 60 characters per line
        #  and the recommended is 45-75, so this is right in the middle

        self.scroll_area = CustomScrollArea()  # QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scroll_area.setAlignment(QtCore.Qt.AlignCenter)
        # self.scroll_area.resize_signal.connect(self.resize_image)
        self.scroll_area.setWidget(self.text_qll)
        self.vbox_l2.addWidget(self.scroll_area)
        self.scroll_area.setFocus()  # -keyboard focus

        self.scroll_area.setWidget(self.text_qll)

    def update_gui(self, i_text: str):
        self.text_qll.setText(i_text)


class BreathingCw(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox_l2)

        self.in_phrase_qll = QtWidgets.QLabel()
        self.in_phrase_qll.setWordWrap(True)
        self.in_phrase_qll.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored,
            self.in_phrase_qll.sizePolicy().verticalPolicy()
        )
        self.in_phrase_qll.setFixedWidth(1200)
        self.in_phrase_qll.setAlignment(QtCore.Qt.AlignCenter)
        new_font = self.in_phrase_qll.font()
        new_font.setPointSize(32)
        self.in_phrase_qll.setFont(new_font)
        self.vbox_l2.addWidget(self.in_phrase_qll, alignment=QtCore.Qt.AlignHCenter)

        self.breathing_dlg = remembering.gui.breathing_dlg.BreathingDlg(i_can_be_closed=False)
        self.vbox_l2.addWidget(self.breathing_dlg, alignment=QtCore.Qt.AlignCenter)

        self.out_phrase_qll = QtWidgets.QLabel()
        self.out_phrase_qll.setFont(new_font)
        self.vbox_l2.addWidget(self.out_phrase_qll, alignment=QtCore.Qt.AlignHCenter)

        """
        self.play_audio_qpb = QtWidgets.QPushButton("Play audio")
        self.play_audio_qpb.clicked.connect(self.on_play_audio_clicked)
        self.play_audio_qpb.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum,
            self.play_audio_qpb.sizePolicy().verticalPolicy()
        )
        self.vbox_l2.addWidget(self.play_audio_qpb, alignment=QtCore.Qt.AlignHCenter)
        """

    def on_play_audio_clicked(self):
        pass

    def update_gui(self, i_text: str):
        io_list = i_text.split(sep=";")
        t_ib_str = io_list[0]
        t_ob_str = ""
        if len(io_list) > 1:
            t_ob_str = io_list[1]
        self.breathing_dlg.set_io_phrases(t_ib_str, t_ob_str)
        self.in_phrase_qll.setText(t_ib_str)
        self.out_phrase_qll.setText(t_ob_str)
        # self.text_qll.setText(i_text)


class ImageCw(QtWidgets.QWidget):
    def __init__(self, i_parent):
        super().__init__(parent=i_parent)

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox_l2)

        self.image_qll = QtWidgets.QLabel(parent=self)
        self.image_qll.setScaledContents(True)

        #########self.vbox_l2.addWidget(self.image_qll)

        # self.update_gui()
        # rg.nn_global.resize_image(self.image_qll, 650)

        self.scroll_area = CustomScrollArea()  # QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scroll_area.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area.resize_signal.connect(self.resize_image)
        self.scroll_area.setWidget(self.image_qll)
        self.vbox_l2.addWidget(self.scroll_area)
        self.scroll_area.setFocus()  # -keyboard focus

    def resize_image(self):
        if self.image_qll.pixmap() is None:
            return
        image_width_int = self.image_qll.pixmap().width()
        image_height_int = self.image_qll.pixmap().height()
        if image_width_int == 0:
            return
        main_window_width_int = self.scroll_area.width()
        main_window_height_int = self.scroll_area.height()
        width_relation_float = image_width_int / main_window_width_int
        height_relation_float = image_height_int / main_window_height_int

        # if width_relation_float > 1.0 or height_relation_float > 1.0:  # -scaling down
        if width_relation_float > height_relation_float:
            if main_window_height_int < 2 * image_height_int:
                scaled_image_height_int = main_window_height_int
            else:
                scaled_image_height_int = 2 * image_height_int
            scaled_image_width_int = (scaled_image_height_int / image_height_int) * image_width_int
        else:
            if main_window_width_int < 2 * image_width_int:
                scaled_image_width_int = main_window_width_int
            else:
                scaled_image_width_int = 2 * image_width_int
            scaled_image_height_int = (scaled_image_width_int / image_width_int) * image_height_int
        self.image_qll.setFixedWidth(scaled_image_width_int)  # - 20
        self.image_qll.setFixedHeight(scaled_image_height_int)  # - 20
        # -can resize be used instead? there seems to be some difference in how it works

    def update_gui(self, i_file_path: str):
        # self.resize_image()
        # self.setup_scroll_area_widget()
        self.image_qll.setPixmap(QtGui.QPixmap(i_file_path))


class CustomScrollArea(QtWidgets.QScrollArea):
    resize_signal = QtCore.Signal()
    next_image_signal = QtCore.Signal()
    prev_image_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()

    # overridden
    def resizeEvent(self, i_QResizeEvent):
        super().resizeEvent(i_QResizeEvent)
        self.resize_signal.emit()


def open_file_or_dir(i_path: str):
    try:
        os.startfile(i_path)
        # -only available on windows
    except:
        subprocess.Popen(["xdg-open", i_path])


def launch_action(i_id: int, i_testing_content: bool) -> None:
    # TODO: Move this so that it's shared with the test button
    remembrance = remembering.model_old.RememberItem.get_item(i_id)
    if (remembrance.content_type_enum == remembering.model_old.ContentType.text
            or remembrance.content_type_enum == remembering.model_old.ContentType.breathing
            or remembrance.content_type_enum == remembering.model_old.ContentType.image):
        textorimage_cw = MyDialog(i_id, i_testing_content)
        textorimage_cw.exec_()
    elif remembrance.content_type_enum == remembering.model_old.ContentType.web_page:
        webbrowser.open_new_tab(remembrance.content_str)
    elif remembrance.content_type_enum == remembering.model_old.ContentType.custom:
        arg_list = remembrance.content_str.split()
        if len(arg_list) > 1:
            # https://stackoverflow.com/q/19971767/2525237
            try:
                ret_val = subprocess.call(arg_list)
                print("ret_val = " + str(ret_val))
            except:
                logging.warning("Cannot run custom command")
        else:
            open_file_or_dir(arg_list[0])
    else:
        pass

    if not i_testing_content:
        remembering.model_old.Remembrances.update_notif_fired(i_id, False)
        # -this is also done inside the "one by one" part for texts and images

    remembering.model_old.Remembrances.update_last_activated_ts(
        i_id,
        QtCore.QDateTime.currentSecsSinceEpoch()
    )
    # TODO: Finding a better place for this, so that things with the "next" button are included


class CustomStackedWidget(QtWidgets.QStackedWidget):
    clicked_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()

    # overridden
    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked_signal.emit()


class Timer(QtCore.QObject):
    update_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.short_interval_qtimer = None

    def start_timer(self):
        self.stop_shared_minute_timer()
        self.short_interval_qtimer = QtCore.QTimer(self)
        self.short_interval_qtimer.timeout.connect(self.short_interval_timer_timeout)
        self.short_interval_qtimer.start(100)  # -one tenth of a second

    def stop_timer(self):
        if self.shared_minute_qtimer is not None and self.shared_minute_qtimer.isActive():
            self.shared_minute_qtimer.stop()
        # update_gui()

    def short_interval_timer_timeout(self):
        """
        Function is called every minute
        """
        logging.debug("timeout")
        self.show_notifications(False)


class HLine(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.show()


class MiniBreathingArea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.hline = HLine()
        vbox_l2.addWidget(self.hline)

        self.nr_of_timeouts_int = 0
        self.short_interval_qtimer = None
        # self.start_timer()
