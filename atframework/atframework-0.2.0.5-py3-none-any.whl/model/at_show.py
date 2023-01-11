"""
Created on Mar 03, 2021

@author: Siro

"""

from atframework.model.model import Model


class AtShow(Model):
    """
    Check the element whether show.
    """

    def is_find_element_via_css(self, css_selector):
        return self._find_element_by_css(css_selector)

    def is_find_element_via_xpath(self, xpath):
        return self._find_element_by_xpath(xpath)

    def is_find_link_via_xpath(self, xpath):
        return self._find_link_by_xpath(xpath)

    def is_find_link_via_css(self, css_selector):
        return self._find_link_by_css(css_selector)

    def is_find_link_via_text(self, text):
        return self._find_link_by_text(text)

    def is_page_shown_via_xpath_text(self, xpath, expected_text):
        text = self._get_text_by_xpath(xpath)
        if text.strip() == expected_text:
            return True
        return False

    def is_page_shown_via_xpath_text_fuzzy_match(self, xpath, expected_result):
       text = self._get_text_by_xpath(xpath)
       if expected_result in text.strip():
           return True
       return False

    def is_page_shown_via_xpath_expected_text(self, xpath, expected_text):
        if self._find_link_by_xpath(xpath) is True:
            text = self._get_text_by_xpath(xpath)
            if text.strip() == expected_text:
                return True
            return False
        else:
            return False

    def is_page_shown_via_css_expected_text(self, css_selector, expected_text):
        if self._find_link_by_css(css_selector) is True:
            text = self._get_text_by_css(css_selector)
            if text.strip() == expected_text:
                return True
            return False
        else:
            return False

    def is_removed_latest_item(self, xpath, latest_item_text):
        item_text = self._get_text_by_xpath(xpath)
        if str(item_text).find(latest_item_text) is not -1:
            return False
        else:
            return True

    def is_text_in_elements(self, text):
        return self._is_expected_text_in_elements(text)

    def is_added_item(self, item_text, target_text):
        if str(item_text).find(target_text) is not -1:
            return True
        else:
            return False
