import os
from abc import ABC


class Constants(ABC):
    # This is a Set which is unordered, unchangeable*, and unindexed collection.
    # Set is used here to hold Key Components of POM because Set do not allow duplicate values.
    # If there is any modification at pom.xml, please add the new tag name here in the Set.
    KEY_COMPONENTS = {"repository","package", "packages"}
    # These set elements will be used for identifying tags and their ID from pom_module_map.xml file.
    DYNAMIC_COMPONENTS = { 3: "test_scenario_0001",
                           2: "example_page", 
                           2.5: "example_page_locator"}

    # https://docs.python.org/3/library/os.path.html
    POM_TEMPLATE_FILE_PATH = str(os.path.join(os.path.dirname(__file__), "property", "pom.xml"))
    POM_MODULE_TEMPLATE_FILE_PATH = str(os.path.join(os.path.dirname(__file__), "property", "pom_module_map.xml"))
    POM_CUSTOM_MODULE_PATH = str(os.path.join(os.path.dirname(__file__), "property", "modules"))
    POM_ROOT_BASE_PATH = str(os.path.join(os.path.realpath(''), "tests"))
    AUTOMATION_SCRIPT_GENERATE_SUCCESS_MESSAGE = "=======>All the scripts generated successfully<======="