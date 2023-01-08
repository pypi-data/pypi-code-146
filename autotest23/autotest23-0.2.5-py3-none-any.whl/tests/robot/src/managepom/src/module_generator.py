"""
Adapter Design Pattern
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
import os
import re
import ast
import glob
from .abstract.i_module_generator import IModuleGenerator
from .modulesourcecode.scenario import ConstractTestScenario
from .modulesourcecode.page_object import ConstractPageObject


class ModuleGenerator(IModuleGenerator):
    """
    ModuleGenerator is a child of ModuleHandler class which is responsible for taking 
    inputs of file name and generate that as a script/module including source code
    and placing that module in the targated places according to its ID.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def generate_module(self, module_type_name: str, pom_map_path: str, pom_module_map_path: str, root_path: str, module_name: str = None):
        module_root_obj_map = self.module_handler_obj._get_xml_tree_root(pom_module_map_path)
        # Passing module name and xml map (tree format) as argument 
        # and assigning three return values at module_location_id, module_name, module_extension 
        module_location_id, module_type_name, module_extension = \
            self.__get_module_id_name_extension(module_type_name, module_root_obj_map)
        file_naming_convension =  module_type_name +"."+ module_extension
        # This private method is from ModuleHandler class. This will only update 
        # the given ID in the module_location_id variable in the path_map_by_id_dict dictionary.  
        self.module_handler_obj.path_generator_as_list(module_location_id, pom_map_path)     # Updating....
        module_placement_path_list = self.module_handler_obj.path_map_by_id_dict[str(module_location_id)]
        module_placement_relative_path = self.module_handler_obj._list_to_path_converter(module_placement_path_list)
        # Creating absolute path
        generate_module_path = str(os.path.join(root_path, module_placement_relative_path))
        if os.path.exists(generate_module_path):
            check_content = module_type_name.lower()
            if check_content.startswith("test"):
                self.__get_all_modules_in_package(generate_module_path, file_naming_convension)
            else:
                file_naming_convension = self.__take_input_and_convert_naming_convension(module_extension, module_name)
                return self.__create_new_script_with_source_code(file_naming_convension, generate_module_path) 
        else:
            raise """
                    Path unkown! Please check pom.xml & pom_module_map.xml files.
                    Or try to refresh POM structure from robot app.
                """
        
    def __get_module_id_name_extension(self, module_name, module_root_obj_map):
        """This method will take module name and xml map in tree format as 
        parameters and return module id, name and extension as string. © BS23"""
        for module in module_root_obj_map:
            if module_name == module.attrib["name"]:
                return module.attrib["id"], module.attrib["name"], module.attrib["extension"]
        raise "No common module found! [module_generator.py]"
    
    def __take_input_and_convert_naming_convension(self, module_extension, module_name):
        """This method will take file extention as parameter and convert it according to PEP8
        style and naming convention. After that returning it as file name including file extention. © BS23"""
        file_name = module_name
        if module_name is None:
            file_name = input("Please provide page name and press ENTER: ")
        file_name = file_name.lower().replace(" ", "_") # Replacing whitespace with _
        file_name = file_name +"_page."+ module_extension # Adding file naming convention.
        return file_name
    
    def has_numbers(self, inputString):
        return any(char.isdigit() for char in inputString)
    
    # Function to convert  
    def listToString(self, component_list): 
        placeholder = "_" 
        # return string  
        return (placeholder.join(component_list))
    
    def __get_all_modules_in_package(self, target_path, file_naming_convension):
        """This method will take path and file name as parameters and get list how many script files are available in 
        that targeted path. Then auto-generate new file with source-code according to a specific order sequence. © BS23"""
        modules_list = glob.glob(target_path+"/*.py")
        if len(modules_list) > 0:
            # If file exist in the targeted path  private method __generate_new_file_name will be called .
            # All module list of that targeted path and file name will be passed as argument.
            # New file name will be assigned at new_file_name from the method's return value.
            new_file_name = self.__generate_new_file_name(modules_list, file_naming_convension)
        else:
            # If targeted path is empty the given sample file name will be considered as the main file name
            new_file_name = file_naming_convension 
        test_obj = ConstractTestScenario()
        print(test_obj.construct_module_with_source_code(new_file_name, target_path))
        
    def __create_new_script_with_source_code(self, new_file_name, target_path):
        """This method will take file name and path as parameters and with the help of ConstractPageObject 
        class a new module will be generted and will return the new generated file path. © BS23"""
        script_generator_obj = ConstractPageObject()
        return script_generator_obj.construct_module_with_source_code(new_file_name, target_path)
    
    def __generate_new_file_name(self, modules_list, file_naming_convension):
        """This method will take file list and a sample file name as parameters.  
        From the given module list this method will identify the max file serial number 
        and create the name file name oder by that serial number. Number length will be always 4.
        Then new file name (with extention) with preoper naming convention will be returned as a string. 
        © BS23"""
        temp_current_module_number = 0
        temp_max_module_number = 0
        for module_path in modules_list:
            module = str(os.path.basename(module_path))
            if self.has_numbers(module):
                temp_current_module_number = int(re.sub("[^0-9]", "", module))
                if temp_max_module_number < temp_current_module_number:
                    temp_max_module_number = temp_current_module_number
            else:
                raise f"Module name {module} is not appropriate. \
                    Please, follow the naming convention."

        temp_max_module_number = temp_max_module_number + 1
        new_module_numbner = str('%04d' % temp_max_module_number)
        current_file_name_as_list = file_naming_convension.split("_")
        for component in current_file_name_as_list:
            if self.has_numbers(component):
                index_position = current_file_name_as_list.index(component)
                current_file_name_as_list[index_position] = str(new_module_numbner +".py")
        new_file_name = self.listToString(current_file_name_as_list)
        return new_file_name
            
            
        