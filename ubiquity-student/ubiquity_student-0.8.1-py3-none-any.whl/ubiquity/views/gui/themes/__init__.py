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
from .sun_valley_dark import SunValleyDarkTheme
from .sun_valley_light import SunValleyLightTheme


class DuplicateThemeException(Exception):
    """Class Exception for the theme plugins errors"""

    def __init__(self, new_class):
        super().__init__()
        self._new_class = new_class

    def __str__(self):
        return f"duplication of theme id or theme name in {self._new_class.__name__} with an other theme"


class ThemeRegistry:
    """Class managing the theme registry"""
    THEMES = [
        SunValleyDarkTheme,
        SunValleyLightTheme
    ]

    def __init__(self):
        self.themes_classes: dict = {}
        self.themes_id = []
        self.themes_names = []
        self._add_themes()

    def _add_themes(self) -> None:
        """Method adding indicator classes"""
        for theme_class in ThemeRegistry.THEMES:
            self._add_indicator(theme_class)

    def _add_indicator(self, theme_class) -> None:
        """
        Method adding a theme class

        :param theme_class: The theme class
        """
        if theme_class.theme_id() in self.themes_id or theme_class.theme_name() in self.themes_names:
            raise DuplicateThemeException(theme_class)
        self.themes_id.append(theme_class.theme_id())
        self.themes_names.append(theme_class.theme_name())
        self.themes_classes[theme_class.theme_name()] = theme_class

    def get_theme_by_id(self, theme_id):
        for theme in self.themes_classes:
            if theme_id == self.themes_classes[theme].theme_id():
                return self.themes_classes[theme]
        return None
