import os
import textwrap
from .abstract.module_content import ModuleContent


class ConstractTestScenario(ModuleContent):
    """
    This concrete class holds the methods for constructing Test Scenario with source code.
     © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def __init__(self) -> None:
        self.IMPORT_LIBRARY = """
        import pytest
        from time import sleep
        from django.test import LiveServerTestCase
        from tests.drivercontroller.driver_controller import DriverController
        """
        self.CLASS_FIXTURE = """
        @pytest.mark.usefixtures("suit_setup_and_tear_down")
        """
        self.METHOD_FIXTURE = """"""
        self.DEFAULT_METHOD_WITH_ARGUMENTS = """
        def test_case_0001(self):
            self.logger.warning("This auto-generated Test-Case is empty.")
        """
        self.INHERITED_CLASSES = ["LiveServerTestCase", "DriverController"]
        self.CLASS_COMMENT = """
        The classe and method names should start with Test...
        inside the test_scenerio_xxx.py file. If this naming convention
        is not followed properly these test scenerios/ test cases
        will not run with pytest command.
        """
        self.METHOD_BLOCK_COMMENT = """
        # Write your test case here.
        """
        self.CLASS_FIXTURE_BLOCK_COMMENT = """
        # This fixture is default for a quick start If needed Tester can
        # remove this fixture and call methods directly from the DriverController.
        # to design own Test Scenerio and Test Cases.
        """     
        
        self.full_body_structure = None
    
    def construct_module_with_source_code(self, module_name: str, module_path_location: str):
        create_file_path = str(os.path.join(module_path_location, module_name))
        self.__prepare_module_body_structure(module_name)
        # w stands for Writing.
        with open(create_file_path, 'w') as file:
            file.write(self.full_body_structure)
        return "New script file has been created!"
    
    def __prepare_module_body_structure(self, module_name):
        #https://docs.python.org/3/library/textwrap.html
        ws = " "
        header_doc = textwrap.dedent(f'"""{self.SCRIPT_HEADER_DOCUMENT}"""')
        import_library = textwrap.dedent(self.IMPORT_LIBRARY)
        class_fixture = textwrap.dedent(self.CLASS_FIXTURE)
        class_block_cmnt = textwrap.dedent(self.CLASS_FIXTURE_BLOCK_COMMENT)
        class_name = module_name.replace("_", "").replace(".py", "").title()
        inherited_classes = str(', '.join(self.INHERITED_CLASSES))
        class_doc_cmnt = textwrap.dedent(f'"""{self.CLASS_COMMENT}"""')
        default_method = textwrap.dedent(self.DEFAULT_METHOD_WITH_ARGUMENTS)
        self.full_body_structure = \
            header_doc +\
            import_library + "\n" +\
            class_block_cmnt +\
            class_fixture+\
            f"class {class_name}({inherited_classes}): \n"+\
            textwrap.indent(class_doc_cmnt, ws*4) +\
            self.METHOD_BLOCK_COMMENT +\
            textwrap.indent(default_method, ws*4)