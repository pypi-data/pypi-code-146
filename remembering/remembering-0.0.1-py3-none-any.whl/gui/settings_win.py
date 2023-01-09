import functools
import logging
import sys

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import remembering.gui.details_cw
import remembering.gui.launch_actions
import remembering.model_old
import remembering.rg_global
import remembering.timer

# TODO: link to videos about anxiety
# Examples: Yongey Mingyur Rinpoche - https://youtu.be/pJs9Y2eqLuE


MAX_NR_OF_SYSTRAY_NOTIFICATIONS_INT = 9
MAX_NR_OF_SYSTRAY_PERMANENT_INT = 9


class SettingsWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(40, 32, 900, 700)
        self.setWindowTitle("Notifications - Settings")

        # Widget setup
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        hbox_l2 = QtWidgets.QHBoxLayout()
        central_widget.setLayout(hbox_l2)

        self.rememberances_list_cw = ListCw()
        self.rememberances_list_cw.list_updated_signal.connect(self.on_list_updated)
        hbox_l2.addWidget(self.rememberances_list_cw)

        """        
        self.rememberances_list_qlw = QtWidgets.QListWidget()
        self.rememberances_list_qlw.currentRowChanged.connect(self.on_rememberances_list_rowchanged)
        hbox_l2.addWidget(self.rememberances_list_qlw)
        """

        self.details_qsw = QtWidgets.QStackedWidget()

        self.details_empty_qll = QtWidgets.QLabel(
            "Please select a remembrance from the list to the left by clicking on the title of "
            "one of the rows")
        self.details_empty_qll.setWordWrap(True)
        self.details_empty_id_int = self.details_qsw.addWidget(self.details_empty_qll)

        self.details_cw = remembering.gui.details_cw.DetailsCw(
            remembering.model_old.RememberItem.get_max_id())  # TODO: Fix id
        self.details_cw.update_signal.connect(self.on_details_updated)
        self.details_used_id_int = self.details_qsw.addWidget(self.details_cw)

        # update_gui

        hbox_l2.addWidget(self.details_qsw)

        # Tray
        pixmap = QtGui.QPixmap("icons/0.png")
        self.tray_icon = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(pixmap),
            self
        )
        self.tray_icon.show()

        self.tray_menu = QtWidgets.QMenu(self)
        self.tray_settings_action = None
        self.tray_quit_action = None
        self.dynamic_qaction_list = []
        # -Please note: We don't read from this list ourselves, but still need to store menu
        # entries here
        #  (which are not stored elsewhere, like the exit and settings actions) so that they are
        #  held in memory
        self.tray_icon.setContextMenu(self.tray_menu)

        # Creating the menu bar..
        # ..setup of actions
        export_qaction = QtGui.QAction("Export", self)
        export_qaction.triggered.connect(remembering.model_old.export_all)
        exit_qaction = QtGui.QAction("Exit", self)
        exit_qaction.triggered.connect(QtWidgets.QApplication.quit)
        backup_qaction = QtGui.QAction("Backup", self)
        backup_qaction.triggered.connect(remembering.model_old.backup_db_file)

        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("&File")
        file_menu.addAction(export_qaction)
        file_menu.addAction(backup_qaction)
        file_menu.addAction(exit_qaction)

        # Timer
        self.timer = remembering.timer.Timer()
        self.timer.update_signal.connect(self.on_timer_signal_activated)
        self.timer.start()

        # Show and update
        self.show()
        self.update_gui()

    """
    # overridden
    def closeEvent(self, QCloseEvent):
        logging.info("SettingsWin - closeEvent")
        # PLASE NOTE: The aboutToQuit signal is used for QApplication (see remembering.py)
        ######rg.model_old.backup_db_file()
    """

    def on_details_updated(self, i_id: int):
        self.update_gui(i_id)

    def on_settings_triggered(self):
        self.showNormal()
        self.raise_()

    def update_systray(self):
        # Systray notifications, "active notifications"
        number_of_active_notifications_int = \
            remembering.model_old.RememberItem.get_nr_of_fired_notifications()
        if number_of_active_notifications_int <= 8:
            file_name_str = "icons/" + str(number_of_active_notifications_int) + ".png"
        else:
            file_name_str = "icons/9+.png"
        pixmap = QtGui.QPixmap(file_name_str)
        self.tray_icon.setIcon(QtGui.QIcon(pixmap))

        # clearing
        self.tray_menu.clear()
        self.dynamic_qaction_list.clear()
        """
        if self.tray_restore_action is not None:
            self.tray_menu.removeAction(self.tray_restore_action)
        if self.tray_quit_action is not None:
            self.tray_menu.removeAction(self.tray_quit_action)
        for i in range(0, MAX_NR_OF_SYSTRAY_NOTIFICATIONS_INT):
            if i < len(self.dynamic_qaction_list):
                self.tray_menu.removeAction(self.dynamic_qaction_list[i])
            else:
                break
        self.dynamic_qaction_list.clear()
        """

        # Collectiong data for both dyn and stat
        t_fired_notification_id_list = []
        t_permanent_id_list = []
        # Popup notifications, "new notifications"
        for remembrance_item in remembering.model_old.Remembrances.get_all():
            if remembrance_item.notif_fired_bool:
                t_fired_notification_id_list.append(remembrance_item.id_int)
            elif remembrance_item.permanent_bool:
                if remembrance_item.notif_active_bool:
                    t_permanent_id_list.append(remembrance_item.id_int)

        # Dynamic..
        # ..rebuilding
        count_int = 0
        for i in range(0, MAX_NR_OF_SYSTRAY_NOTIFICATIONS_INT):
            if len(t_fired_notification_id_list) == 0:
                break
            else:
                t_fired_notification_int_id = t_fired_notification_id_list.pop()
                remembrance = remembering.model_old.RememberItem.get_item(
                    t_fired_notification_int_id)

                t_tray_dynamic_qaction = QtGui.QAction(remembrance.title_str)
                self.tray_menu.addAction(t_tray_dynamic_qaction)
                t_tray_dynamic_qaction.triggered.connect(
                    functools.partial(
                        self.on_systray_qaction_triggered,
                        t_fired_notification_int_id)
                )
                self.dynamic_qaction_list.append(t_tray_dynamic_qaction)
            count_int += 1
        if count_int >= 1:
            self.tray_menu.addSeparator()

        # Static
        count_int = 0
        for i in range(0, MAX_NR_OF_SYSTRAY_PERMANENT_INT):
            if len(t_permanent_id_list) == 0:
                break
            else:
                t_permanent_int_id = t_permanent_id_list.pop()
                remembrance = remembering.model_old.RememberItem.get_item(t_permanent_int_id)
                time_since_last_activated_str = remembering.rg_global.get_time_diff_string(
                    remembrance.last_activated_ts_int,
                    QtCore.QDateTime.currentSecsSinceEpoch()
                )
                t_title_with_time_str = remembrance.title_str + " (" + \
                                        time_since_last_activated_str + ")"
                t_tray_dynamic_qaction = QtGui.QAction(t_title_with_time_str)
                self.tray_menu.addAction(t_tray_dynamic_qaction)
                t_tray_dynamic_qaction.triggered.connect(
                    functools.partial(
                        self.on_systray_qaction_triggered,
                        t_permanent_int_id)
                )
                self.dynamic_qaction_list.append(t_tray_dynamic_qaction)
            count_int += 1
        if count_int >= 1:
            self.tray_menu.addSeparator()

        """
        self.tray_settings_action = QtGui.QAction("Settings")
        self.tray_settings_action.triggered.connect(self.on_settings_triggered)
        self.tray_menu.addAction(self.tray_settings_action)
        """
        self.tray_settings_action = QtGui.QAction("Settings")
        self.tray_settings_action.triggered.connect(self.on_settings_triggered)
        self.tray_menu.addAction(self.tray_settings_action)
        self.tray_quit_action = QtGui.QAction("Quit")
        self.tray_quit_action.triggered.connect(sys.exit)
        self.tray_menu.addAction(self.tray_quit_action)

    def on_list_updated(self, i_new_item_added: bool):
        self.update_gui()
        if i_new_item_added:
            self.details_cw.title_qle.setFocus()

    def on_systray_message_clicked(self):
        logging.debug("on_systray_message_clicked")
        # -doesnt seem to work on LXDE. Documentation says it doesn't work on MacOS

    def on_timer_signal_activated(self, i_new_notifications_id_list: list, i_missed: bool):
        """
        Important function!
        """
        # Popup notifications, "new notifications"
        for id_int in i_new_notifications_id_list:
            title_str = "Remembering"
            remembrance = remembering.model_old.RememberItem.get_item(id_int)
            message_str = remembrance.title_str
            if i_missed:
                message_str += " [missed]"
            # pixmap = QtGui.QPixmap("DSC_1033.JPG")
            # self.tray_icon.showMessage(title_str, message_str, QtGui.QIcon(pixmap))
            self.tray_icon.showMessage(title_str, message_str)
            # check the number of notifications

        self.update_gui()

        """
        self.tray_notification_action = QtGui.QAction(title_str)
        # self.tray_quit_action.triggered.connect(sys.exit)
        self.tray_menu.addAction(self.tray_notification_action)
        dynamic_qaction = self.dynamic_qaction_list[count_int]
        dynamic_qaction.setText(remembrance.title_str)
        """

    def on_systray_qaction_triggered(self, i_id: int):
        # rg.model.Remembrances.update_notif_fired(i_id, False)
        # -doing this first since the following code is blocking

        remembering.gui.launch_actions.launch_action(i_id, False)
        self.update_gui()

    def update_gui(self, i_id: int = -1):
        self.rememberances_list_cw.update_gui(i_id)
        # TODO: selecting the topmost item

        # update the details area?
        # as it looks now this is probably not needed
        if remembering.rg_global.current_item_id_int == remembering.rg_global.NO_VALUE_SET_INT:
            self.details_qsw.setCurrentIndex(self.details_empty_id_int)
        else:
            self.details_qsw.setCurrentIndex(self.details_used_id_int)
            self.details_cw.update_gui()

        # Updating the system tray
        self.update_systray()

        """
        self.rememberances_list_qlw.clear()
        # title_list = [(key_str, item.title_str) for (key_str, item) in 
        rg.model.Rememberances.get_items()]
        count_int = 0
        for (key_str, item) in rg.model.Rememberances.get_items():
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(item.title_str)
            list_item.setData(QtWidgets.QListWidgetItem.UserType, key_str)
            count_int += 1
            self.rememberances_list_qlw.addItem(list_item)
        """

        # self.details_cw.update_gui()


def resize_image_fullscreen(self):
    if self.image_cqll.pixmap() is None:
        return
    image_width_int = self.image_cqll.pixmap().width()
    image_height_int = self.image_cqll.pixmap().height()
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
    self.image_cqll.setFixedWidth(scaled_image_width_int - 20)
    self.image_cqll.setFixedHeight(scaled_image_height_int - 20)
    # -can resize be used instead? there seems to be some difference in how it works


class ListCw(QtWidgets.QWidget):
    list_updated_signal = QtCore.Signal(bool)  # -bool is for if the item is new

    def __init__(self):
        super().__init__()

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox_l2)

        """
        self.preset_qcb = QtWidgets.QComboBox()
        self.preset_qcb.addItems([
            "active preset 1", "2", "3"
        ])
        self.vbox_l2.addWidget(self.preset_qcb)
        """

        self.scroll_area_w3 = QtWidgets.QScrollArea()
        # self.scroll_area_w3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_w3.setWidgetResizable(True)
        self.scroll_list_w4 = QtWidgets.QWidget()
        self.scroll_list_w4.setObjectName("MY_WIDGET_NAME_STR")
        self.scroll_list_vbox_l5 = QtWidgets.QVBoxLayout()
        # self.scroll_list_vbox_l5.setContentsMargins(0, 0, 0, 0)

        self.scroll_list_w4.setLayout(self.scroll_list_vbox_l5)
        self.scroll_area_w3.setWidget(self.scroll_list_w4)
        self.vbox_l2.addWidget(self.scroll_area_w3)

        self.scroll_list_vbox_l5.addStretch(1)

        self.hbox_l3 = QtWidgets.QHBoxLayout()
        self.vbox_l2.addLayout(self.hbox_l3)

        self.delete_spec_time_qpb = QtWidgets.QPushButton("del")
        self.delete_spec_time_qpb.clicked.connect(self.on_del_clicked)
        self.hbox_l3.addWidget(self.delete_spec_time_qpb)

        self.clear_all_qpb = QtWidgets.QPushButton("clear all")
        self.clear_all_qpb.clicked.connect(self.on_clear_all_clicked)
        self.hbox_l3.addWidget(self.clear_all_qpb)

        self.add_new_qgb = QtWidgets.QGroupBox()
        self.hbox_l3.addWidget(self.add_new_qgb)
        hbox_l4 = QtWidgets.QHBoxLayout()
        self.add_new_qgb.setLayout(hbox_l4)

        self.add_new_text_qpb = QtWidgets.QPushButton("Text")
        self.add_new_text_qpb.clicked.connect(functools.partial(
            self.on_add_new_clicked,
            remembering.model_old.ContentType.text
        ))
        hbox_l4.addWidget(self.add_new_text_qpb)
        self.add_new_image_qpb = QtWidgets.QPushButton("Image")
        self.add_new_image_qpb.clicked.connect(functools.partial(
            self.on_add_new_clicked,
            remembering.model_old.ContentType.image
        ))
        hbox_l4.addWidget(self.add_new_image_qpb)
        self.add_new_web_page_qpb = QtWidgets.QPushButton("Web page")
        self.add_new_web_page_qpb.clicked.connect(functools.partial(
            self.on_add_new_clicked,
            remembering.model_old.ContentType.web_page
        ))
        hbox_l4.addWidget(self.add_new_web_page_qpb)
        self.add_new_appl_qpb = QtWidgets.QPushButton("Custom")
        self.add_new_appl_qpb.clicked.connect(functools.partial(
            self.on_add_new_clicked,
            remembering.model_old.ContentType.custom
        ))
        hbox_l4.addWidget(self.add_new_appl_qpb)

        self.add_new_breathing_qpb = QtWidgets.QPushButton("Breathing")
        self.add_new_breathing_qpb.clicked.connect(functools.partial(
            self.on_add_new_clicked,
            remembering.model_old.ContentType.breathing
        ))
        hbox_l4.addWidget(self.add_new_breathing_qpb)

    def on_clear_all_clicked(self):
        for remembrance_item in remembering.model_old.Remembrances.get_all():
            remembering.model_old.Remembrances.update_notif_fired(remembrance_item.id_int, False,
                i_store=False)
        remembering.model_old.Remembrances.store()
        self.list_updated_signal.emit(False)

    def on_del_clicked(self):
        remembering.model_old.RememberItem.del_item(remembering.rg_global.current_item_id_int)
        remembering.rg_global.current_item_id_int = remembering.model_old.RememberItem.get_max_id()
        self.list_item_row_selected()

    def on_add_new_clicked(self, i_content_type: remembering.model_old.ContentType):
        new_remembrance_id_int = remembering.model_old.RememberItem.add_item(
            "",
            i_content_type,
            "",
            remembering.model_old.NO_VALUE_SET_INT
        )
        remembering.rg_global.current_item_id_int = new_remembrance_id_int
        self.list_updated_signal.emit(True)

    def list_item_row_selected(self):
        self.list_updated_signal.emit(False)
        # self.update_gui(i_id)

    def on_item_notif_cleared(self):
        self.list_updated_signal.emit(False)

    def on_item_notif_active_toggled(self):
        self.list_updated_signal.emit(False)

    def update_gui(self, i_id: int = -1):
        if i_id == -1:
            clear_widget_and_layout_children(self.scroll_list_vbox_l5)
            for remember_item in remembering.model_old.Remembrances.get_all():
                list_item = ListItemCw(int(remember_item.id_int))
                list_item.row_selected_signal.connect(self.list_item_row_selected)
                list_item.notif_cleared_signal.connect(self.on_item_notif_cleared)
                list_item.notif_active_toggled_signal.connect(self.on_item_notif_active_toggled)
                # self.vbox_l3.addWidget(list_item)
                # list_item.set_is_current_row(i_id_for_selected_row == int(key_str))
                self.scroll_list_vbox_l5.addWidget(list_item)
            self.scroll_list_vbox_l5.addStretch(1)
        else:
            # clear_widget_and_layout_children(self.scroll_list_vbox_l5)
            # list_items_list = self.scroll_list_vbox_l5.findChildren(ListItemCw)
            i = 0
            while i < self.scroll_list_vbox_l5.count():
                list_item = self.scroll_list_vbox_l5.itemAt(i).widget()
                if type(list_item) is ListItemCw and list_item.id_int == \
                        remembering.rg_global.current_item_id_int:
                    list_item.update_gui()
                i += 1


def clear_widget_and_layout_children(i_qlayout_or_qwidget):
    if i_qlayout_or_qwidget.widget():
        i_qlayout_or_qwidget.widget().deleteLater()
    elif i_qlayout_or_qwidget.layout():
        while i_qlayout_or_qwidget.layout().count():
            child_qlayoutitem = i_qlayout_or_qwidget.takeAt(0)
            clear_widget_and_layout_children(child_qlayoutitem)  # Recursive call


class ListItemCw(QtWidgets.QWidget):
    """
    IMPORTANT: There's a difference between id_int and the globally shared current row id.
    This is important because one row/item can be "selected" and the user can still click on the
    button of another
    item/row
    """
    row_selected_signal = QtCore.Signal()
    notif_cleared_signal = QtCore.Signal()
    notif_active_toggled_signal = QtCore.Signal()

    def __init__(self, i_id: int):
        super().__init__()
        self.updating_gui = True
        self.id_int = i_id

        hbox_l2 = QtWidgets.QHBoxLayout()
        hbox_l2.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox_l2)

        self.notification_fired_qll = CustomNotifLabel(self.id_int)
        self.notification_fired_qll.setFixedWidth(40)
        self.notification_fired_qll.setAlignment(QtCore.Qt.AlignCenter)
        self.notification_fired_qll.mouse_released_signal.connect(
            self.on_notif_fired_mouse_released)
        hbox_l2.addWidget(self.notification_fired_qll)

        self.notifications_active_qpb = QtWidgets.QPushButton("Active")
        self.notifications_active_qpb.setCheckable(True)
        self.notifications_active_qpb.toggled.connect(self.on_notif_active_toggled)
        # self.notifications_active_qpb.setFixedWidth(80)
        hbox_l2.addWidget(self.notifications_active_qpb)

        self.content_type_qll = QtWidgets.QLabel()
        self.content_type_qll.setFixedWidth(30)
        self.content_type_qll.setAlignment(QtCore.Qt.AlignCenter)
        hbox_l2.addWidget(self.content_type_qll)

        self.title_ctl = CustomTitleLabel(self.id_int, "Title")
        # self.title_ctl.setFixedWidth(190)
        self.title_ctl.mouse_released_signal.connect(self.on_title_mouse_released)
        self.title_ctl.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            self.title_ctl.sizePolicy().verticalPolicy(),
        )
        hbox_l2.addWidget(self.title_ctl)

        # hbox_l2.addStretch(1)

        self.update_gui()

        # TODO: Detecting click in this row (or only for the title?)

        # TODO: add another "column" that the user can click to launch the action?
        # This is however already available from the systray, but might be nice
        # It only has to be large enough to click, the action itself doesn't have to be seen
        # Alternatively clicking the title could launch the action, but then we need to find
        # another way to
        # show the settings/details for the row

        self.updating_gui = False

    def on_notif_active_toggled(self, i_checked: bool):
        if self.updating_gui:
            return
        remembering.model_old.Remembrances.update_notif_active(self.id_int, i_checked)

        remembrance = remembering.model_old.RememberItem.get_item(self.id_int)
        if remembrance is not None:
            next_notification_time_ts_secs = remembering.model_old.NO_VALUE_SET_INT
            if remembrance.notif_active_bool:
                next_notification_time_ts_secs = remembrance.get_next_notification_time()
            remembering.model_old.Remembrances.update_next_notif(
                int(self.id_int),
                next_notification_time_ts_secs
            )

        self.update_gui()
        self.notif_active_toggled_signal.emit()

    def on_notif_fired_mouse_released(self):
        # clear notification
        remembering.model_old.Remembrances.update_notif_fired(self.id_int, False)
        self.update_gui()
        self.notif_cleared_signal.emit()

    def on_title_mouse_released(self):
        remembering.rg_global.current_item_id_int = self.id_int
        logging.debug(
            "on_title_mouse_released rg.nn_global.current_item_row_int = " + str(
                remembering.rg_global.current_item_id_int))
        self.row_selected_signal.emit()

    def update_gui(self):
        self.updating_gui = True
        remembrance = remembering.model_old.RememberItem.get_item(self.id_int)
        self.title_ctl.setText(remembrance.title_str)
        self.notifications_active_qpb.setChecked(remembrance.notif_active_bool)
        if remembrance.permanent_bool:
            self.notification_fired_qll.setText("static")
        else:
            if remembrance.notif_fired_bool:
                self.notification_fired_qll.setText("x")
            else:
                if remembrance.next_notif_ts_int != remembering.model_old.NO_VALUE_SET_INT:
                    remaining_time_str = remembering.rg_global.get_time_diff_string(
                        remembrance.next_notif_ts_int,
                        QtCore.QDateTime.currentSecsSinceEpoch()
                    )
                    self.notification_fired_qll.setText(remaining_time_str)
                else:
                    self.notification_fired_qll.setText("")

        content_type_as_letter_str = remembrance.content_type_enum.name[0].upper()
        self.content_type_qll.setText(content_type_as_letter_str)

        # new_font = self.title_ctl.font()
        # new_font.setBold(self.id_int == rg.nn_global.current_item_id_int)
        # self.title_ctl.setFont(new_font)
        self.title_ctl.update_gui(self.id_int == remembering.rg_global.current_item_id_int)

        self.updating_gui = False


class CustomTitleLabel(QtWidgets.QLabel):
    mouse_released_signal = QtCore.Signal(int)  # -id sent

    def __init__(self, i_id: int, i_title: str):
        super().__init__(i_title)
        self.id_int = i_id
        self.update_gui(False)

    def update_gui(self, i_selected: bool):
        if i_selected:
            self.setStyleSheet("QLabel { background-color: #47cf64 }")
        else:
            self.setStyleSheet("QLabel { background-color: #8aeb9f }")

    def mouseReleaseEvent(self, i_qmouseevent):
        self.mouse_released_signal.emit(self.id_int)


class CustomNotifLabel(QtWidgets.QLabel):
    mouse_released_signal = QtCore.Signal(int)  # -id sent

    def __init__(self, i_id: int):
        super().__init__()
        self.id_int = i_id
        self.update_gui()

    def update_gui(self):
        pass
        """
        if i_selected:
            self.setStyleSheet("QLabel { background-color: #47cf64 }")
        else:
            self.setStyleSheet("QLabel { background-color: #8aeb9f }")
        """

    def mouseReleaseEvent(self, i_qmouseevent):
        self.mouse_released_signal.emit(self.id_int)
