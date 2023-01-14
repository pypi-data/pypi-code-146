from os import walk
import os

try:
    from nrobo.config import nRoboConfig
except ModuleNotFoundError as e:
    from config import nRoboConfig


# Get list of test files under given folder
def get_list_of_files(folder, file_extension, ignore_file_names=[]):
    # folder path
    dir_path = folder
    print(dir_path)
    # list to store files name
    res = []
    for (dir_path_, dir_names, file_names) in walk(dir_path):
        for file_name in file_names:
            # print(dir_path_ + "<>" + file_name)
            f_name, f_extension = os.path.splitext(file_name)
            if f_extension == file_extension:
                match_found = False
                for ignore_file_name in ignore_file_names:
                    if f_name == ignore_file_name:
                        match_found = True
                        break
                if not match_found:
                    res.append(dir_path_ + os.sep + file_name)

    return res


def list_test_files_for_launcher(dirname):
    test_files = ""
    list_of_test_files = get_list_of_files(dirname, ".py", ["__init__"])
    for test_file_name in list_of_test_files:
        test_files = test_files + nRoboConfig.Constants.SPACE.value + test_file_name

    return test_files
