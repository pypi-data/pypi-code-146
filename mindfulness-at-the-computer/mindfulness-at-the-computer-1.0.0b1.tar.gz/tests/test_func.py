# import pytest
import random

import pytest
from PySide6 import QtCore

import matc.constants
import matc.gui
import matc.gui.breathing
import matc.gui.intro_dlg
import matc.gui.modal_dialogs
import matc.gui.settings_dlg
import matc.shared
import matc.state
from . import tshared

upper_left_pos = QtCore.QPoint(matc.gui.breathing.DLG_CORNER_RADIUS,
    matc.gui.breathing.DLG_CORNER_RADIUS)
lower_left_pos = QtCore.QPoint(matc.gui.breathing.DLG_CORNER_RADIUS,
    matc.gui.breathing.DLG_HEIGHT - matc.gui.breathing.DLG_CORNER_RADIUS)
middle_pos = QtCore.QPoint(matc.gui.breathing.DLG_WIDTH // 2, matc.gui.breathing.DLG_HEIGHT // 2)
middle_up_pos = QtCore.QPoint(
    matc.gui.breathing.DLG_WIDTH // 2, (matc.gui.breathing.DLG_HEIGHT // 2) - 5)
outside_pos = QtCore.QPoint(-100, matc.gui.breathing.DLG_HEIGHT // 2)


def delay_and_process_events(i_msecs: int):
    """
    Inspiration: https://stackoverflow.com/a/11487434/2525237

    Excluded alternatives:
    * At the time of writing QtTest.QTest doesn't have a qSleep function
    * Using Python's time.sleep() blocks execution
    """
    finish_time = QtCore.QTime.currentTime().addMSecs(i_msecs)
    while QtCore.QTime.currentTime() < finish_time:
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)


def move_process_compare(qtbot, i_widget, i_pos, i_time_secs: int, timer_func):
    delay_and_process_events(25)
    # -this is needed for the br_dlg mouse move event to be emitted
    # -(Specifically test_breathing_dlg_mouse_hover_line and test_breathing_dlg_mouse_hover_columns)
    time_msecs: int = 1000 * i_time_secs

    qtbot.mouseMove(i_widget, i_pos)
    delay_and_process_events(time_msecs // 2)

    # Shift the position slightly so that the mouse move event is triggered again
    # (This is used to test what happens when the mouse move event handler is entered a 2nd time)
    pos_2 = i_pos
    pos_2.setX(i_pos.x() + 1)
    qtbot.mouseMove(i_widget, pos_2)
    delay_and_process_events(time_msecs // 2)

    if timer_func is not None:
        assert 0.9 * time_msecs < timer_func() < 1.1 * time_msecs


def breathing_dlg_mouse_hover(qtbot, main_object):
    """
    Please note that it's difficult to test against 0 time for QTimeLine, since the time is not
    reset when the timer is stopped
    """
    br_dlg = main_object.br_dlg
    qtbot.addWidget(br_dlg)
    main_object.open_br_dlg()

    move_process_compare(qtbot, br_dlg, lower_left_pos, 1, None)
    for i in range(0, 2):
        move_process_compare(qtbot, br_dlg, middle_up_pos, 1, br_dlg.ib_qtimeline.currentTime)
        move_process_compare(qtbot, br_dlg, lower_left_pos, 1, br_dlg.ob_qtimeline.currentTime)
    move_process_compare(qtbot, br_dlg, outside_pos, 1, br_dlg.close_dialog_qtimeline.currentTime)


def press_process_compare(qtbot, i_widget, i_in_out: bool, i_time_secs: int, timer_func):
    delay_and_process_events(25)
    # -this is needed for the br_dlg mouse move event to be emitted
    # -(Specifically test_breathing_dlg_mouse_hover_line and test_breathing_dlg_mouse_hover_columns)
    time_msecs: int = 1000 * i_time_secs

    if i_in_out:
        qtbot.keyPress(i_widget, QtCore.Qt.Key.Key_Shift)  # ..mouseMove(i_widget, i_pos)
    else:
        qtbot.keyRelease(i_widget, QtCore.Qt.Key.Key_Shift)
    delay_and_process_events(time_msecs)

    if timer_func is not None:
        assert 0.9 * time_msecs < timer_func() < 1.1 * time_msecs


def breathing_dlg_keyboard(qtbot, main_object):
    """
    Please note that it's difficult to test against 0 time for QTimeLine, since the time is not
    reset when the timer is stopped
    """
    br_dlg = main_object.br_dlg
    qtbot.addWidget(br_dlg)
    main_object.open_br_dlg()

    press_process_compare(qtbot, br_dlg, False, 1, None)
    for i in range(0, 2):
        press_process_compare(qtbot, br_dlg, True, 1, br_dlg.ib_qtimeline.currentTime)
        press_process_compare(qtbot, br_dlg, False, 1, br_dlg.ob_qtimeline.currentTime)


class TestBrDlg:
    # TODO: Test close by clicking on br dlg

    @pytest.mark.slow
    def test_mouse_hover(self, qtbot, main_object, br_vis_param):
        matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION] = br_vis_param.value
        breathing_dlg_mouse_hover(qtbot, main_object)

    @pytest.mark.slow
    def test_keyboard(self, qtbot, main_object, br_vis_param):
        matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION] = br_vis_param.value
        breathing_dlg_keyboard(qtbot, main_object)

    @pytest.mark.slow
    def test_open_close_hover_br_dlg(self, qtbot, main_object, br_dlg, br_vis_param):
        matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION] = br_vis_param.value
        for i in range(0, 2):
            main_object.br_dlg.close_dlg()
            main_object.open_br_dlg()
            breathing_dlg_mouse_hover(qtbot, main_object)

    def test_open_close(self, qtbot, main_object):
        qtbot.addWidget(main_object.br_dlg)
        for i in range(0, 2):
            main_object.br_dlg.close_dlg()
            assert not main_object.br_dlg.isVisible()
            main_object.open_br_dlg()
            assert main_object.br_dlg.isVisible()
            # main_object.br_dlg.setFocus()
            main_object.br_dlg.close_dlg()
            # -cannot use qtbot.mousePress, it gives an error that i've been unable to track
            assert not main_object.br_dlg.isVisible()

    def test_open_close_press_enter_br_dlg(self, qtbot, main_object, br_dlg, br_vis_param):
        pass


def test_reminder_timeout(qtbot, main_object):
    systray_qsti: QtWidgets.QSystemTrayIcon = main_object.tray_icon
    matc.state.settings[matc.state.SK_BREATHING_BREAK_TIMER_SECS] = 1

    # standard case
    main_object.br_dlg.close_dlg()
    assert tshared.compare_icons(systray_qsti.icon(), False)
    delay_and_process_events(1500)
    assert tshared.compare_icons(systray_qsti.icon(), True)

    # br dlg visible when time out happens
    main_object.open_br_dlg()
    assert tshared.compare_icons(systray_qsti.icon(), False)
    delay_and_process_events(1500)
    assert tshared.compare_icons(systray_qsti.icon(), False)

    # notifications disabled
    main_object.br_dlg.close_dlg()
    main_object.tray_notifications_enabled_action.setChecked(False)
    assert tshared.compare_icons(systray_qsti.icon(), False)
    delay_and_process_events(1500)
    assert tshared.compare_icons(systray_qsti.icon(), False)


@pytest.mark.slow
def test_stress(qtbot, main_object, settings_dlg, br_dlg):
    for i in range(0, 2):
        br_vis_value = random.choice([b.value for b in matc.shared.BrVis])
        matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION] = br_vis_value
        main_object.br_dlg.close_dlg()
        delay_and_process_events(500)
        main_object.open_br_dlg()
        breathing_dlg_mouse_hover(qtbot, main_object)

        main_object.tray_open_settings_action.trigger()
        delay_and_process_events(1000)
        settings_dlg.close()
        delay_and_process_events(500)
