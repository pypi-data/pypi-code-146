import re
import sys

try:
    from colorama import init
    from nrobo.config import nRoboConfig
except ModuleNotFoundError as e:
    pass

class SecurityChecks:
    """
    This class holds several framework security-backup procedures
    """

    def __init__(self):
        """SecurityChecks constructor

        Nothing special to do as of now here.
        """
        try:
            from colorama import init
            from nrobo.config import nRoboConfig
        except ModuleNotFoundError as e:
            pass
        # init colorama
        init()

        pass

    @staticmethod
    def __is_an_restricted_application_link(self):
        """
        Description
            Check if the application link is restricted/prohibited to launch test.

        Returns
            Boolean -> True if application link restricted, else returns False.
        """

        # Get app link
        app_link = nRoboConfig.URL

        # replace https protocol string with empty string if it is present
        app_link = re.sub(nRoboConfig.Constants.HTTPS.value, nRoboConfig.Constants.EMPTY.value, app_link)

        # replace http protocol string with empty string if it is present
        app_link = re.sub(nRoboConfig.Constants.HTTP.value, nRoboConfig.Constants.EMPTY.value, app_link)

        # loops though all the available apps
        # for app in COMMON.get_list_of_all_supported_apps():
        #
        #     if CONSTANTS.UNDERSCORE in app:
        #         """if app is having multiple words separated by underscore"""
        #
        #         # split app name by underscore
        #         app = re.split(CONSTANTS.UNDERSCORE, app)
        #
        #         # use only first word for url match
        #         match_found = re.search("^" + app[0].lower() + "*.*(.com)$", app_link)
        #     else:
        #         """app name is a single word"""
        #
        #         # use only single word for url match
        #         match_found = re.search("^" + app.lower() + ".*(.com)$", app_link)
        #
        #     if match_found:
        #         """if match found, then application link is a restricted link"""
        #
        #         # return to the caller with True
        #         return True


        # link is fine for launching tests-backup
        return False

    def perform_url_security_check(self):
        """
        Description
            Perform url security-backup check
        """

        # get app link
        app_link = nRoboConfig.CommandLineSwitchesLong.URL

        if self.__is_an_restricted_application_link(self):
            """if app link is restricted"""

            # inform user that he/she is trying to launch test on a restricted url.
            print("Test link {0} failed URL security-backup check.".format(app_link))

            # capture the details of the test, test machine and shoot an email to panchdev.chauhan@spherewms.com

            sys.exit(1)
        else:
            print("Test link {0} passed URL security-backup check.".format(app_link))
