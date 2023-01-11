"""
Created on Nov 15, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtClear(Model):
    """
    Inherit the basic GUI action, and expand some methods on AtClear
    """
    def clear_text_from_field_via_xpath(self, xpath):
        self._clear_text_field_by_xpath(xpath)

