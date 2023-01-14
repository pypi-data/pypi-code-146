import os
import shutil

"""
|- assets
|- config
|- helpers
|- pages
|- security
|- tests
|- test_data
|- test_output
|- tests_advanced_reports
|- tests_api
|- tests_performance
|- tools
"""

dir_structure = [
    "assets",
    "config",
    "helpers",
    "pages",
    "security",
    "tests",
    "test_data",
    "test_output",
    "tests_advanced_reports",
    "tests_api",
    "tests_performance",
    "tools"
]


def create_dir_structure():
    """
    Create directory structure for tests development

    :return:
    """

    for index in range(len(dir_structure)):
        # iterate through dir_structure and create folder structure

        # STEP-2: Copy framework files to respective project directory
        framework_dir = "framework"
        sep = os.sep
        source_dir = framework_dir + sep + dir_structure[index]
        target_dir = dir_structure[index]

        # Copy folder tree
        try:
            shutil.copytree(source_dir, target_dir)
        except OSError as oserror:
            print(oserror)
            pass

    # Copy file only
    try:
        shutil.copy("framework/speedboat.py", "speedboat.py")
        shutil.copy("framework/conftest.py", "conftest.py")
    except OSError as oserror:
        print(oserror)
        pass


def create_directory(dir_path):
    try:
        os.mkdir(dir_path)
        if os.path.isdir(dir_path):
            print("Directory, " + dir_path + ", created successfully!")
        elif os.path.isfile(dir_path):
            print("File, " + dir_path + ", created successfully!")
    except OSError as osError:
        if os.path.isdir(dir_path):
            print("Directory, " + dir_path + ", already exists!")
        elif os.path.isfile(dir_path):
            print("File, " + dir_path + ", already exists!")
        pass