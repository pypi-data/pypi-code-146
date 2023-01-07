from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import matc.constants
import matc.gui.breathing
import matc.shared
import matc.state

NEXT = "Next >>"
FINISH = "Finish"
PREV = "<< Prev"
MARGIN_TOP = 35
WIDGET_SPACING = 10

"""
An alternative to using a custom QDialog can be to use QWizard with QWizardPages
"""


class Label(QtWidgets.QLabel):
    def __init__(self, i_text: str):
        text = i_text.strip()  # -removing newlines at beginning and end
        super().__init__(text=text)
        self.setWordWrap(True)
        self.setTextFormat(QtCore.Qt.MarkdownText)
        self.setOpenExternalLinks(True)


class ImageLabel(QtWidgets.QLabel):
    def __init__(self, image_file_path: str):
        super().__init__()
        self.setPixmap(QtGui.QPixmap(image_file_path))


class IntroDlg(QtWidgets.QDialog):
    """
    The introduction wizard with examples of dialogs and functionality to adjust initial settings

    Run using .exec(), so it's run like a modal dialog
    """
    close_signal = QtCore.Signal()

    @staticmethod
    def start():
        dlg = IntroDlg()
        dlg.exec()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Intro Dialog - {matc.constants.APPLICATION_PRETTY_NAME}")
        self.setWindowIcon(QtGui.QIcon(matc.shared.get_app_icon_path()))

        self.wizard_qsw_w3 = QtWidgets.QStackedWidget()
        self.prev_qpb = QtWidgets.QPushButton(PREV)
        self.next_qpb = QtWidgets.QPushButton(NEXT)

        self.prev_qpb.clicked.connect(self.on_prev_clicked)
        self.next_qpb.clicked.connect(self.on_next_clicked)

        hbox_l3 = QtWidgets.QHBoxLayout()
        hbox_l3.addStretch(1)
        hbox_l3.addWidget(self.prev_qpb, stretch=1)
        hbox_l3.addWidget(self.next_qpb, stretch=1)
        hbox_l3.addStretch(1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        vbox_l2.addWidget(self.wizard_qsw_w3)
        vbox_l2.addLayout(hbox_l3)

        welcome_ll = Label("""
## Welcome to Mindfulness at the Computer!

This introduction intends to help you understand how to use the application.

***Mindfulness at the Computer*** is an application that helps you stay ***mindful*** while using 
the computer by reminding you to take ***breathing breaks***. 


These breaks are ***interactive*** to help you focus on your breathing. When breathing we try to 
stay aware of what is going on with the breath, but we don't try to control it.


There are also ***breathing phrases*** that can be used while following the breath, 
to stay mindful of your body, or other aspects of your experience

<br/>

The main parts of the application:
- The system tray icon
- The system tray menu
- The breathing dialog
- The settings window

<br/>

These parts will now be discussed on the following pages. Please click *next* to continue
        """)
        welcome_page = IntroPage(welcome_ll)
        self.wizard_qsw_w3.addWidget(welcome_page)

        systray_icon_ll = Label("""
## The system tray icon

When you run Mindfulness at the Computer it is accessible via the system tray.
From the menu that opens when clicking on this icon you can:
- Open the settings window
- Invoke a breathing session
- Invoke a breathing session with a specified phrase
- Exit the application
        """)
        image_file_path = matc.shared.get_app_icon_path()
        systray_icon_image = ImageLabel(image_file_path)
        systray_icon_notification_ll = Label("""
### The breathing notification

This notification is shown at certain intervals to remind you to take a breathing break. You can 
adjust how often you would like to get this notification.""")
        image_file_path = matc.shared.get_app_icon_path(True)
        systray_icon_br_image = ImageLabel(image_file_path)
        systray_icon_page = IntroPage(systray_icon_ll, systray_icon_image,
            systray_icon_notification_ll, systray_icon_br_image)
        self.wizard_qsw_w3.addWidget(systray_icon_page)

        systray_menu_ll = Label("""
## The system tray menu

You can access the tray menu by clicking or right 
clicking on the systray icon.

The following options are available from the systray menu:
- ***Opening the breathing dialog***
- Switching to a different breathing phrase (through the "Phrases" sub-menu)
- Opening the settings dialog
- Enabling/disabling application notifications
- Exiting the application""")
        image_file_path = matc.shared.get_res_path("systray-menu.png")
        systray_menu_image = ImageLabel(image_file_path)
        systray_menu_page = IntroPage(systray_menu_ll, systray_menu_image)
        self.wizard_qsw_w3.addWidget(systray_menu_page)

        br_dlg_ll = Label("""
## The breathing dialog

This dialog helps you to relax and return to your breathing. Try it out, it's interactive!
        """)
        self.breathing_dlg = matc.gui.breathing.BreathingGraphicsView(i_is_closeable=False)
        self.breathing_dlg.initiate_gv(matc.shared.BrVis.bar.value)
        # self.breathing_dlg.setSizePolicy(QtWidgets.QSizePolicy.Maximum,
        # QtWidgets.QSizePolicy.Minimum)
        self.breathing_dlg.updateGeometry()
        br_dlg_details_ll = Label("""
There are two ways to interact with the breathing dialog:
- Using the mouse cursor to hover over the light green area in the middle while breathing in, 
and leaving the mouse cursor outside the light green area while breathing out
- Using the (right or left) shift key on the keyboard: Pressing down and holding while breathing 
in, and letting it be while breathing out
        """)
        self.br_dlg_page = IntroPage(br_dlg_ll, self.breathing_dlg, br_dlg_details_ll)
        self.wizard_qsw_w3.addWidget(self.br_dlg_page)

        mindful_breathing_tips_ll = Label("""
## Tips for mindfulness of breathing

- We allow our breathing to be like it is, fast or slow, deep or shallow,
without trying to change it
- The breath will naturally deepen after practicing for a while
- We can practice mindfulness of breathing for just a single breath, or we can
practice for several minutes, whatever we feels right for us
- If you are feeling tense it may be useful to practice a bit longer, or to take a
break from the computer for a while

Other breathing applications ask the user to follow a certain tempo, but in our
application we want to do the opposite:
The length of the breaths determines the movement of the graphics! For this to
happen it can be helpful to wait half a second after your breathing has changed (
from in to out or vice versa) before you interact with the breathing dialog.

When you exit the breathing dialog you may wish to continue following the breath and
stay connected with the body. For the transition to be smooth you could exit the
breathing dialog as you start breathing in (or out).
        """)
        self.mindful_breathing_page = IntroPage(mindful_breathing_tips_ll)
        self.wizard_qsw_w3.addWidget(self.mindful_breathing_page)

        settings_ll = Label(f"""
## Settings
The settings dialog can be reached by opening the systray menu and selecting 
"Settings" from there. (Please open it now if you want to follow along in the 
description below)

<br/>

Some of the settings that can be changed:
- Amount of time before a breathing notification is shown --- You may want to adjust this setting 
now (the default is {matc.state.BREATHING_BREAK_TIMER_DEFAULT_SECS // 60} minutes)
- Volume of the audio (bells)
- Breathing phrases (displayed at the bottom of the breathing dialog) --- It is possible to add 
new phrases and reorder them
- Whether or not the application will automatically move the mouse cursor into the breathing 
dialog (useful if you are using a touchpad)
        """)
        settings_page = IntroPage(settings_ll)
        self.wizard_qsw_w3.addWidget(settings_page)

        platform = matc.shared.get_platform()
        if platform == matc.shared.Platform.gnu_linux:
            platform_specific_setup_text = """
The application has been added to the menu system and to autostart."""
        else:
            platform_specific_setup_text = """
Now that you have started the application you may want to do some *additional setup*:"
* Adding a desktop shortcut for the application
* Adding a shortcut to the start menu
* Adding the application to autostart

You can find instructions for doing additional setup on this page:
https://mindfulness-at-the-computer.gitlab.io/installation
"""
        platform_specific_setup_text = platform_specific_setup_text.strip()
        finish_ll = Label(f"""
## Finish

{platform_specific_setup_text}

You can start this wizard again by choosing "Help" -> "Show intro wizard" in the
settings window (available from the system tray icon menu)

Other ways to get help:
- The gitter chat: https://gitter.im/mindfulness-at-the-computer/community
- Email: [{matc.constants.EMAIL_ADDRESS}]({matc.constants.EMAIL_ADDRESS})

We are grateful for any feedback you can give us. Please use the email address above
to contact us with gratitudes or suggestions for improvements."

When you click on finish and exit this wizard a breathing dialog will be shown.
        """)
        finish_page = IntroPage(finish_ll)
        self.wizard_qsw_w3.addWidget(finish_page)

        self.move(150, 100)
        self.update_gui()
        # self.show()

    def on_next_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int >= self.wizard_qsw_w3.count() - 1:
            self.close_signal.emit()
            self.close()
        self.wizard_qsw_w3.setCurrentIndex(current_index_int + 1)
        self.update_gui()

    def on_prev_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        self.wizard_qsw_w3.setCurrentIndex(current_index_int - 1)
        self.update_gui()

    def update_gui(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        self.prev_qpb.setDisabled(current_index_int == 0)

        if current_index_int == self.wizard_qsw_w3.count() - 1:
            self.next_qpb.setText(FINISH)  # "open breathing dialog"
        else:
            self.next_qpb.setText(NEXT)

        if self.wizard_qsw_w3.currentWidget() == self.br_dlg_page:
            self.breathing_dlg.setFocus()


class IntroPage(QtWidgets.QWidget):
    def __init__(self, *i_widgets):
        super().__init__()

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        (cm_left, cm_top, cm_right, cm_bottom) = self.vbox_l2.getContentsMargins()
        self.vbox_l2.setContentsMargins(40, cm_top, 20, cm_bottom)
        self.setLayout(self.vbox_l2)
        self.vbox_l2.addSpacing(MARGIN_TOP)

        for widget in i_widgets:
            self.vbox_l2.addWidget(widget)
            self.vbox_l2.addSpacing(WIDGET_SPACING)

        self.vbox_l2.addSpacing(WIDGET_SPACING)
        self.vbox_l2.addStretch(1)
