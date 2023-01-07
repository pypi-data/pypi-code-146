import os
import textwrap
from .abstract.module_content import ModuleContent


class ConstractPageObject(ModuleContent):
    """
    This concrete class holds the methods for constructing Page and Abstract locator classes with source code included.
     © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def __init__(self) -> None:
        self.IMPORT_LIBRARY = """
        from tests.resources.custom_keywords import CustomKeywords
        from tests.constants.common_constants import CommonConstants
        from tests.pages.locators.nav_bar_locators import NavBarLocators
        """
        self.CLASS_FIXTURE = None
        self.METHOD_FIXTURE = None
        self.DEFAULT_METHOD_WITH_ARGUMENTS = """
        def __init__(self):
            self.log(file_directory= self.LOG_FILE_PATH_LOCATION)
        
        def example_method(self):
            self.logger.warning("nav_locator: "+self.NAV_LOCATOR_TESTER)
            self.logger.warning("page_locator: "+self.PAGE_LOCATOR_TESTER)
            self.logger.warning("Page Found.")
        """
        # Page locator will append in the method section for inheritance. 
        self.INHERITED_CLASSES = ["CommonConstants", "CustomKeywords", "NavBarLocators"] 
        self.CLASS_COMMENT = None
        self.METHOD_BLOCK_COMMENT = None
        self.CLASS_FIXTURE_BLOCK_COMMENT = None     
        self.full_body_structure = None
        # This Constant is for page classes only
        self.page_locators_page_template = """
        from abc import ABC

        class ExamplePageLocator(ABC):
    
            PAGE_LOCATOR_TESTER = "Page locator found."
            '''This constsant is for connectivity test only  [BS23]'''"""
        self.LOCATOR_FILE_RELATIVE_PATH = "locators"
        self.LOCATOR_IMPORT = "from tests.pages.locators.example_page_locator import ExamplePageLocator"
        
    def construct_module_with_source_code(self, module_name: str, module_path_location: str):
        create_file_path = str(os.path.join(module_path_location, module_name))
        self.__prepare_module_body_structure(module_name, module_path_location)
        # w stands for Writing.
        with open(create_file_path, 'w') as file:
            file.write(self.full_body_structure)
        print("New script file has been created!")
        return create_file_path
    
    def __prepare_module_body_structure(self, module_name, module_path_location):   
        #https://docs.python.org/3/library/textwrap.html
        ws = " "
        import_library = textwrap.dedent(self.IMPORT_LIBRARY)
        locator_import_path = textwrap.dedent(self.LOCATOR_IMPORT)
        module_name = module_name.title()
        class_name = module_name.replace("_", "").replace(".Py", "")
        source_code = textwrap.dedent(self.page_locators_page_template)
        page_locator_class_name, page_locator_module_name = self.__constract_page_locator_source_code(module_name, class_name, source_code, module_path_location)
        locator_import_path = locator_import_path.replace("example_page_locator", page_locator_module_name.replace(".py", "")).replace("ExamplePageLocator", page_locator_class_name)
        self.INHERITED_CLASSES.append(page_locator_class_name)
        inherited_classes = str(', '.join(self.INHERITED_CLASSES))
        default_method = textwrap.dedent(self.DEFAULT_METHOD_WITH_ARGUMENTS)
        self.full_body_structure = \
            import_library + "\n" +\
            locator_import_path + "\n\n" +\
            f"class {class_name}({inherited_classes}): \n"+\
            textwrap.indent(default_method, ws*4)
            
    def __constract_page_locator_source_code(self, module_name: str, class_name: str, \
        source_code: str, module_path_location: str):
        module_name = module_name.replace("Page", "page_locators").lower()
        class_name = class_name.replace("Page", "PageLocators")
        source_code = source_code.replace("ExamplePageLocator", class_name)
        module_path_location =  str(os.path.join(module_path_location, self.LOCATOR_FILE_RELATIVE_PATH))
        
        create_file_path = str(os.path.join(module_path_location, module_name))
        # w stands for Writing.
        with open(create_file_path, 'w') as file:
            file.write(source_code)
        print("Page locator has been created!") 
        return class_name, module_name