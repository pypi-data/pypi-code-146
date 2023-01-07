import logging
import sys
import traceback

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

try:
    # noinspection PyUnresolvedReferences
    from PySide6 import QtMultimedia
except ImportError as ie:
    logging.warning("ImportError for QtMultimedia (maybe because there's no sound card available)")
    # -An alternative to this approach is to use this:
    # http://doc.qt.io/qt-5/qaudiodeviceinfo.html#availableDevices
    logging.debug(f"{ie.msg=}")
import matc.constants
import matc.shared
import matc.state
import matc.gui.breathing
import matc.gui.settings_dlg
import matc.gui.intro_dlg
import matc.gui.modal_dialogs

SAME_PHRASE = -1


class MainObject(QtCore.QObject):
    """
    We are using this QObject as the core of the application (rather than using a QMainWindow).
    Areas of responsibility:
    * Breathing timer
    * Settings window
    * Breathing dialog
    * Audio
    * Systray icon and systray menus (and sub-menus)
    """

    def __init__(self, i_is_first_time_ever_started: bool):
        super().__init__()

        # Handling of (otherwise) uncaught exceptions
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                # -"KeyboardInterrupt" includes ctrl+c and exiting the application with the
                # "stop" button in PyCharm
                logging.debug("KeyboardInterrupt")
            else:
                # logging.critical("Uncaught exception", exc_info=(exc_type, exc_value,
                # exc_traceback))
                # matc.gui.modal_dialogs.ErrorDlg.start(f"Uncaught exception: {exc_value}")
                # logging.exception("exception logging----------")
                full_info_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
                full_info_text = "".join(full_info_list)  # -newlines are already added
                matc.gui.modal_dialogs.ErrorDlg.log_and_start(
                    logging.critical, "***Uncaught exception***", full_info_text)

        sys.excepthook = handle_exception
        # -can be tested with: raise RuntimeError("Testing RuntimeError")

        # System tray and menu setup
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self._update_systray_image()
        self.tray_icon.activated.connect(self.on_systray_activated)
        self.tray_menu = QtWidgets.QMenu()  # self
        self.tray_menu.aboutToShow.connect(self.on_tray_menu_about_to_show)
        self.tray_open_breathing_dialog_qaction = QtGui.QAction("Breathing Dialog")
        self.tray_menu.addAction(self.tray_open_breathing_dialog_qaction)
        self.tray_open_breathing_dialog_qaction.triggered.connect(
            self.on_tray_open_breathing_dialog_triggered)
        self.tray_br_phrases_qmenu = QtWidgets.QMenu("Phrases")
        self.tray_br_phrases_qmenu.triggered.connect(self.on_tray_br_phrase_triggered)
        self.tray_menu.addMenu(self.tray_br_phrases_qmenu)
        self.tray_open_settings_action = QtGui.QAction("Settings")
        self.tray_menu.addAction(self.tray_open_settings_action)
        self.tray_open_settings_action.triggered.connect(self.on_tray_open_settings_triggered)
        self.tray_notifications_enabled_action = QtGui.QAction("Notifications enabled")
        self.tray_notifications_enabled_action.setCheckable(True)
        self.tray_notifications_enabled_action.setChecked(True)
        self.tray_menu.addAction(self.tray_notifications_enabled_action)

        self.help_menu = self.tray_menu.addMenu("&Help")
        self.show_intro_dialog_action = QtGui.QAction("Show intro wizard", self)
        self.help_menu.addAction(self.show_intro_dialog_action)
        self.show_intro_dialog_action.triggered.connect(self.show_intro_dialog)
        self.feedback_action = QtGui.QAction("Give feedback", self)
        self.help_menu.addAction(self.feedback_action)
        self.feedback_action.triggered.connect(self.show_feedback_dialog)
        self.sysinfo_action = QtGui.QAction("System Information", self)
        self.help_menu.addAction(self.sysinfo_action)
        self.sysinfo_action.triggered.connect(self.show_sysinfo_box)
        self.about_action = QtGui.QAction("About", self)
        self.help_menu.addAction(self.about_action)
        self.about_action.triggered.connect(self.show_about_box)
        self.check_for_update_action = QtGui.QAction("Check for updates", self)
        self.help_menu.addAction(self.check_for_update_action)
        self.check_for_update_action.triggered.connect(self.check_for_updates)

        self.tray_notifications_enabled_action.toggled.connect(
            self.on_tray_notifications_enabled_toggled)
        self.tray_quit_action = QtGui.QAction("Quit")
        self.tray_menu.addAction(self.tray_quit_action)
        self.tray_quit_action.triggered.connect(self.on_tray_quit_triggered)
        if sys.flags.dev_mode:
            self.debug_menu = self.tray_menu.addMenu("&Debug")
            self.open_config_dir_action = QtGui.QAction("Open config dir", self)
            self.debug_menu.addAction(self.open_config_dir_action)
            self.open_config_dir_action.triggered.connect(self.on_open_config_dir_triggered)
            self.do_manual_gc_action = QtGui.QAction("do manual garbage collection", self)
            self.debug_menu.addAction(self.do_manual_gc_action)
            self.do_manual_gc_action.triggered.connect(self.on_do_manual_gc_triggered)
            self.disable_gc_action = QtGui.QAction("disable garbage collection", self)
            self.debug_menu.addAction(self.disable_gc_action)
            self.disable_gc_action.triggered.connect(self.on_disable_gc_triggered)
            self.raise_exception_action = QtGui.QAction("Raise exception", self)
            self.debug_menu.addAction(self.raise_exception_action)
            self.raise_exception_action.triggered.connect(self.on_raise_exception_triggered)
        self.tray_menu.setDefaultAction(self.tray_open_breathing_dialog_qaction)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.messageClicked.connect(self.on_tray_icon_message_clicked)
        self.tray_icon.show()

        # Timer setup
        self.breathing_reminder_timer = Timer()
        self.breathing_reminder_timer.timeout_signal.connect(self.on_breathing_timer_timeout)

        # Window setup..
        # ..settings dialog
        # Important that the settings dialog is not initialized here (if we do we will get strange
        # issues at autostart on login)
        self.settings_dlg = None
        # ..breathing dialog
        self.br_dlg = matc.gui.breathing.BreathingGraphicsView()
        self.br_dlg.first_breathing_gi_signal.connect(self.on_first_breathing_gi)
        self.br_dlg.close_signal.connect(self.on_br_dlg_closed)

        matc.gui.modal_dialogs.UpdateAvailableDlg.check_if_update_available_and_start()

        if i_is_first_time_ever_started:
            matc.shared.do_extra_setup()
            matc.state.save_settings_to_json_file()
            """ - We save the settings just to have an indication that the application has been 
            started before. So that if the application crashes (for example a user turns off the 
            computer without exiting the application) the first time it's run, there is an 
            indication that the application has been started before, and therefore the intro 
            dialog/wizard is not shown
            """
            self.show_intro_dialog()
        else:
            self.open_br_dlg()

    def on_systray_activated(self, i_reason):
        """
        LXDE:
        XFCE: Bug: This function is not called
        macOS:
        Windows:
        """
        logging.debug("===== on_systray_activated =====")
        logging.debug(
            f"i_reason = {str(i_reason)} (0->Unknown, 1->Context, 2->DoubleClick, 3->Trigger, "
            f"4->MiddleClick) - more info: "
            f"https://doc.qt.io/qt-6/qsystemtrayicon.html#ActivationReason-enum")
        logging.debug("mouseButtons() = " + str(QtWidgets.QApplication.mouseButtons()))
        logging.debug("=====")
        """
        self.tray_icon.activated.emit(i_reason)
        if i_reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.restore_window()
        else:
            self.tray_icon.activated.emit(i_reason)
        """

    def show_intro_dialog(self):
        matc.gui.intro_dlg.IntroDlg.start()
        self.open_br_dlg()

    def open_br_dlg(self, i_new_phrase_id: int = SAME_PHRASE):
        if i_new_phrase_id != SAME_PHRASE:
            matc.state.active_phrase_id = i_new_phrase_id
        phrase = matc.state.get_breathing_phrase(matc.state.active_phrase_id)
        self.br_dlg.open_dlg(phrase)
        self._update_systray_image()
        self.breathing_reminder_timer.stop()

    def on_tray_br_phrase_triggered(self, i_action: QtGui.QAction):
        phrase_id_text = i_action.data()
        if phrase_id_text:
            self.open_br_dlg(i_new_phrase_id=int(phrase_id_text))

    def on_tray_quit_triggered(self):
        QtWidgets.QApplication.quit()

    def on_br_dlg_closed(self):
        br_timer_secs: int = matc.state.settings.get(matc.state.SK_BREATHING_BREAK_TIMER_SECS)
        self.breathing_reminder_timer.start(br_timer_secs)
        self._update_systray_image()

    def play_audio(self, i_audio_file_path: str, i_volume: int) -> None:
        try:
            sound_effect = QtMultimedia.QSoundEffect(self)
            # -Please note: A parent has to be given here, otherwise we will not hear anything
        except NameError:
            return
        master_volume: int = matc.state.settings[matc.state.SK_MASTER_VOLUME]
        audio_source_qurl = QtCore.QUrl.fromLocalFile(i_audio_file_path)
        sound_effect.setSource(audio_source_qurl)
        sound_effect.setVolume(float(i_volume / 100) * float(master_volume / 100))
        sound_effect.play()

    def on_tray_icon_message_clicked(self):
        """
        Works on: Windows 10
        Doesn't work on: XFCE
        https://forum.qt.io/topic/115121/qsystemtrayicon-not-sending-messageclicked-signal-on
        -linux/6
        """
        logging.debug("on_tray_icon_message_clicked")
        self.open_br_dlg()

    def on_breathing_timer_timeout(self):
        if self.br_dlg.isVisible():
            return
        if not self.tray_notifications_enabled_action.isChecked():
            return
        self._update_systray_image(i_is_breathing_reminder_shown=True)
        self.play_notif_audio()
        phrase = matc.state.get_breathing_phrase(matc.state.active_phrase_id)
        phrase_text: str = f"{phrase.in_breath}\n{phrase.out_breath}"

        notification_duration_msecs = matc.state.settings[matc.state.SK_NOTIFICATION_DURATION_MSECS]
        self.tray_icon.showMessage(matc.constants.APPLICATION_PRETTY_NAME,
            phrase_text, QtWidgets.QSystemTrayIcon.NoIcon, notification_duration_msecs)
        # -on Windows 10, where the tray icon may normally be hidden, it will be shown during the
        # time that the notification popup (message_title) is shown

    def play_notif_audio(self):
        notif_file_path: str = matc.state.settings[matc.state.SK_NOTIFICATION_AUDIO_FILE_PATH]
        notif_volume: int = matc.state.settings[matc.state.SK_NOTIFICATION_AUDIO_VOLUME]
        self.play_audio(notif_file_path, notif_volume)

    def on_systray_breathing_timeout(self):
        self._update_systray_image()

    def on_first_breathing_gi(self):
        self.play_br_audio()

    def play_br_audio(self):
        br_file_path: str = matc.state.settings[matc.state.SK_BREATHING_AUDIO_FILE_PATH]
        br_volume: int = matc.state.settings[matc.state.SK_BREATHING_AUDIO_VOLUME]
        self.play_audio(br_file_path, br_volume)

    def on_do_manual_gc_triggered(self):
        """
        About the Python GC: https://stackify.com/python-garbage-collection/ (see "Generational
        garbage collection")
        """
        import gc
        logging.debug(f"{gc.get_count()=}")
        logging.debug("Triggering manual garbage collection")
        gc.collect()
        logging.debug(f"{gc.get_count()=}")

    def on_raise_exception_triggered(self):
        raise Exception("Testing raising an exception")

    def on_disable_gc_triggered(self):
        import gc
        logging.debug(f"{gc.get_threshold()=}")
        logging.debug("Disabling the garbage collector by setting threshold to 0,0,0")
        gc.set_threshold(0, 0, 0)
        logging.debug(f"{gc.get_threshold()=}")

    def show_sysinfo_box(self):
        matc.gui.modal_dialogs.SysinfoDialog.start()

    def show_about_box(self):
        matc.gui.modal_dialogs.AboutDlg.start()

    def check_for_updates(self):
        update_available = matc.shared.is_update_available()
        if update_available:
            matc.gui.modal_dialogs.UpdateAvailableDlg.start()
        else:
            matc.gui.modal_dialogs.AlreadyLatestVersionDialog.start()

    def on_open_config_dir_triggered(self):
        config_path: str = matc.shared.get_config_path()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(config_path))

    def show_feedback_dialog(self):
        matc.gui.modal_dialogs.FeedbackDialog.start()

    def _update_systray_image(self, i_is_breathing_reminder_shown: bool = False):
        systray_icon_path = matc.shared.get_app_icon_path(i_is_breathing_reminder_shown)
        self.tray_icon.setIcon(QtGui.QIcon(systray_icon_path))

    def on_tray_menu_about_to_show(self):
        """
        Here we add the breathing phrases to the "phrases" sub-menu (attempting to add them directly
        to the base menu will make the menu too small, i.e. it will keep the size from before)
        """
        # self.rest_progress_qaction.setText("TBD - time since last rest")
        self.tray_br_phrases_qmenu.clear()
        phrases: list[matc.state.BreathingPhrase] = matc.state.settings[
            matc.state.SK_BREATHING_PHRASES]
        for p in phrases:
            phrase = matc.state.get_breathing_phrase(p.id)
            phrase_text: str = f"{phrase.in_breath}"
            bp_qaction = QtGui.QAction(phrase_text, parent=self.tray_br_phrases_qmenu)
            # -please note that we have to use the parent param (or the sub-menu will be empty)
            bp_qaction.setData(p.id)
            self.tray_br_phrases_qmenu.addAction(bp_qaction)

    def setup_settings_dlg(self):
        if self.settings_dlg is None:
            self.settings_dlg = matc.gui.settings_dlg.SettingsDlg()
            self.settings_dlg.br_timer_change_signal.connect(self.on_settings_br_timer_change)
            self.settings_dlg.notif_audio_test_signal.connect(self.play_notif_audio)
            self.settings_dlg.br_audio_test_signal.connect(self.play_br_audio)

    def on_tray_open_settings_triggered(self):
        self.setup_settings_dlg()
        self.settings_dlg.show()

    def on_tray_notifications_enabled_toggled(self, i_checked: bool):
        if i_checked:
            self.breathing_reminder_timer.start()
        else:
            self._update_systray_image()

    def on_settings_br_timer_change(self):
        br_noftif_time = matc.state.settings[matc.state.SK_BREATHING_BREAK_TIMER_SECS]
        self.breathing_reminder_timer.start(br_noftif_time)

    def on_tray_open_breathing_dialog_triggered(self):
        self.open_br_dlg()


class Timer(QtCore.QObject):
    timeout_signal = QtCore.Signal()

    def __init__(self, i_continuous: bool = True):
        super().__init__()
        # self.minutes_elapsed: int = 0
        self.timeout_secs = 0
        self.timer = None
        self.continuous: bool = i_continuous

    def stop(self):
        if self.timer and self.timer.isActive():
            self.timer.stop()
        # self.minutes_elapsed = 0

    def start(self, i_timeout_secs: int = 0):
        self.stop()
        if i_timeout_secs:
            self.timeout_secs = i_timeout_secs
        elif self.timeout_secs:
            pass
        else:
            raise Exception("timeout_secs error, not possible to have 0 for this value")
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timeout)
        self.timer.start(int(self.timeout_secs * 1000))

    def timeout(self):
        logging.debug("timeout")
        # self.minutes_elapsed += 1
        self.timeout_signal.emit()
        if not self.continuous:
            self.timer.stop()
