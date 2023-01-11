"""
Created on Nov 15, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtType(Model):
    """
    Inherit the basic GUI action, and expand some methods on AtType
    """
    def type_text_in_field_via_xpath(self, xpath, input_text):
        self._type_in_text_field_by_xpath(xpath, input_text)

    def type_text_in_field_via_css(self, field_css, input_text):
        self._type_in_text_field_by_css(field_css, input_text)

    def type_text_via_xpath_and_enter(self, field_xpath, input_text):
        self._type_in_text_field_by_xpath_and_click_enter(field_xpath, input_text)