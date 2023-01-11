"""
Created on Mar 03, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtWaiting(Model):
    """
    Inherit the basic GUI action, and expand waiting methods
    """
    def refresh_page(self):
        self._refresh_page()

    def waits(self, wait_seconds):
        self._pause(wait_seconds)

    def wait_css_shown(self, css_selector):
        self._wait_for_css_shown_and_sleep(css_selector)

    def wait_xpath_shown(self, xpath):
        self._wait_for_xpath_shown_and_sleep(xpath)

    def wait_xpath_shown2(self, xpath):
        return self._wait_for_xpath_shown2_and_sleep(xpath)

    def wait_css_and_click(self, css_selector):
        self._wait_for_css_shown_and_click(css_selector)
