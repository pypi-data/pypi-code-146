"""
Created on Nov 15, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtSelect(Model):
    """
    Inherit the basic GUI action, and expand some methods AtSelect
    """

    def select_dropdown_menu_element_via_locator_value(self, locator, value):
        self._select_dropdown_menu_element_by_value(locator, value)

    def select_dropdown_menu_element_via_locator_text(self, locator, text):
        self._select_dropdown_menu_element_by_text(locator, text)


