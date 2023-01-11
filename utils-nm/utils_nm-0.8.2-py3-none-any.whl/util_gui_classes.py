# util_gui_classes.py
# -*- coding: utf-8 -*-

"""
Classes which serve for gui applications.
"""

from typing import Any

from _tkinter import TclError
import tkinter
import tkinter.messagebox
import customtkinter

from .util_functions import split_text


# ______________________________________________________________________________________________________________________


customtkinter.set_appearance_mode('System')  # Modes: 'System' (standard), 'Dark', 'Light'
customtkinter.set_default_color_theme('blue')  # Themes: 'blue' (standard), 'green', 'dark-blue'


# ______________________________________________________________________________________________________________________


class GuiPromptYesNo(customtkinter.CTk):
    """
    Creates a yes / no gui based prompt with default value and countdown functionality.
    The user input will be stored in:
    >>> instance.answer
    """
    WIDTH = 500
    HEIGHT = 200

    def __init__(self, question: str, default_value: str = 'no', countdown_seconds: int = 0):
        super().__init__()
        self.terminated = False

        self.title('input required')
        self.geometry(f'{self.__class__.WIDTH}x{self.__class__.HEIGHT}')
        self.protocol('WM_DELETE_WINDOW', self.on_closing)  # call .on_closing() when app gets closed
        self.resizable(False, False)

        if len(question) > 50:
            question = split_text(text=question, n_chars=50)
        self.question = question
        self.answer = None
        self.default_value = default_value
        self.countdown_seconds = countdown_seconds
        self.remaining_seconds = countdown_seconds

        # ============ create top-level-frames ============

        # configure grid layout (4x1)
        self.equal_weighted_grid(self, 4, 1)
        self.grid_rowconfigure(0, minsize=10)
        self.grid_rowconfigure(3, minsize=10)

        self.frame_label = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frame_label.grid(row=1, column=0)

        self.frame_buttons = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color=None)
        self.frame_buttons.grid(row=2, column=0)

        # ============ design frame_label ============

        # configure grid layout (5x4)
        self.equal_weighted_grid(self.frame_label, 5, 4)
        self.frame_label.grid_rowconfigure(0, minsize=10)
        self.frame_label.grid_rowconfigure(2, minsize=10)
        self.frame_label.grid_rowconfigure(5, minsize=10)

        self.label_question = customtkinter.CTkLabel(
            master=self.frame_label,
            text=self.question,
            font=('Consolas', 12),
        )
        self.label_question.grid(row=1, column=0, columnspan=4, pady=5, padx=10)

        self.label_default_value = customtkinter.CTkLabel(
            master=self.frame_label,
            text='default value: ',
            font=('Consolas', 12),
        )
        self.label_default_value.grid(row=3, column=0, pady=5, padx=10)

        self.entry_default_value = customtkinter.CTkEntry(
            master=self.frame_label,
            width=40,
            justify='center',
            placeholder_text=self.default_value,
            state='disabled',
            textvariable=tkinter.StringVar(value=self.default_value),
            font=('Consolas', 12),
        )
        self.entry_default_value.grid(row=3, column=1, pady=5, padx=10)

        if countdown_seconds > 0:
            self.label_timer = customtkinter.CTkLabel(
                master=self.frame_label,
                text='timer [s]: ',
                font=('Consolas', 12),
            )
            self.label_timer.grid(row=3, column=2, pady=5, padx=10)

            self.entry_timer = customtkinter.CTkEntry(
                master=self.frame_label,
                width=40,
                justify='center',
                state='disabled',
                textvariable=tkinter.StringVar(value=str(self.remaining_seconds)),
                placeholder_text=str(self.remaining_seconds),
                font=('Consolas', 12),
            )
            self.entry_timer.grid(row=3, column=3, pady=5, padx=10)

        # ============ design frame_buttons ============

        # configure grid layout (3x2)
        self.equal_weighted_grid(self.frame_buttons, 3, 2)
        self.frame_buttons.grid_rowconfigure(0, minsize=10)
        self.frame_buttons.grid_rowconfigure(2, minsize=10)

        self.button_yes = customtkinter.CTkButton(
            master=self.frame_buttons,
            text='yes',
            font=('Consolas', 12),
            command=lambda: self.button_event('yes'),
        )
        self.button_yes.grid(row=1, column=0, pady=5, padx=20)

        self.button_no = customtkinter.CTkButton(
            master=self.frame_buttons,
            text='no',
            font=('Consolas', 12),
            command=lambda: self.button_event('no'),
        )
        self.button_no.grid(row=1, column=1, pady=5, padx=20)

        if self.countdown_seconds > 0:
            self.countdown()

        self.attributes('-topmost', True)
        self.mainloop()

    # __________________________________________________________
    # methods

    @staticmethod
    def equal_weighted_grid(obj: Any, rows: int, cols: int):
        """configures the grid to be of equal cell sizes for rows and columns."""
        for row in range(rows):
            obj.grid_rowconfigure(row, weight=1)
        for col in range(cols):
            obj.grid_columnconfigure(col, weight=1)

    def button_event(self, answer):
        """Stores the user input as instance attribute `answer`."""
        self.answer = answer
        self.terminate()

    def countdown(self):
        """Sets the timer for the question."""
        if self.answer is not None:
            self.terminate()
        elif self.remaining_seconds < 0:
            self.answer = self.default_value
            self.terminate()
        else:
            self.entry_timer.configure(textvariable=tkinter.StringVar(value=str(self.remaining_seconds)))
            self.remaining_seconds -= 1
            self.after(1000, self.countdown)

    def stop_after_callbacks(self):
        """Stops all after callbacks on the root."""
        for after_id in self.tk.eval('after info').split():
            self.after_cancel(after_id)

    def on_closing(self, event=0):
        """If the user presses the window x button without providing input"""
        if self.answer is None and self.default_value is not None:
            self.answer = self.default_value
        self.terminate()

    def terminate(self):
        """Properly terminates the gui."""
        if not self.terminated:
            # stop all .after callbacks to avoid error message "Invalid command ..." after destruction
            self.stop_after_callbacks()

            self.terminated = True
            try:
                self.destroy()
            except TclError:
                self.destroy()


# ______________________________________________________________________________________________________________________


"""
# example usage
if __name__ == '__main__':
    print('before')

    q1 = GuiPromptYesNo(question='1. do you want to proceed?', countdown_seconds=5)
    print(f'>>>{q1.answer=}')

    print('between')

    q2 = GuiPromptYesNo(question='2. do you want to proceed?', countdown_seconds=5)
    print(f'>>>{q2.answer=}')

    print('after')
"""


# ______________________________________________________________________________________________________________________
