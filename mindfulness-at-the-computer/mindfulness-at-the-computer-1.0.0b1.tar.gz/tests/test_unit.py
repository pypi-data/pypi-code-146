import logging
import webbrowser

import pytest
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import matc.constants
import matc.gui
import matc.gui.breathing
import matc.gui.intro_dlg
import matc.gui.modal_dialogs
import matc.gui.settings_dlg
import matc.shared
import matc.state
from . import tshared


class TestModel:
    # state.py

    def test_data_phrases(self, qtbot):
        br_phrase_list = matc.state.settings[matc.state.SK_BREATHING_PHRASES]
        for br_phrase in br_phrase_list:
            br_phrase: matc.state.BreathingPhrase
            if "Breathing in" in br_phrase.in_breath:
                return
        pytest.fail()

    @pytest.mark.pycharm_auto
    def test_load_faulty_json_from_file(self, qtbot, monkeypatch):
        monkeypatch.setattr(matc.gui.modal_dialogs.ErrorDlg,
            "log_and_start", classmethod(lambda *args: None))

        invalid_json = '{key_without_citation_marks:"value"}'
        with open(matc.state.settings_file_path, 'w+') as file:
            file.write(invalid_json)
        old_length = len(matc.state.settings)
        matc.state._initiate_settings_dict()
        assert old_length != 0
        assert old_length == len(matc.state.settings)

    def test_load_correct_json_from_file(self, qtbot):
        valid_json = '{"key":"value"}'
        with open(matc.state.settings_file_path, 'w+') as file:
            contents = file.write(valid_json)
        old_length = len(matc.state.settings)
        matc.state._initiate_settings_dict()
        assert old_length != 0
        assert old_length + 1 == len(matc.state.settings)

    def test_reading_existing_json(self, qtbot, main_object):
        matc.state._initiate_settings_dict()
        matc.state.save_settings_to_json_file()
        matc.state._initiate_settings_dict()
        assert len(matc.state.settings[matc.state.SK_BREATHING_PHRASES]) > 0


class TestTimer:
    SIGNAL_TIMEOUT = "process timed-out"

    def test_timer_fired(self, qtbot, main_object):
        timer = matc.main_object.Timer(i_continuous=False)
        with qtbot.wait_signal(timer.timeout_signal, timeout=1200):
            timer.start(1)

    def test_timer_timeout(self, qtbot, main_object):
        timer = matc.main_object.Timer(i_continuous=False)
        with qtbot.wait_signal(timer.timeout_signal, timeout=800, raising=False) as blocker:
            timer.start(1)
        assert blocker.signal_triggered != self.SIGNAL_TIMEOUT


class TestSettingsDlg:
    def test_change_auto_move_cursor(self, qtbot, settings_dlg):
        assert settings_dlg.auto_move_mouse_cursor_qcb.isChecked()
        # qtbot.mouseClick(settings_dlg.auto_move_mouse_cursor_qcb, QtCore.Qt.LeftButton)
        settings_dlg.auto_move_mouse_cursor_qcb.click()
        assert not settings_dlg.auto_move_mouse_cursor_qcb.isChecked()
        assert not matc.state.settings[matc.state.SK_MOVE_MOUSE_CURSOR]

    def test_change_br_vis(self, qtbot, settings_dlg, br_vis_param):
        qrb = settings_dlg.bv_group_qbg.button(br_vis_param.value)
        qrb.click()
        vis_nr = matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION]
        assert vis_nr == br_vis_param.value
        assert qrb.isChecked()

    def test_toggle_auto_move(self, qtbot, settings_dlg):
        assert settings_dlg.auto_move_mouse_cursor_qcb.isChecked()
        assert matc.state.settings[matc.state.SK_MOVE_MOUSE_CURSOR]
        settings_dlg.auto_move_mouse_cursor_qcb.click()
        assert not settings_dlg.auto_move_mouse_cursor_qcb.isChecked()
        assert not matc.state.settings[matc.state.SK_MOVE_MOUSE_CURSOR]

    @pytest.mark.pycharm_auto
    def test_change_volume(self, qtbot, settings_dlg):
        original_value = matc.state.MASTER_VOLUME_DEFAULT
        new_value = 42
        assert settings_dlg.volume_qsr.value() == original_value
        assert matc.state.settings[matc.state.SK_MASTER_VOLUME] == original_value
        settings_dlg.volume_qsr.setValue(new_value)
        assert settings_dlg.volume_qsr.value() == new_value
        assert matc.state.settings[matc.state.SK_MASTER_VOLUME] == new_value

    def test_br_vis_id_clicked(self, qtbot, settings_dlg):
        original_value = matc.state.BREATHING_VISUALIZATION_DEFAULT
        new_value = matc.shared.BrVis.circle.value
        assert original_value != new_value

        assert settings_dlg.bv_group_qbg.checkedId() == original_value
        assert matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION] == original_value
        settings_dlg.circle_bv_option_cw.qrb.click()
        assert settings_dlg.bv_group_qbg.checkedId() == new_value
        assert matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION] == new_value

    def test_br_timer_changed(self, qtbot, settings_dlg):
        """Unforunately there is no way to access the modal dialog and change the texts"""
        SECS_PER_MIN = 60

        old_value_frontend = settings_dlg.breathing_break_time_qsb.value()
        old_value_backend = matc.state.settings[matc.state.SK_BREATHING_BREAK_TIMER_SECS]
        assert old_value_frontend * SECS_PER_MIN == old_value_backend

        new_value_frontend_to_set = 42
        assert new_value_frontend_to_set != old_value_frontend
        settings_dlg.breathing_break_time_qsb.setValue(new_value_frontend_to_set)

        new_value_frontend = settings_dlg.breathing_break_time_qsb.value()
        assert new_value_frontend == new_value_frontend_to_set

        new_value_backend = matc.state.settings[matc.state.SK_BREATHING_BREAK_TIMER_SECS]
        assert new_value_frontend * SECS_PER_MIN == new_value_backend


class TestSettingsPhraseList:

    def test_phrases_list_drop_item(self, qtbot, settings_dlg):
        brp_list_before = matc.state.settings[matc.state.SK_BREATHING_PHRASES]

        take_pos, drop_pos = 3, 1
        qlwi = settings_dlg.breathing_phrases_qlw.takeItem(take_pos)
        settings_dlg.breathing_phrases_qlw.insertItem(drop_pos, qlwi)

        settings_dlg.on_bp_item_dropped()  # -this will update the settings data

        brp_list_after = matc.state.settings[matc.state.SK_BREATHING_PHRASES]
        assert brp_list_before != brp_list_after
        assert qlwi.data(QtCore.Qt.UserRole) == 4
        # -the value in the position 3 is 4, since we start at 0
        assert qlwi.data(QtCore.Qt.UserRole) == brp_list_after[drop_pos].id

    def test_add_bp_clicked(self, qtbot, settings_dlg, monkeypatch):
        old_count = settings_dlg.breathing_phrases_qlw.count()
        monkeypatch.setattr(matc.gui.settings_dlg.BreathingPhraseEditDialog, "start",
            lambda *args: True)
        settings_dlg.add_bp_qpb.click()
        new_count = settings_dlg.breathing_phrases_qlw.count()
        assert new_count == old_count + 1

    def test_add_bp_clicked_cancelled(self, qtbot, settings_dlg, monkeypatch):
        old_count = settings_dlg.breathing_phrases_qlw.count()
        monkeypatch.setattr(matc.gui.settings_dlg.BreathingPhraseEditDialog, "start",
            lambda *args: False)
        settings_dlg.add_bp_qpb.click()
        new_count = settings_dlg.breathing_phrases_qlw.count()
        assert new_count == old_count

    def test_del_bp_clicked(self, qtbot, settings_dlg, monkeypatch):
        old_count = settings_dlg.breathing_phrases_qlw.count()
        monkeypatch.setattr(QtWidgets.QMessageBox, "question",
            lambda *args: QtWidgets.QMessageBox.Yes)
        settings_dlg.del_bp_qpb.click()
        new_count = settings_dlg.breathing_phrases_qlw.count()
        assert new_count == old_count - 1

    def test_edit_bp_clicked(self, qtbot, settings_dlg, monkeypatch):
        """Unforunately there is no way to access the modal dialog and change the texts"""
        old_count = settings_dlg.breathing_phrases_qlw.count()
        monkeypatch.setattr(matc.gui.settings_dlg.BreathingPhraseEditDialog, "start",
            lambda *args: True)
        settings_dlg.edit_bp_qpb.click()
        new_count = settings_dlg.breathing_phrases_qlw.count()
        assert new_count == old_count

    def test_br_phrase_edit_dlg_internal(self, qtbot, main_object, settings_dlg):
        brp_test_id = 1
        brp = matc.state.get_breathing_phrase(brp_test_id)
        brp_edit_dlg = matc.gui.settings_dlg.BreathingPhraseEditDialog(brp_test_id)
        assert brp_edit_dlg.in_breath_phrase_qle.text() == brp.in_breath

        new_ib_phrase_text = "test"
        brp_edit_dlg.in_breath_phrase_qle.setText(new_ib_phrase_text)
        assert brp_edit_dlg.in_breath_phrase_qle.text() == new_ib_phrase_text


@pytest.mark.skip(tshared.MANUAL_TEST_CASE_NOT_YET_COMPLETE)
def test_application_opens_on_restart():
    """
    This has been a problem previously. See issue
    https://gitlab.com/mindfulness-at-the-computer/mindfulness-at-the-computer/-/issues/428
    """


@pytest.mark.skip(tshared.MANUAL_TEST_CASE_NOT_YET_COMPLETE)
def test_dark_mode_from_os():
    """
    Does this work at all???????????????????
    1. Go to the OS settings
    2. select dark mode
    3. open the application settings
    4. verify that a dark background is used
    5. open the info dialog from the systray menu
    6. verify that a dark background is used
    """


class TestBreathingDlg:
    def test_breathing_dlg(self, qtbot, main_object, br_dlg, br_vis_param):
        br_dlg.close_dlg()
        assert not br_dlg.isVisible()
        main_object.open_br_dlg()
        assert br_dlg.isVisible()

        assert br_dlg.breathing_state == matc.gui.breathing.BrState.inactive
        br_dlg.start_breathing_in()
        assert br_dlg.breathing_state == matc.gui.breathing.BrState.breathing_in
        br_dlg.start_breathing_out()
        assert br_dlg.breathing_state == matc.gui.breathing.BrState.breathing_out
        br_dlg.start_breathing_in()
        assert br_dlg.breathing_state == matc.gui.breathing.BrState.breathing_in


class TestIntroDlg:
    def test_intro_dlg(self, qtbot, main_object):
        """
        Difficult to test visibility since the intro dialog uses .exec() (rather than .show()) to
        start
        """
        intro_dlg = matc.gui.intro_dlg.IntroDlg()
        stack_count = intro_dlg.wizard_qsw_w3.count()
        stack_range = range(stack_count)
        logging.debug(f"{stack_range=}")
        assert intro_dlg.wizard_qsw_w3.currentIndex() == 0
        for i in stack_range[:-1]:
            qtbot.mouseClick(intro_dlg.next_qpb, QtCore.Qt.LeftButton)
            assert intro_dlg.wizard_qsw_w3.currentIndex() == i + 1
        for i in list(reversed(stack_range))[:-1]:
            qtbot.mouseClick(intro_dlg.prev_qpb, QtCore.Qt.LeftButton)
            assert intro_dlg.wizard_qsw_w3.currentIndex() == i - 1
        for i in stack_range[:-1]:
            assert intro_dlg.next_qpb.text() == matc.gui.intro_dlg.NEXT
            qtbot.mouseClick(intro_dlg.next_qpb, QtCore.Qt.LeftButton)
            logging.debug(f"{i=}")
        assert intro_dlg.next_qpb.text() == matc.gui.intro_dlg.FINISH
        with qtbot.wait_signal(intro_dlg.close_signal, timeout=100, raising=False) as blocker:
            qtbot.mouseClick(intro_dlg.next_qpb, QtCore.Qt.LeftButton)


def test_save_on_settings_dlg_closed(qtbot, main_object, settings_dlg):
    with open(matc.state.settings_file_path, 'r') as file:
        old_file_contents: str = file.read()
    with open(matc.state.settings_file_path, 'r') as file:
        new_file_contents: str = file.read()
    assert old_file_contents == new_file_contents

    settings_dlg.auto_move_mouse_cursor_qcb.click()
    settings_dlg.close()

    with open(matc.state.settings_file_path, 'r') as file:
        new_file_contents: str = file.read()
    assert old_file_contents != new_file_contents


class TestSystray:
    def test_open_settings_dlg_from_systray_menu(qtbot, main_object, settings_dlg):
        assert not settings_dlg.isVisible()
        main_object.on_tray_open_settings_triggered()
        assert settings_dlg.isVisible()

    def test_systray_menu_open_settings_dlg(self, qtbot, main_object, settings_dlg):
        systray_menu = main_object.tray_menu
        tray_menu_action_list = systray_menu.actions()
        # print(f"{action_list=}")
        # assert main_object.tray_open_breathing_dialog_qaction in tray_menu_action_list
        assert main_object.tray_open_settings_action in tray_menu_action_list

        assert not settings_dlg.isVisible()
        main_object.tray_open_settings_action.trigger()
        assert settings_dlg.isVisible()

    def test_systray_help_submenu(self, qtbot, main_object, monkeypatch):
        # Safer way to do this: https://stackoverflow.com/questions/53771621/python-context-manager
        # -to-restore-a-variables-value

        help_menu = main_object.help_menu
        help_menu_action_list = help_menu.actions()
        # print(f"{action_list=}")
        # assert main_object.tray_open_breathing_dialog_qaction in tray_menu_action_list
        assert main_object.show_intro_dialog_action in help_menu_action_list
        assert main_object.feedback_action in help_menu_action_list
        assert main_object.sysinfo_action in help_menu_action_list
        assert main_object.about_action in help_menu_action_list
        assert main_object.check_for_update_action in help_menu_action_list

        start_calls = []

        monkeypatch.setattr(matc.gui.intro_dlg.IntroDlg, "start", lambda: start_calls.append(1))
        main_object.show_intro_dialog_action.trigger()
        main_object.br_dlg.close_dlg()

        monkeypatch.setattr(matc.gui.modal_dialogs.FeedbackDialog, "start",
            lambda: start_calls.append(2))
        main_object.feedback_action.trigger()

        monkeypatch.setattr(matc.gui.modal_dialogs.SysinfoDialog, "start",
            lambda: start_calls.append(3))
        main_object.sysinfo_action.trigger()

        monkeypatch.setattr(matc.gui.modal_dialogs.AboutDlg, "start", lambda: start_calls.append(4))
        main_object.about_action.trigger()

        assert start_calls == [1, 2, 3, 4]

        """
            update_available = matc.shared.is_update_available()
        if update_available:
            matc.gui.modal_dialogs.UpdateAvailableDlg.start()
        else:
            matc.gui.modal_dialogs.AlreadyLatestVersionDialog.start()
        """

    @pytest.mark.skip(
        "Skipped until we have set the latest version in the gitlab site version file")
    def test_systray_help_submenu_check_for_updates(self, main_object, monkeypatch):
        monkeypatch.setattr(matc.gui.modal_dialogs.AlreadyLatestVersionDialog, "start",
            lambda: start_calls.append(5))
        main_object.check_for_update_action.trigger()

        monkeypatch.setattr(matc.gui.modal_dialogs.UpdateAvailableDlg, "start",
            lambda: start_calls.append(6))

        monkeypatch.setattr(matc.shared, "get_version", lambda: "100.999.000")
        main_object.check_for_update_action.trigger()

        assert start_calls == [5, 6]

    def test_systray_menu_notifications_enabled(self, qtbot, main_object):
        systray_menu = main_object.tray_menu
        tray_menu_action_list = systray_menu.actions()
        assert main_object.tray_notifications_enabled_action in tray_menu_action_list

        assert main_object.tray_notifications_enabled_action.isChecked()

        main_object.tray_notifications_enabled_action.toggle()
        assert not main_object.tray_notifications_enabled_action.isChecked()
        assert not main_object.breathing_reminder_timer.timer.isActive()

        main_object.tray_notifications_enabled_action.toggle()
        assert main_object.tray_notifications_enabled_action.isChecked()
        assert main_object.breathing_reminder_timer.timer.isActive()

    def test_systray_menu_open_br_dlg(self, qtbot, main_object):
        systray_menu = main_object.tray_menu
        tray_menu_action_list = systray_menu.actions()
        assert main_object.tray_open_breathing_dialog_qaction in tray_menu_action_list
        main_object.br_dlg.close_dlg()
        assert not main_object.br_dlg.isVisible()
        main_object.tray_open_breathing_dialog_qaction.trigger()
        assert main_object.br_dlg.isVisible()

    def test_systray_menu_quit_application(self, qtbot, main_object, monkeypatch):
        """
        Inspiration:
        https://pytest-qt.readthedocs.io/en/latest/qapplication.html#testing-qapplication-exit

        """
        appl_exit_calls = []
        monkeypatch.setattr(QtGui.QGuiApplication, "quit", lambda: appl_exit_calls.append(1))
        systray_menu = main_object.tray_menu
        tray_menu_action_list = systray_menu.actions()
        assert main_object.tray_quit_action in tray_menu_action_list

        main_object.tray_quit_action.trigger()

        assert appl_exit_calls == [1]

    def test_phrases_menu_actions(self, qtbot, main_object):
        main_object.on_tray_menu_about_to_show()
        phrases_menu = main_object.tray_br_phrases_qmenu
        phrases_menu_action_list = phrases_menu.actions()
        phrases_from_backend_list = matc.state.settings[matc.state.SK_BREATHING_PHRASES]
        assert len(phrases_menu_action_list) == len(phrases_from_backend_list)
        assert len(phrases_menu_action_list) != 0

        for phrases_menu_action in phrases_menu_action_list:
            main_object.br_dlg.close_dlg()
            assert not main_object.br_dlg.isVisible()
            phrases_menu_action.trigger()
            assert main_object.br_dlg.isVisible()
            id_ = int(phrases_menu_action.data())
            assert id_ in [p.id for p in phrases_from_backend_list]
            bp = matc.state.get_breathing_phrase(id_)
            breathing_phrase_combo_text = main_object.br_dlg.br_text_gi.toPlainText()
            assert bp.in_breath in breathing_phrase_combo_text
            assert bp.out_breath in breathing_phrase_combo_text

    def test_systray_menu_open_phrases_menu(self, qtbot, main_object):
        phrases_menu = main_object.tray_br_phrases_qmenu

        main_object.on_tray_menu_about_to_show()
        old_phrases_menu_action_list = phrases_menu.actions()
        old_phrases_count = len(old_phrases_menu_action_list)

        brp_to_remove_id = 1
        matc.state.remove_breathing_phrase(brp_to_remove_id)

        # systray_menu.show()
        main_object.on_tray_menu_about_to_show()
        new_phrases_menu_action_list = phrases_menu.actions()
        new_phrases_count = len(new_phrases_menu_action_list)

        assert old_phrases_count == new_phrases_count + 1

    @pytest.mark.skip("")
    def test_help_menu(self, qtbot, main_object):
        help_menu = main_object.help_menu
        help_menu_action_list = help_menu.actions()
        for help_menu_action in help_menu_action_list:
            help_menu_action.trigger()


class TestVariousDialogs:
    def test_br_dlg_appl_started_before(self, qtbot, main_object_started_before):
        # TODO: Use this instead? https://docs.pytest.org/en/latest/how-to/parametrize.html
        assert main_object_started_before.br_dlg.isVisible()
        # main_object_started_before.br_dlg.close_dlg()

    def test_about_dlg(self, qtbot, main_object):
        """
        We don't run dlg.exec() since that would stop execution
        """
        dlg = matc.gui.modal_dialogs.AboutDlg()
        dlg.show()  # -not needed, but may be good to test
        assert "Tord" in dlg.info_qll.text()
        assert "asdf" not in dlg.info_qll.text()
        assert "About" in dlg.windowTitle()
        # main_object.show_about_box()

    def test_sysinfo_dlg(self, qtbot, main_object):
        appl_version = matc.shared.get_version()
        dlg = matc.gui.modal_dialogs.SysinfoDialog()
        # dlg.show()
        sysinfo_text = dlg.system_info_pqte.toPlainText()
        assert appl_version in sysinfo_text
        assert "asdf" not in sysinfo_text

        qclipboard = QtGui.QGuiApplication.clipboard()
        cb_text = qclipboard.text()
        assert appl_version not in cb_text
        qtbot.mouseClick(dlg.copy_qpb, QtCore.Qt.LeftButton)
        cb_text = qclipboard.text()
        assert appl_version in cb_text

    def test_feedback_dlg(self, qtbot, main_object, monkeypatch):
        dlg = matc.gui.modal_dialogs.FeedbackDialog()
        dlg.show()
        assert dlg.isVisible()
        assert "mail" in dlg.help_request_qll.text()
        assert "asdf" not in dlg.help_request_qll.text()

        assert dlg.isVisible()
        close_button_qpb = tshared.get_close_button_from_button_box(dlg.button_box)
        qtbot.addWidget(close_button_qpb)
        qtbot.mouseClick(close_button_qpb, QtCore.Qt.LeftButton)
        assert not dlg.isVisible()

        monkeypatch.setattr(webbrowser, "open", lambda url_string: None)
        # webbrowser.open(url_string)
        dlg.emailus_qpb.click()

        # TODO: MANUAL testing needed, checking that "email us" works

    def test_update_available_dlg(self, qtbot, main_object):
        dlg = matc.gui.modal_dialogs.UpdateAvailableDlg()

    def test_already_latest_version_dlg(self, qtbot, main_object):
        dlg = matc.gui.modal_dialogs.AlreadyLatestVersionDialog()

    def test_error_dlg(self, qtbot, main_object):
        dlg = matc.gui.modal_dialogs.ErrorDlg("Title", "Extra info")
        # dlg.copy_qpb
        # dlg.open_log_file_qpb
        # dlg.report_qpb


def test_systray_icon_notification(qtbot, main_object):
    # TODO: Perhaps use this approach https://stackoverflow.com/a/42156088/2525237
    # and move this function back into unit_test.py
    systray_qsti: QtWidgets.QSystemTrayIcon = main_object.tray_icon
    assert tshared.compare_icons(systray_qsti.icon(), False)
    main_object.br_dlg.close_dlg()
    main_object.on_breathing_timer_timeout()
    assert tshared.compare_icons(systray_qsti.icon(), True)


@pytest.mark.skip("")
def test_main_obj_audio(qtbot, main_object):
    pass
