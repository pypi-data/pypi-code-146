"""
Created on Nov 15, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtClick(Model):
    """
    Inherit the basic GUI action, and expand some methods on AtClick
    """

    def click_link_via_xpath(self, xpath):
        self._click_link_by_xpath(xpath)

    def click_link_via_css(self, css_selector):
        self._click_link_by_css(css_selector)

    def click_element_via_xpath(self, xpath):
        self._click_element_by_xpath(xpath)

    def click_element_via_css(self, css_selector):
        self._click_element_by_css(css_selector)

    def click_element_in_list_by_index_via_css(self, css_selector, index):
        self._click_element_in_list_via_css(css_selector, index)

    def click_element_via_partial_text(self, text):
        self._click_element_by_partial_link_text(text)

    def click_element_after_scroll_via_xpath(self, xpath):
        self._scroll_browser_to_element_by_xpath(xpath)
        self._click_element_by_xpath(xpath)