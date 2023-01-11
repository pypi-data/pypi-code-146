"""
Created on Nov 15, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtGet(Model):
    """
    Inherit the basic GUI action, and expand some methods on AtGet
    """

    def get_text_via_xpath(self, xpath):
        return self._get_text_by_xpath(xpath)

    def get_value_via_xpath(self, xpath):
        return self._get_value_by_xpath(xpath)

    def get_current_selected_option_text(self, xpath):
        return self._get_first_or_current_selected_dropdown_menu_option_text(xpath)