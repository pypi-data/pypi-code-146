"""
Created on Mar 03, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtOpening(Model):
    def setup_browser(self, browser_name):
        return self._open_browser(browser_name)

    def max_browser(self):
        self._max_browser()

    def access_web_url(self, url):
        self._access_website(url)

    def access_web_url_till_one_time(self, site_name):
        self._access_website_till_one_time(site_name)

    def bring_to_front(self):
        self._bring_to_front()

    def delete_all_cookies_at(self):
        self._delete_all_cookies()

    def get_cookies_at(self):
        self._get_cookies()

    def add_cookie_at(self, cookie_dict):
        self._add_cookie(cookie_dict)