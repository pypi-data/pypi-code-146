"""
Created on Mar 03, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtClosing(Model):
    def teardown_browser(self):
        self._close_browser()

    def take_screenshot_file(self, file_name):
        self._take_screenshot_as_file(file_name)

    def click_logout_button_via_css(self, link_css):
        self._click_element_by_css(link_css)

    def is_logout_successfully(self, link_id):
        self._wait_for_id_shown_and_sleep_2s(id_name=link_id)
        return self._find_link_by_id(link_id)
