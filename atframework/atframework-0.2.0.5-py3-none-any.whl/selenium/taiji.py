"""
Created on Mar 02, 2021

@author: Siro

"""


class Taiji(object):
    '''
    Open browser
    '''

    def _open_browser(self, browser_name):
        assert False, 'action must be defined!'

    '''
    Close browser
    '''

    def _close_browser(self):
        assert False, 'action must be defined!'

    '''
    Finally: max browser
    '''

    def _max_browser(self):
        assert False, 'action must be defined!'

    '''
    Finally: bring the browser to front
    '''

    def _bring_to_front(self):
        assert False, 'action must be defined!'

    '''
    scroll browser to target id
    '''

    def _scroll_browser_to_id(self, link_id):
        assert False, 'action must be defined!'

    '''
    scroll browser to target element by css
    '''

    def _scroll_browser_to_element_by_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    scroll browser to target element by xpath
    '''
    def _scroll_browser_to_element_by_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
    click DOEN from css element
    '''
    def _scroll_down_by_key_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    click UP from css element
    '''
    def _scroll_up_by_key_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    access website
    '''

    def _access_website(self, site_address):
        assert False, 'action must be defined!'

    '''
    find Specific Link By Class
    '''

    def _find_link_by_class(self, class_name):
        assert False, 'action must be defined!'

    '''
    click Specific Link By Class
    '''

    def _click_link_by_class(self, class_name):
        assert False, 'action must be defined!'

    '''
    find Specific Link By id
    '''

    def _find_link_by_id(self, link_id):
        assert False, 'action must be defined!'

    '''
    click Specific Link By Class
    '''

    def _click_link_by_id(self, link_id):
        assert False, 'action must be defined!'

    '''
    find Specific link By Text
    '''

    def _find_link_by_text(self, link_text):
        assert False, 'action must be defined!'

    '''
    click Specific link By Text
    '''

    def _click_link_by_text(self, link_text):
        assert False, 'action must be defined!'

    '''
    click Specific link By xpath
    @param element - xpath
    '''

    def _click_link_by_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
    find Specific Button By css_selector
    @param element - css_selector
    '''

    def _find_link_by_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    find Specific Link By xpath
    '''

    def _find_link_by_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
    click Specific Button By css_selector
    param element - css_selector
    '''

    def _click_link_by_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    find Text Field By Id 
    '''

    def _find_text_field_by_id(self, field_id):
        assert False, 'action must be defined!'

    '''
    click Text Field By Id
    '''

    def _type_in_text_field_by_id(self, field_id, input_text):
        assert False, 'action must be defined!'

    '''
    click Text Field By CSS
    '''

    def _type_in_text_field_by_css(self, field_id, input_text):
        assert False, 'action must be defined!'

    '''
    click Text Field By XPath
    '''

    def _type_in_text_field_by_xpath(self, field_xpath, input_text):
        assert False, 'action must be defined!'

    '''
    click Text Field By XPath and click Enter on keyborad
    '''

    def _type_in_text_field_by_xpath_and_click_enter(self, field_xpath, input_text):
        assert False, 'action must be defined!'

    '''
    find Specific Button By Class
    '''

    def _find_button_by_class(self, class_name):
        assert False, 'action must be defined!'

    '''
    find Specific Button By Id
    '''

    def _find_button_by_id(self, id_name):
        assert False, 'action must be defined!'

    '''
    click Specific Button By Class
    '''

    def _click_button_by_class(self, class_name):
        assert False, 'action must be defined!'

    '''
    click Specific Button By id
    param element - class_name
    '''

    def _click_button_by_id(self, id_name):
        assert False, 'action must be defined!'

    '''
    click Specific Button By CSS
    @param element - css_selector
    '''

    def _click_button_by_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    click Specific Button By CSS and javascript
    @param element - css_selector
    '''

    def _click_element_by_css_script(self, css_selector):
        assert False, 'action must be defined!'

    '''
    click Specific Button By xpath and javascript
    @param element - xpath
    '''

    def _click_element_by_locator_script_and_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
    If there are some same element on the page, click Specific Button By index and javascript (index start form 1)
    @param element - css_selector
    '''

    def _click_button_in_list_by_css_script(self, css_selector, index):
        assert False, 'action must be defined!'

    '''
    Click Element By Locator
    @param element - text, locator
    '''

    def _click_element_by_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    Click Element By XPath
    @param element - text, XPath
    '''

    def _click_element_by_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
    Click Element By link text
    @param element - link_text
    '''

    def _click_element_by_link_text(self, link_text):
        assert False, 'action must be defined!'

    '''
    Click Element By partial_link_text
    @param element - partial_link_text
    '''

    def _click_element_by_partial_link_text(self, partial_link_text):
        assert False, 'action must be defined!'

    '''
    Find Element By Locator
    @param element - text, locator
    '''

    def _find_element_by_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    Find Element By css
    @param element - text, locator
    '''

    def _find_element_by_partial_link_text(self, partial_link_text):
        assert False, 'action must be defined!'

    '''
    find Specific element By xpath
     @param - xpath
    '''

    def _find_element_by_xpath(self, xpath):
        assert False, 'action must be defined!'


    '''
    Double click on element
    @param - element
    '''

    def double_click_element(self, webElement):
        assert False, 'action must be defined!'

    '''
    Double click element by Id
    @param - elementId
    '''

    def double_Click_element_by_id(self, elementId):
        assert False, 'action must be defined!'

    '''
    Double click element by Id
    @param - locator
    '''

    def double_click_element_by_css(self, locator):
        assert False, 'action must be defined!'

    '''
    switch to alert
    '''

    def _switch_to_alert(self):
        assert False, 'action must be defined!'

    '''
    switch and then close the alert
    '''

    def _switch_and_close_alert(self):
        assert False, 'action must be defined!'

    '''
    Select Element in DropMenu
    @param element - locator, text, value
    '''

    def _select_dropdown_menu_element_by_css(self, css_selector, text, value):
        assert False, 'action must be defined!'

    '''
    Select Element in DropMenu
    @param element - xpath, text, value
    '''

    def _select_dropdown_menu_element_by_xpath(self, xpath, text, value):
        assert False, 'action must be defined!'

    '''
    Select Element by index in DropMenu
    @param element - locator, index
    '''

    def _select_dropdown_menu_element_by_index(self, locator, index):
        assert False, 'action must be defined!'

    '''
    Select Element by value in DropMenu
    @param element - locator, value
    '''

    def _select_dropdown_menu_element_by_value(self, locator, value):
        assert False, 'action must be defined!'

    '''
    Select Element by text in DropMenu
    @param element - locator, text
    '''

    def _select_dropdown_menu_element_by_text(self, locator, text):
        assert False, 'action must be defined!'

    '''
    Return select options in DropMenu
    @param element - locator
    '''

    def _get_select_dropdown_menu_options(self, locator):
        assert False, 'action must be defined!'

    '''
    Return The first selected option in this select tag (or the currently selected option in a normal select)
    @param element - locator
    '''

    def _get_first_or_current_selected_dropdown_menu_option_text(self, locator):
        assert False, 'action must be defined!'

    '''
     is select check box or not
     @param element - xpath
     '''

    def _is_select_checkbox_by_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
    If there are some same element on the page, click Specific Button By index (index start form 0)
    @param element - css_selector
    '''

    def _click_element_in_list_via_css(self, css_selector, index):
        assert False, 'action must be defined!'

    '''
    If there are some same element on the page, click Specific Button By index (index start form 1)
    @param element - xpath
    '''

    def _click_element_in_list_via_xpath(self, xpath, index):
        assert False, 'action must be defined!'

    '''
    click Specific Button By xpath
    @param element - xpath
    '''

    def _click_button_by_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
    Clear text by css_selector in text field
    @param element - locator
    '''

    def _clear_text_field_by_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
     Clear text by xpath in text field
     @param element - xpath
     '''

    def _clear_text_field_by_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
     Clear text by xpath in text field and send Enter
     @param element - xpath
     '''

    def _clear_text_field_by_xpath_and_enter(self, xpath):
        assert False, 'action must be defined!'

    '''
    Get Text By CSS
    @param element - css locator
    '''

    def _get_text_by_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    Get Text By XPath
    @param element - XPath
    '''

    def _get_text_by_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
    click center key By CSS
    @param element - css locator
    '''

    def _click_enter_key_by_css(self, css_selector):
        assert False, 'action must be defined!'

    '''
    If there are some same elements on the page, find whether has expected text on these elements.
    @param element - expected_text
    '''

    def _is_expected_text_in_elements(self, expected_text):
        assert False, 'action must be defined!'

    '''
    Get Value By XPath
    @param element - XPath
    '''

    def _get_value_by_xpath(self, xpath):
        assert False, 'action must be defined!'

    '''
     Get input disable text By locator script
     @param element - css_selector
     '''

    def _get_input_disable_text_by_locator_script(self, css_selector):
        assert False, 'action must be defined!'

    '''
    switch the frame for locate elements.
    '''

    def _switch_frame(self):
        assert False, 'action must be defined!'

    '''
    switch the frame back to default.
    '''

    def _switch_frame_fack_to_default(self):
        assert False, 'action must be defined!'

    '''
    refresh the current page.
    '''

    def _refresh_page(self):
        assert False, 'action must be defined!'

    '''
    Get elements's URL By Text
    @param element - link_text
    '''

    def _get_element_url_by_text(self, link_text):
        assert False, 'action must be defined!'

    '''
    Take screenshot as jpg and save file
    '''

    def _take_screenshot_as_file(self, file_name):
        assert False, 'action must be defined!'

    '''
    Delete all cookies
    '''

    def _delete_all_cookies(self):
        assert False, 'action must be defined!'

    '''
    Get cookies
    '''

    def _get_cookies(self):
        assert False, 'action must be defined!'

    '''
    Add cookies
    '''

    def _add_cookie(self):
        assert False, 'action must be defined!'
