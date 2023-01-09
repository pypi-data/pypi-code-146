"""
This is a GUI to prompt you to hibernate your computer.

It can easily be delayed an hour by pressing the delay button.
If you want to cancel the process after that you can right click the system tray icon
and hit exit
"""

import datetime
import os
import subprocess
import sys
import time

import PySimpleGUI as sg
from psgtray import SystemTray

from .__version__ import __version__

DELAY_TEXT = "Delay"
HIBERNATE_TEXT = "Hibernate"
DELAY_TIMEDELTA = datetime.timedelta(hours=1)

if os.name != "nt":
    raise NotImplementedError(
        "This program only works on Windows.. feel free to PR hibernate calls for other OS's!"
    )


def hibernate_and_exit() -> None:
    """
    Tells Windows to Hibernate NOW and then exits the program

    Funny enough the exit may happen right after the system resumes.
    """
    subprocess.call("shutdown /h", shell=True)

    sys.exit(0)


def countdown_to_str(countdown: int) -> str:
    """
    Takes the given int and adds a 's' after it
    """
    return f"{countdown}s"


def run(countdown: int = 300) -> None:
    """
    Starts the GUI and runs the countdown
    """
    window = sg.Window(
        "SleepyTime?",
        [
            [
                sg.Text("Hibernating in: "),
                sg.Text(countdown_to_str(countdown), key="countdown"),
            ],
            [
                sg.Button(DELAY_TEXT, bind_return_key=True, expand_x=True),
                sg.Button(HIBERNATE_TEXT, expand_x=True),
            ],
        ],
        grab_anywhere=True,
        alpha_channel=0.8,
        no_titlebar=True,
        keep_on_top=True,
        resizable=False,
        disable_close=True,
        disable_minimize=True,
        font=("Arial", 50),
        location=(30, 30),
    )

    sys_tray = SystemTray(
        menu=["", ["Exit"]],
        tooltip=f"SleepTime {__version__} is running...",
        window=window,
    )

    death_time = time.time() + countdown
    unhide_time = None

    try:
        while time.time() < death_time:
            event, values = window.read(timeout=500)
            # print(event, values)

            window["countdown"].update(
                countdown_to_str(int(max(0, death_time - time.time())))
            )

            if unhide_time and unhide_time < time.time():
                # we unhide, reset unhide time and reset death time
                window["countdown"].update(countdown_to_str(countdown))
                death_time = time.time() + countdown
                window.un_hide()
                unhide_time = None

            if event == DELAY_TEXT:
                window.hide()
                unhide_time = time.time() + DELAY_TIMEDELTA.total_seconds()
                sys_tray.set_tooltip(f"Sleeping until: {unhide_time}")

            elif event == HIBERNATE_TEXT:
                hibernate_and_exit()
            elif (
                event in (sg.WIN_CLOSED, "Exit")
                or event == SystemTray.DEFAULT_KEY
                and values[sys_tray.key] == "Exit"
            ):
                break
            elif event == sg.EVENT_TIMEOUT:
                continue
        else:
            hibernate_and_exit()
    finally:
        window.close()
        sys_tray.close()
