from abc import ABC, abstractmethod
from lxml import etree
from bs4 import BeautifulSoup
from ...constants import Constants
import re


class ILocatorExtractor():
    
    @abstractmethod
    def locator_extractor(self, html_body: BeautifulSoup, identity_placeholder_by_tag_map: dict) -> dict:
        """
        This method will take the HTML body section and a dictionary mapped as identity name (Variable) by html tags.
        After having those arguments this method will be able to extract the locator.  
        © BS23
        """
        
    @abstractmethod
    def delete_displayed_text(self, element):
        """
        delete displayed text from beautiful soup tag element object recursively
        :param element: beautiful soup tag element object
        :return: beautiful soup tag element object
        """
    
    def get_tag_locator(self, html_chunk: BeautifulSoup, target_page_dict: dict) -> dict:
        """
        This method will take a chunk of HTML part (convert it to String) and dictionary of 
        html tags as parameter and will try to identify their locators.
        Then return a dictionary where value will be also a dictionary which will contain attribute 
        name : its value and their HTML tag.
        Example: 
                {  
                    'user_name_text_box': {
                        'id': 'u_name',
                        'tag': <a href='example.com'>Hello World</a>
                    }  
                }
        © BS23
        """
        attr_name = None
        for tag_key in target_page_dict:
            for tag_attr in Constants.PRIORITY_ATTRIBUTES_AS_LOCATOR:
                current_tag = target_page_dict[tag_key]
                if tag_attr in current_tag.attrs:
                    attr_name = tag_attr
                    attr_value = current_tag.attrs[tag_attr]
                    target_page_dict[tag_key] = {
                        attr_name: attr_value,
                        'tag': target_page_dict[tag_key]
                    }
                    break
                else: 
                    attr_name = None
            if attr_name is None:
                target_page_dict[tag_key] = \
                    self.get_xpath_of_single_tag(html_chunk, target_page_dict[tag_key])
        return target_page_dict
    
    def get_xpath_of_single_tag(self, html_chunk, target_tag):
        """
        This method will take a chunk of HTML part (convert it to String) and a html tags 
        as parameter and replace the targeted tag with their XPath. Then return the updated dictionary. 
        © BS23
        """
        try:
            html_chunk = str(html_chunk)
            # parsing xml with illegal special characters
            html_chunk = html_chunk.replace('&', '&amp;')
            # Getting root object
            root = etree.fromstring(html_chunk)
            # Converting HTML into tree structure
            tree = etree.ElementTree(root)
            for e in root.xpath('//*'):
                if str(target_tag) == str(etree.tostring(e).decode()):
                    # If any match found from the actual HTML body XPath will get updated in the dictionary
                    target_tag = {
                        'xpath': f"/{str(tree.getpath(e))}",
                        'tag': target_tag
                        }
                    break
                else:
                    continue
            if isinstance(target_tag, dict):
                return target_tag
            else:
                print(f"XPath can not get generate for this tag: {target_tag}")
                return None
        except Exception as err:
            print(err)
            return None 
             
    def get_xpath_of_multiple_tags(self, html_chunk, target_page_dict: dict) -> dict:
        """
        This method will take a chunk of HTML part (convert it to String) and dictionary of 
        html tags as parameter and replace those targeted tages with their XPath. Then return 
        the updated dictionary. © BS23
        """
        root = etree.fromstring(str(html_chunk))
        tree = etree.ElementTree(root)
        for e in root.xpath('//*'):
            for page_name in target_page_dict:
                # Searching element accordinmg to user choice dictionary list.
                if str(target_page_dict[page_name]) == str(etree.tostring(e).decode()):
                    # If any match found from the actual HTML body XPath will get updated in the dictionary
                    target_page_dict[page_name] = "/"+str(tree.getpath(e))
                    break
                else:
                    continue
        return target_page_dict