"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
from abc import ABC, abstractmethod
from typing import List


class ModuleContent(ABC):
    """
     This abstract class holds all the constant components and abstract methods 
     which are common for a auto-generated script/module body. Such as import libraries, 
     packages class and variables etc.
     © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    SCRIPT_HEADER_DOCUMENT = """
    Reminder: Make sure to use logger where it is needed. 
    These given log type will keep record in the log file.
    Logger Levels:
        * error
        * warning
        * critical
    [BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)]
    """
    
    IMPORT_LIBRARY: str = None
    """This holds all the import libraries and packages source code. © BS23"""
    CLASS_FIXTURE: str = None
    """This holds the important fixtures which will be placed over the class. © BS23"""
    METHOD_FIXTURE: str = None
    """This holds the important fixtures which will be placed over the methods/functions. © BS23"""
    DEFAULT_METHOD_WITH_ARGUMENTS: str = None
    """This constant string holds the default method body including its arguments. © BS23"""
    INHERITED_CLASSES:list = []
    """This constant list holds the class names which will be inherited. Class names will be string. © BS23"""
    CLASS_COMMENT: str =  None
    """This constant holds the class detail documentation in a multiline string. If mouse 
    is hovered over that targeted class this string will be visible (VS Code feature). © BS23"""
    METHOD_BLOCK_COMMENT: str = None
    """This holds the comment for the default method. The string should start with #.
    Example:
        # Line one comment
        continue......
    © BS23"""
    CLASS_FIXTURE_BLOCK_COMMENT: str = None
    """This holds the block comment for the default fixture. The comment should start with #. © BS23"""
    
    full_body_structure:str = None
    """This is the main variable where concatenation took place of all the constant variables. According 
    to their concatenation sequence a complete module template structure will be created. © BS23"""
    
    @abstractmethod
    def construct_module_with_source_code(self, module_name: str, module_path_location: str):
        """This method collets module name and its path as argument and 
        generate a new module, including its source code. © BRAIN STATION 23"""
        pass
    
    