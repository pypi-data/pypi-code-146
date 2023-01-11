"""
Created on Nov 15, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtExpand(Model):
    """
    Inherit the basic GUI action, and expand some methods on AtExpand
    """

    def expand_menu_via_css(self, css_selector):
        self._click_element_by_css(css_selector)

    def expand_menu_via_css_from_list(self, css_selector, index):
        self._scroll_browser_to_element_by_css(css_selector)
        self._click_element_in_list_via_css(css_selector, index)

