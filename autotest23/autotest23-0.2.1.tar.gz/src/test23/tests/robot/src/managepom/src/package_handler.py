"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from .abstract.i_pom_structure import IPOMStructure

class PackageHandler(IPOMStructure):
    """
    PackageHandler is responsible for auto creating all the packages and repositories 
    according to the Page Object Model (POM) map from the pom.xml file.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def create_pom_structure(self, file_path: str, pom_root_base_path: str):
        pom_map = self.__get_pom_structure(file_path)
        for base in pom_map.keys():
            if os.path.exists(pom_root_base_path) and os.path.basename(pom_root_base_path) == base:
                directory_list: list = pom_map[base]
                print(self.__make_pom_structure(pom_root_base_path, directory_list))
            else:
                return "Location unkown! Please, check your path and try again."
        print("---END---")
    
    def __get_pom_structure(self, file_path: str):
        # Getting XML file parsed data as Tree Structure.
        xml_tree = ET.parse(r"%s" %file_path)
        # Identifying data from the root.
        pom_root_map = xml_tree.getroot()
        # Re-mapping xml.etree structure to Python Dictionary through recursion.
        pom_map:dict = self.__convert_etree_to_dict(pom_root_map)
        return pom_map    
      
    # recursion    
    def __convert_etree_to_dict(self, xml_etree):
        # Getting tag name from xml.etree structure
        name = xml_etree.attrib['name']
        # Traversing every tag and making LIST all the child through recursion.
        # If any of these tags dont have any child the children list will be enpty.
        children = [self.__convert_etree_to_dict(c) for c in xml_etree]
        # If children is available it will return as dictionary structure 
        # where KEY will be parent name and VALUE will be list.
        # Else this method will just return the parent name 
        # as the list named children is empty.
        return {name: children} if children else name
    
    # Making directory (recursion)
    def __make_pom_structure(self, pom_root_base_path:str, directory_list: list):
        for directory in directory_list:
            # Checking the Data Type.
            if isinstance(directory, dict):
                for parent_directory in directory.keys():
                    # First createing a directory which have children/child.
                    print(self.__make_directory(pom_root_base_path))
                    # Going inside the newly created directory.
                    pom_root_base_path = str(os.path.join(pom_root_base_path, parent_directory))
                    # Getting the this list of children directory names 
                    temp_list = directory[parent_directory]
                    # Passing the list again of the children directory names (recursion) 
                    self.__make_pom_structure(pom_root_base_path, temp_list)
                    # Getting out from the current directory.
                    pom_root_base_path = str(Path(pom_root_base_path).parent)
            else:
                pom_root_base_path = str(os.path.join(pom_root_base_path, directory))
                print(self.__make_directory(pom_root_base_path))
                # Getting out from the current directory.
                pom_root_base_path = str(Path(pom_root_base_path).parent)
        return "--END--"
        
    def __make_directory(self, current_directory_path:str):
        # Only if the folder is not already created then this method will create the folder
        if not os.path.exists(current_directory_path):
            os.makedirs(current_directory_path)
            return "====>"+os.path.basename(current_directory_path)+" created......"
        # If the folder already exist this method will avoid that list content
        elif os.path.exists(current_directory_path):
            return "****"+os.path.basename(current_directory_path)+" already created!****"
        else:
            return "**********Someting went wrong!**********"
        
    def __create_module(self, module_name: str, module_type: str, module_location: str):
        # This method is responsible for creating modules accroding to POM Map
        # and write blueprint codes inside them. [ This is part of future Scope]
        module_content = None   #Future Scope
        module_path = str(os.path.join(module_location, module_name+".py"))
        # w stands for Writing.
        with open(module_path, 'w') as file:
            file.write(json.dumps(module_content))
        return "Module Created."
        
    def __save_path_by_id(self, path_map_dict: dict, pom_map_path: str):
        # This method is used for saving a python dictionary file into static file.
        # w stands for Writing.
        with open(pom_map_path, 'w') as file:
            file.write(json.dumps(path_map_dict))
        return "Path map of Page Object Model (POM) has been saved"