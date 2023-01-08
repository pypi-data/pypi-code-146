"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
import os
from pathlib import Path
from shutil import copy
from xml.dom.minidom import Element
import xml.etree.ElementTree as ET
from .abstract.i_pom_module_handler import IPOMModuleHandler


class ModuleHandler(IPOMModuleHandler):
    """
    ModuleHandler is responsible for collecting specific modules from the 
    property and placing those in the targated places.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    # This will hold all the directories as a list ordered by id.
    path_map_by_id_dict = {}
    # This will temporary hold the directory name list to assign 
    # the name list into the path_map_by_id_dict dictionary.
    path_in_list = []
    """This list is for temporary use only during the loop traversal."""
    
    SUPPORTED_TAG_TYPES = {"module", "file"}
        
    def create_pom_modules(self, pom_map_path: str, pom_module_map_path: str, \
        custom_module_path: str, pom_root_base_path: str):
        self.__arrance_module_path_by_id(pom_map_path, pom_module_map_path)
        
        # Converting xml to tree fromat and getting its root object.
        pom_module_root_obj_map = self._get_xml_tree_root(pom_module_map_path)
        self.__copy_paste_modules(pom_root_base_path, custom_module_path, \
            self.path_map_by_id_dict, pom_module_root_obj_map)
        
    def _get_xml_tree_root(self, xml_file_path):
        tree_map_root_object = None
        # Converting xml to tree fromat.
        map_xml_tree = ET.parse(r"%s" %xml_file_path)
        # Getting the root object address to map the whole module file tree.
        tree_map_root_object = map_xml_tree.getroot()
        return tree_map_root_object
    
    def __arrance_module_path_by_id(self, pom_map_path: str, pom_module_map_path: str):
        # Converting xml to tree fromat.
        pom_module_root_obj_map = self._get_xml_tree_root(pom_module_map_path)
        # Traversing every tag.
        for module in pom_module_root_obj_map:
            # Getting the tag's id attribute. 
            module_location_id = module.attrib["id"]
            self.__path_generator_as_list(module_location_id, pom_map_path) 
            
    # Encapsulation         
    def path_generator_as_list(self, module_location_id, pom_root_map):
        """
        This method will take a module id and POM Model file location. Then 
        this method will search for the same tag id in the POM model as a 
        Foreign Key and dig down to its child directories to arrange a list 
        sequesce and map it oderded by module id as a Dictionary. [dict: path_map_by_id_dict]
        © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
        """
        self.__path_generator_as_list(module_location_id, pom_root_map)
    
    def __path_generator_as_list(self, module_location_id, pom_root_map):
        """
        This method will take a module id and POM Model file location. Then 
        this method will search for the same tag id in the POM model as a 
        Foreign Key and dig down to its child directories to arrange a list 
        sequesce and map it oderded by module id as a Dictionary. [dict: path_map_by_id_dict]
        © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
        """
        # Converting xml to tree fromat and getting its root object.
        pom_root_map = self._get_xml_tree_root(pom_root_map)
        # Getting ID and Sub-ID of POM model directories/packages as a list
        pom_location_id_as_list = module_location_id.split(".")
        # Traversing every parent tag of POM model.
        for parent_tag in pom_root_map:
            # Converting current tag id into ID and Sub-ID format as a list.
            current_location_id_as_list = str(parent_tag.attrib["id"]).split(".")
            # After coverting the location id a specific parent tag can be targeted.
            if pom_location_id_as_list[0] == current_location_id_as_list[0]:
                # Enlisting the base-location name (tag name) in the temporary list.
                self.path_in_list.append(parent_tag.attrib["name"])       
                # If the current tag/base-location have any child then we will take help of recursion. 
                if len(parent_tag) > 0 and module_location_id != str(parent_tag.attrib["id"]):
                    self.__arrange_path_list(parent_tag, module_location_id)
                #Enlisting the updated list in the dictionary ordered by Module ID as KEY.
                self.path_map_by_id_dict[module_location_id] = self.path_in_list.copy()
                # As mentioned this list is for temporary use we are clearing it every 
                # time after our each operation.
                self.path_in_list.clear()
        
    # recursion   
    def __arrange_path_list(self, pom_root_obj_map, module_location_id):
        """
        This method is responsible arrange directories and sub-directories as 
        a list through recursion and update the list temporarily at the path_in_list  
        © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
        """
        for repo in pom_root_obj_map:
            # Enlisting the base-location name (tag name) in the temporary list.
            self.path_in_list.append(repo.attrib["name"])
            # checking If the Targeted module id and current POM base tag is same or not
            if module_location_id == str(repo.attrib["id"]):
                # If both are same method will return from the recursion.
                return
            # Else if the current repor have more children
            elif len(repo) > 0:
                # recursion will take place.
                self.__arrange_path_list(repo, module_location_id) 
            # Else if we are at the dead end and no Matched id is found, 
            # this method will start popping elements from the list it its 
            # back tracking journey of recursion.
            elif len(repo) <= 0:
                self.path_in_list.pop()
                
    def __copy_paste_modules(self, root_directory: str, copy_path: str, \
        paste_path_dict: dict, pom_module_tree_map: Element):
        temp_copy_file_path: str = None
        temp_paste_file_path = None
        # Traversing every module and file tag.
        for module in pom_module_tree_map:
            # Converting path list to string path.
            temp_paste_file_path = self._list_to_path_converter(\
                paste_path_dict[str(module.attrib["id"])]\
                    )
            # Concatenating relative and root path to create an absolute path
            temp_paste_file_path = str(os.path.join(root_directory, temp_paste_file_path))
            # Check if the current tag is suppoted or not.
            if str(module.tag) in self.SUPPORTED_TAG_TYPES:
                # If it is supported then concatenating the file name with extension.
                temp_copy_file_path = os.path.join( copy_path, \
                    str(module.attrib["name"])+"."+str(module.attrib["extension"])\
                        )
            else:
                print("File type unknown. Please checkyour xml files.")
                # If file type in unknown this single loop traversel will be skipped.
                continue 
            # Checking if the copy and paste paths are valid or not.
            if os.path.exists(temp_copy_file_path) and os.path.exists(temp_paste_file_path):
                # Copying file from the first argument (path with file name and extension) and
                # Pasting file in the second argument.   
                copy(temp_copy_file_path, temp_paste_file_path)
                print(f"""
                      **************************************************************************
                      {str(module.tag)} name: {str(module.attrib["name"])+"."+str(module.attrib["extension"])},
                      Placed successfully to the path: {temp_paste_file_path}.
                      **************************************************************************
                      """)
            else:
                print(f"""
                      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                      Path unknown. Please checkyour pom.xml file.
                      Copy Path: {temp_copy_file_path}
                      Paste Path: {temp_paste_file_path}  
                      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                      """)
                # If copy path or paste path is unknown, this single loop traversel will be skipped. 
                continue 
        print("Copy Success!!!")
                
    def _list_to_path_converter(self, path_in_list):
        temp_path = ""
        for directory in path_in_list:
            temp_path = str(os.path.join(temp_path, directory))
        return temp_path
