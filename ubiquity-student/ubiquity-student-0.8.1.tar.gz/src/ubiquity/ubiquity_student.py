"""Module managing the application"""
#      ubiquity
#      Copyright (C) 2022  INSA Rouen Normandie - CIP
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import signal
from tkinter import Tk, TclError, PhotoImage
from typing import Any, Union

from . import __version__
from .argument_parser import ArgumentParser
from .controllers.main_controller import MainController
from .model import Model
from .views.cui.main_view import MainView as CuiMainView
from .views.gui.main_view import MainView as GuiMainView
from .views.gui.menu_bar import MenuBar


def _get_kwargs_value(kwargs: dict, key: str, default: Any) -> Any:
    try:
        return kwargs[key]
    except KeyError:
        return default


class App(Tk):
    """Class managing the tkinter application"""
    VERSION = __version__
    LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/ubiquity_icon.png")

    def __init__(self):
        super().__init__()
        config, values, params = ArgumentParser().execute_actions()
        has_form = _get_kwargs_value(params, 'has_form', True)
        has_gui = _get_kwargs_value(params, 'has_gui', True)
        has_color = _get_kwargs_value(params, 'has_color', True)
        has_restore = _get_kwargs_value(params, 'has_restore', False)

        if has_gui:
            config.init_theme()

        self.model = Model(values)
        self.controller = MainController(config, self.model, has_gui)
        signal.signal(signal.SIGINT, self.close)

        if has_restore:
            self.controller.extract_restored_zip()
        self.view = self._get_view(has_gui, has_form, has_color)

    def _get_view(self, has_gui: bool, has_form: bool, has_color: bool) -> Union[GuiMainView, CuiMainView]:
        if has_gui:
            self.title("Ubiquity Student")
            self.geometry("500x200")
            self.minsize(500, 200)
            self.iconphoto(False, PhotoImage(file=App.LOGO))
            self.menu_bar = MenuBar(self, has_form)
            self.config(menu=self.menu_bar)
            self.protocol("WM_DELETE_WINDOW", self.close)
            view = GuiMainView(self, has_form, has_color)
            return view
        self.withdraw()
        return CuiMainView(self.model, self.controller, has_form, has_color)

    def exec(self):
        """Method to execute the application"""
        self.mainloop()

    def close(self, *_, **__):
        """Method to close the application"""
        if self.controller and self.controller.worker:
            self.controller.stop()
        try:
            self.destroy()
        except TclError:
            pass
        self.quit()


def main() -> None:
    """Main function"""
    app = App()
    app.exec()
