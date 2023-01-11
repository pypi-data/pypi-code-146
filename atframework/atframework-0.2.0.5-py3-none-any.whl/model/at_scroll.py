"""
Created on Nov 15, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtScroll(Model):
    """
    Inherit the basic GUI action, and expand some methods AtScroll
    """

    def scroll_browser_to_target_via_xpath(self, xpath):
        self._scroll_browser_to_element_by_xpath(xpath)





