'''
Created on Mar 03, 2021

@author: Siro

'''

import random
import datetime
import re
import os

from atframework.utils.properties import Properties


class Utils(object):
    site = ""
    browser = ""
    testing_type = ""

    '''
    Get browser header
    '''

    def get_header(self, device='desktop', cookie=''):
        header = {}
        desktop_user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        mobile_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
        tablet_user_agent = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
        jsessionid = 'JSESSIONID=' + cookie
        if device == 'desktop':
            if cookie != '':
                header = {
                    'Cookie': jsessionid,
                    'User-Agent': desktop_user_agent,
                    'Content-Type': 'application/json'
                }
            else:
                header = {
                    'User-Agent': desktop_user_agent,
                    'Content-Type': 'application/json'
                }
        elif device == 'mobile':
            if cookie != '':
                header = {
                    'Cookie': jsessionid,
                    'User-Agent': mobile_user_agent,
                    'Content-Type': 'application/json'
                }
            else:
                header = {
                    'User-Agent': mobile_user_agent,
                    'Content-Type': 'application/json'
                }
        else:#tablet
            if cookie != '':
                header = {
                    'Cookie': jsessionid,
                    'User-Agent': tablet_user_agent,
                    'Content-Type': 'application/json'
                }
            else:
                header = {
                    'User-Agent': tablet_user_agent,
                    'Content-Type': 'application/json'
                }
        return header

    '''
    Get Random phone number from 100000-99999999999
    '''

    def get_phone_number(self):
        number = random.randint(100000, 99999999999)
        phoneNumber = str(number)
        return phoneNumber

    '''
    Get test email xxx@xxx.xxx
    '''

    def get_test_mock_email(self):
        # abc98656@abc98656.xxx
        prefix = str(chr(random.randint(97, 122))) + str(chr(random.randint(97, 122))) + str(
            chr(random.randint(97, 122))) + str(random.randint(0, 100000))
        mid = str(chr(random.randint(97, 122))) + str(chr(random.randint(97, 122))) + str(
            chr(random.randint(97, 122))) + str(random.randint(0, 100000))
        postfix = str(chr(random.randint(97, 122))) + str(chr(random.randint(97, 122))) + str(
            chr(random.randint(97, 122)))
        email = prefix + "@" + mid + "." + postfix
        return email

    '''
    Get Random number from 1-10000
    '''

    def get_test_user_name(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 100000)
        # abc98656
        username = str(name1) + str(name2) + str(name3) + str(number)
        return username

    '''
    Get nick name from 1-10000
    '''

    def get_test_nick_name(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 100000)
        # ab98656c
        nickname = str(name1) + str(name2) + str(number) + str(name3)
        return nickname

    def get_test_user_name_prefix(self, randint=random.randint(0, 10)):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = randint
        # abc9
        usernamePrefix = str(name1) + str(name2) + str(name3) + str(number)
        return usernamePrefix

    def get_all_properties(self, properties_path):
        dictProperties = Properties(properties_path).getProperties()
        return dictProperties

    def get_setup_info(self, properties_path):
        dictInfos = Properties(properties_path).getProperties()
        return dictInfos

    def override_setup_properties(self, file_path, opt_key, opt_value):
        try:
            file_data = ""
            with open(file_path, 'r', encoding='utf-8') as read_setup_properties:
                file_str = read_setup_properties.readlines()
                for line in file_str:
                    line = line.strip().replace('\n', '')
                    find_str = opt_key + '='
                    opt_key_index = line.find(find_str)
                    line_content = line
                    if opt_key_index is not -1:
                        re_file_str = line[(opt_key_index + len(find_str)):]
                        line_content = line.replace(re_file_str, opt_value)
                    file_data += line_content + "\n"
            with open(file_path, 'w', encoding='utf-8') as write_setup_properties:
                write_setup_properties.writelines(file_data)
        except Exception as e:
            raise e

    def get_integration_properties_path(self, site):
        return os.path.abspath(os.path.dirname(os.getcwd(
        ))) + "/properties/" + str(site) + "/integration.properties"

    def get_setup_properties_path(self):
        return os.path.abspath(os.path.dirname(
            os.getcwd())) + "/properties/setup.properties"

    def get_document_image_path(self):
        return os.path.abspath(os.path.dirname(
            os.getcwd())) + '/images/testDocument.jpg'

    def is_xpath(self, xpath):
        result = False
        xpath_prefix = xpath[0:2]
        if str(xpath_prefix) == "//":
            result = True
        return result

    def get_campaign_name(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 10000)
        # abc9865
        campaign = str(name1) + str(name2) + str(name3) + str(number)
        return campaign

    def get_promocode_details(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 10000)
        # abc9865
        promocode = str(name1) + str(name2) + str(name3) + str(number)
        return promocode

    def get_campaign_end_time(self):
        # end in 1 days
        endTime = datetime.datetime.today() + datetime.timedelta(days=1)
        endTimeFormat = endTime.strftime('%Y-%m-%d')
        return endTimeFormat

    def get_rebate_name(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 10000)
        # abc9865
        rebate_name = str(name1) + str(name2) + str(name3) + str(number)
        return rebate_name

    def get_rebate_template_name(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 10000)
        # templateabc9865
        rebate_template_name = 'template' + str(name1) + str(name2) + str(name3) + str(number)
        return rebate_template_name

    def get_rebate_instance_name(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 10000)
        # instanceabc9865
        rebate_instance_name = 'instance' + str(name1) + str(name2) + str(name3) + str(number)
        return rebate_instance_name

    def get_rebate_instance_end_time(self):
        # end in 1 days
        endTime = datetime.datetime.today() + datetime.timedelta(days=1)
        endTimeFormat = endTime.strftime('%Y-%m-%d')
        return endTimeFormat

    def get_testing_type_details_name(self, testing_type):
        if str(testing_type).upper() in 'BAT':
            return 'Build Acceptance Testing'
        elif str(testing_type).upper() in 'BVT':
            return 'Build Acceptance Testing'
        elif str(testing_type).upper() in 'API':
            return 'API Testing'
        elif str(testing_type).upper() in 'ALL':
            return 'Full Testing Cycle'
        else:
            return 'Full Testing Cycle'

    '''
    Format cash/promo from 1,001.23 to 1001.23
    '''
    def format_string(self, cash_or_promo):
        return str(cash_or_promo).replace(",", "")
