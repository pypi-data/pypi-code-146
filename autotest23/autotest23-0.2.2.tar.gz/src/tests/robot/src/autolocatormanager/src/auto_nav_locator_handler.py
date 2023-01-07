import os
from ... import ObjMapper
from bs4 import BeautifulSoup
from ... import IoC_Container
from ..constants import Constants
from ...managepom.src.abstract.i_automation import IAutomation
from .abstract.i_auto_nav_locator_handler import IAutoNavLocatorHandler


class AutoNavLocatorHandler(IAutoNavLocatorHandler):
    
    def page_element_identifier_and_writer(self, payload: dict):
        page_class_file_paths = {}
        if not os.path.exists(Constants.NAV_BAR_FILE_PATH):
            raise "NavBar-Locator not found! Please, refresh the POM Manager and try again."
        html_chunk = payload["html_content"]
        base_url = payload["base_url"]
        page_names_with_locators = self.nav_bar_identifier(html_chunk.body,base_url)

        if page_names_with_locators is None:
            print("end with single page")
            return

        nav_locators = self.__update_page_name_with_tag_name(page_names_with_locators)
        print("""
        if override is `yes` then old locators override and 
        update these locators which is already exists.=.
        if `no` this all old locators replaced by new locators.
        """)
        nav_override = input("Do you want to override nav locators? (y/n): ")
        print(self.module_locator_writer_obj.module_code_writer(Constants.NAV_BAR_FILE_PATH, nav_locators, nav_override))
        if page_names_with_locators is not None:
            page_names_list = list(page_names_with_locators.keys())
            page_class_file_paths = self.generate_page_classes(page_names_list)
        else: 
            print("\n\n===================No Sub pages found from Navigation Bar <===================\n\n")
        pages_payload = self.scrap_targeted_page(base_url, page_names_with_locators)
        pages_payload_updated = {k: v for k, v in pages_payload.items() if v is not None}
        # if not pages_payload_updated:
        #     print("\n\n===========> Not Auto writable content found. Please, do it manually. <===========\n\n")
        #     return None
        pages_payload = self.__process_page_name_by_tag(pages_payload_updated)

        self.__write_locator_to_file(pages_payload, nav_override)
    
    def __process_page_name_by_tag(self, pages_payload: dict):
        tags_by_text: dict = {}
        for page in pages_payload:
            if pages_payload[page] is None:
                continue
            html_content = pages_payload[page]['page_payload']['html_content']
            html_content.nav.decompose()
            tags_from_page_body = html_content.body.findAll(Constants.PRIORITY_ATTRIBUTES_IN_PAGE_BODY)
            for tag in tags_from_page_body:
                if tag.name == "input" and tag.attrs['type'] == "hidden":
                    continue
                if tag is None:
                    continue
                tag_text = self.find_tag_text_as_page_name(tag)
                if tag_text is None:
                    continue
                tag_text = self.__text_cleaner(tag_text)
                tags_by_text[tag_text] = tag
            tags_and_locators_by_name = self.locator_extractor(html_content, tags_by_text.copy())
            filtered = {k: v for k, v in tags_and_locators_by_name.items() if v is not None}
            pages_payload[page]['page_payload']['html_tags_locators'] = filtered.copy()
            filtered.clear()
            tags_by_text.clear()
            tags_and_locators_by_name.clear()
        return pages_payload
        
    def nav_bar_identifier(self, html_body: BeautifulSoup, baseurl):
        nav_exist: bool = False
        tag_list = []
        # Checking a specific tag. checking the existence in a specific html page
        for tag in html_body.findAll(True):
            if "nav" == str(tag.name):
                nav_exist = True
        if nav_exist:
            tags_from_nav_bar = html_body.nav.findAll(Constants.NAV_TARGETED_HTML_TAGS)
            pages_with_locators = self.get_page_list_from_nav_bar(html_body, tags_from_nav_bar)
            pages_with_locators_updated = {k: v for k, v in pages_with_locators.items() if v is not None}
            return pages_with_locators_updated
        else:
            print("No Navigation Bar found!..trying to generate for current page")

            self.single_page_element_identifier()

            return None

    def show_and_process_idetified_pages(self, nav_page_list: dict) -> dict:
        ignore_list = list(nav_page_list.keys())
        print("This is the List of identified pages from the Navigation Bar.")
        self.print_list_with_index(ignore_list)
        auto_generate_concent = input("\n\nDo you want to auto generate these pages? (y/n) : ")
        if auto_generate_concent.lower() == "y":
            # Preparing user defined ignore index list.
            ignore_index_list = self.user_defined_index_numbers(len(nav_page_list))
            # If the ignore list is not empty nav_page_list will get modified
            if ignore_index_list:
                for i, item in enumerate(ignore_list):
                    # Checking ignore list index number and enlisting it in new list.
                    if i in ignore_index_list:
                        del nav_page_list[ignore_list[i]]
                self.print_list_with_index(list(nav_page_list.keys()))    # Printing updated List 
            return nav_page_list
        elif auto_generate_concent.lower() == "n":
            print("********You can create custom page classes from the POM manager.********")
            # Getting Object id of the main menu.
            id = ObjMapper.OBJ_MAP['robo_manager']
            # Getting Main Menu object reference
            route = ObjMapper.id2obj(id)
            # Calling Method from the instance
            route.menu()
            return None
        else:
            raise "User input unknown!"
        
    def find_tag_text_as_page_name(self, tag):
        page_name = None        
        if len(tag.text) > 0:
            # If text is found in the text that will be assigned as Page Name.
            page_name = self.__text_cleaner(tag.text)
        else:
            # If text is not found then it will look for other targeted attributes.
            for alt_attr in Constants.OPTIONAL_HTML_ATTR:
                if alt_attr in tag.attrs:
                    # If any of those attributes are hould with a meaningful page name 
                    # that text will be assigned as page_name
                    page_name = tag.attrs[alt_attr]
                    break
                else: 
                    page_name = None
        return page_name
    
    def __text_cleaner(self, text_content: str) -> str:
        """This private method will take a string as a parameter and 
        convert it into a Number & Special character free string. © BS23"""
        if text_content is None:
            return None
        text_content = text_content.rstrip('\r|\n')
        text_content = ''.join(e for e in text_content if e.isalnum())                
        text_content = text_content.strip()
        return text_content
    
    def get_page_list_from_nav_bar(self, html_chunk, tag_list: list) -> dict:
        page_by_tag: dict = {}
        for tag in tag_list:
            if self.find_tag_text_as_page_name(tag) is None:
                # If no Page name representative text is found this look 
                # will skip this tag and look for the next.
                continue
            page_by_tag[self.find_tag_text_as_page_name(tag)] = tag
        page_by_tag = self.show_and_process_idetified_pages(page_by_tag)
        # Updating tag dictionary after having modification from Test Engineer 
        return self.locator_extractor(html_chunk,page_by_tag)
    
    def __update_page_name_with_tag_name(self, page_by_tag: dict) -> dict:
        name_with_tag_by_tag = {}
        for page_name in page_by_tag:
            tag = page_by_tag[page_name]['tag']
            name_with_tag_by_tag[f"{page_name}_{tag.name}_tag"] = page_by_tag[page_name]
        return name_with_tag_by_tag
    
    def generate_page_classes(self, updated_page_list: list) -> dict:
        try:
            # Getting IoC Container
            ioc_container = IoC_Container.CONTAINER
            # Creating Scraper class instance
            manage_pom_automate_obj: IAutomation = ioc_container.resolve(IAutomation)
            # According to the Dictionary Key -> 2 is the number of Page Class type
            new_modules_abs_file_path = manage_pom_automate_obj.auto_generate_modules(2, updated_page_list)
            return new_modules_abs_file_path
        except Exception as err:
            raise f"Something went wrong! \n Error: {err}"
    
    def locator_extractor(self, html_body: BeautifulSoup, identity_placeholder_by_tag_map: dict) -> dict:
        return self.get_tag_locator(html_body, identity_placeholder_by_tag_map)
    
    def print_list_with_index(self, content_list: list) -> None:
        return self.user_handler_obj.print_list_with_index(content_list)
    
    def user_defined_index_numbers(self, max_num: int) -> list:
        return self.user_handler_obj.user_defined_index_numbers(max_num)
    
    def scrap_targeted_page(self, base_url: str, locators_and_tags: dict) -> dict:
        return self.scrap_page_by_nav_obj.scrap_targeted_page(base_url, locators_and_tags)
    
    def _get_routing_link(self, locators_and_tags: dict) -> str:
        return self.scrap_page_by_nav_obj._get_routing_link(locators_and_tags)


    def single_page_element_identifier(self, payload: dict):
        html_chunk = payload["html_content"]
        base_url = payload["base_url"]
        html_body = html_chunk.body
        title = html_chunk.title.text
        tags_by_text = {}
        tags_from_page_body = html_body.findAll(Constants.PRIORITY_ATTRIBUTES_IN_PAGE_BODY)
        for tag in tags_from_page_body:
            if self.find_tag_text_as_page_name(tag) is not None:
                tag_text = self.find_tag_text_as_page_name(tag)
                tags_by_text[tag_text] = tag

        tags_and_locators_by_name = self.locator_extractor(html_body, tags_by_text.copy())
        filtered = {k: v for k, v in tags_and_locators_by_name.items() if v is not None}
        # locator_values = tags_and_locators_by_name
        page_name = self.__text_cleaner(title)
        page_class_file_paths = self.generate_page_classes([page_name])
        pages_payload = {
            page_name: {
                "page_payload":{
                    "html_tags_locators": filtered
                }
            }
        }
        # pages_payload = self.__process_page_name_by_tag(pages_payload)
        self.__write_locator_to_file(pages_payload)

    def __write_locator_to_file(self, pages_payload: dict, nav_override=None):

        for page_name in pages_payload:
            new_locator_file_name = page_name.replace(" ", "_").lower()+"_page_locators.py"
            locator_file_path = str(os.path.join(Constants.PAGE_LOCATOR_DIRECTORY_PATH, new_locator_file_name))
            locator_values = pages_payload[page_name]['page_payload']['html_tags_locators']
            print(self.module_locator_writer_obj.module_code_writer(locator_file_path, locator_values, nav_override))
        print("==============END==============")
    