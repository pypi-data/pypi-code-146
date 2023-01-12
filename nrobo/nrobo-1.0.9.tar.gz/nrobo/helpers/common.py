import inspect
import json
import os.path as path
import random
import string
import sys
from builtins import FileNotFoundError
from time import time

# import speedtest

try:
    import yaml
    from termcolor import colored
except ModuleNotFoundError as e:
    try:
        import yaml
    except ModuleNotFoundError as e:
        pass


class Common:
    """
    Description
        Customized Selenium WebDriver class which contains all the useful methods that can be re used.
        These methods _help to in the following cases:
        To reduce the time required to write automation script.
        To take the screenshot in case of test case failure.
        To log
        To provide waits
    """

    color_info = 'magenta'
    color_info_on = 'on_blue'
    color_error = 'red'
    color_error_on = color_info_on
    color_success = 'green'
    color_attribute = ['concealed']

    @staticmethod
    def read_file_as_string(file_path):
        try:

            with open(file_path) as f:
                text = f.read()
                return str(text)

        except FileNotFoundError as file_not_found_error:
            Common.print_error("No such file or directory found: " + file_path)

    @staticmethod
    def write_text_to_file(file_path, text):
        try:

            with open(file_path, 'w') as f:
                f.write(text)

        except FileNotFoundError as file_not_found_error:
            Common.print_error("No such file or directory found: " + file_path)

    @staticmethod
    def read_json(file_path):
        """
        Description
            Reads a json file from given file path

        Returns
            data - json file content
        """
        try:

            with open(file_path) as f:
                data = json.load(f)
                return data

        except FileNotFoundError as file_not_found_error:
            Common.print_error("No such file or directory found: " + file_path)

    @staticmethod
    def write_json(file_path, dictionary):
        """
        Writes given dictionary to a file at given file path
        """
        with open(file_path, 'w') as file:  # Open given file in write mode
            json.dump(dictionary, file, sort_keys=True, indent=4)

    @staticmethod
    def is_file_exist(file_path):
        return path.exists(file_path)

    @staticmethod
    def read_yaml(file_path):
        """
        Description
            Reads a yaml file from given file path

        Returns
            data - yaml file content as python dictionary format
        """

        if not path.exists(file_path):
            """if file does not exist, then let's create it first"""

            with open(file_path, 'w') as file:
                """Create a file"""

                # initialize file with empty dictionary
                yaml.dump({}, file)
        else:
            """Do Nothing as file exists"""

        # Read the file
        with open(r'{0}'.format(file_path)) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            data = yaml.load(file, Loader=yaml.SafeLoader)

            # return with data as dictionary
            return data

    @staticmethod
    def write_yaml(file_path, dictionary):
        """
        Description
            Writes given dictionary to a file at given file path
        """
        with open(file_path, 'w') as file:  # Open given file in write mode
            yaml.dump(dictionary, file)

    @staticmethod
    def convert_string_dictionary_to_dictionary(string_dictionary):
        """
        Description
            Coverts given string dictionary to dictionary object

        Returns
            dict obj
        """

        return json.loads(string_dictionary)

    @staticmethod
    def generate_random_string(length):
        """
        Returns a random string of given length

        @Returns string a random string
        """
        random_string = ''.join(random.choices(string.ascii_lowercase +
                                               string.digits + string.ascii_uppercase, k=length))
        return random_string

    @staticmethod
    def get_os():
        """
        Returns platform information

        @Return string platform information
        """
        platform = sys.platform

        return platform

    # @staticmethod
    # def download_speed():
    #
    #     st = speedtest.Speedtest()
    #
    #     return int(st.download() / 1024 / 1024)  # return download speed in Mb/Sec

    # @staticmethod
    # def upload_speed():
    #
    #     st = speedtest.Speedtest()
    #
    #     return int(st.upload() / 1024 / 1024)  # return upload speed in Mb/Sec

    @staticmethod
    def time():
        return time()

    @staticmethod
    def log_page_load_time(page_name, start_time, end_time):
        # internet_speed = Common.download_speed()
        # print(colored("\n Speed: {} Load Time: {} Seconds, Page: {}".
        #              format(internet_speed, int(end_time - start_time), page_name), color_info))
        print(colored("\n[\n\tLoad Time: {} Seconds, \n\tMax Load Time: {} Seconds, \n\tPage: {} \n\tHost Internet "
                      "Speed: {} Mbps\n] "
                      .format(int(end_time - start_time), int(config.wait), page_name, config_v2.internet_speed),
                      color_info))

    @staticmethod
    def is_a_None(anything):
        """
        Return True if _type of anything is None else returns False

        :param anything: Value or Object of _type any
        :return: Boolean
        """
        if type(anything) is type(None):  # Check if _type of anything is None
            return True  # return True if Yes
        else:
            return False  # return False if No

    @staticmethod
    def get_list_of_all_supported_apps():
        """Get list of all supported apps"""

        # all module candidates
        candidates = dir(apps)

        # variable to hold variables only
        supported_apps = []

        for name in candidates:
            """loop through all candidates"""

            # get attribute
            obj = getattr(apps, name)

            if not (
                    inspect.isclass(obj) or
                    inspect.isfunction(obj) or
                    inspect.ismodule(obj) or
                    "__" in name
            ):
                # append to variables list
                # print(name)
                supported_apps.append(obj)

        # return list of supported apps
        return supported_apps

    @staticmethod
    def print_error(message):
        print(message)

    @staticmethod
    def print_info(message):
        print(message)

    @staticmethod
    def print_success(message):
        print(message)

    @staticmethod
    def generate_random_numbers(min, max):
        """
        Returns a random string of given length

        @Returns string a random string
        """
        random_number = random.randint(min, max)

        return random_number


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)
