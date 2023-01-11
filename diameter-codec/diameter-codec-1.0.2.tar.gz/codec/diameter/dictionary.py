import logging
import os.path
from abc import ABC, abstractmethod
from typing import NamedTuple, Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


class AvpDict(NamedTuple):
    """ Dictionary NamedTuple """
    application_id: int
    code: int
    name: str
    type: str
    content_type: str
    vendor_id: int
    vendor_flag: bool
    mandatory_flag: bool
    enums: dict


class DictionaryLayout(ABC):
    """ ABC DictionaryLayout """
    __dictionary: ElementTree

    @abstractmethod
    def __init__(self, path: str):
        if not path:
            raise ValueError("Path is None.")

        if len(path.strip()) == 0:
            raise ValueError("Path is empty.")

        if not os.path.exists(path):
            raise FileNotFoundError("Path is not valid.")

        if not os.path.isfile(path):
            raise FileNotFoundError("Path doesn't point to file. Maybe it is a directory.")

        dictionary: ElementTree = ElementTree.parse(path)
        self.__dictionary = dictionary

    def get_dictionary(self) -> ElementTree:
        """
        Diameter dictionary.
        :return: diameter xml object
        """
        return self.__dictionary

    @abstractmethod
    def find_avp_by_name(self, application_id: int, avp_name: str) -> Optional[AvpDict]:
        """
        Find avp by name.
        :param application_id: application id
        :param avp_name: avp name
        """

    @abstractmethod
    def find_avp_by_code(self, application_id: int, avp_code: int) -> Optional[AvpDict]:
        """
        Find avp by code.
        :param application_id: application id
        :param avp_code: avp code
        """


class DefaultDictionaryLayout(DictionaryLayout):
    """ DefaultDictionaryLayout """
    def __init__(self, path: str):
        """
        Constructor.
        :param path: path to file
        """
        super().__init__(path)
        self._ns = {'xmlns': self.__find_namespace(super().get_dictionary())}

    @staticmethod
    def __find_namespace(dictionary: ElementTree):
        tag: str = dictionary.getroot().tag
        if tag.startswith("{") and tag.index("}") > 0:
            return tag[1:tag.index("}")]

        raise AttributeError(f"Namespace attribute not found in {tag}.")

    def __enums(self, avp_xml: Element) -> dict:
        enums: dict = {}
        enum_ns: str = f'{"{" + self._ns["xmlns"] + "}"}enum'
        try:
            for _c in avp_xml:
                if _c.tag == enum_ns:
                    key: int = int(_c.get("value"))
                    enums[key] = _c.text
        except ValueError as _e:
            logging.error(_e)

        return enums

    def find_avp_by_code(self, application_id: int, avp_code: int) -> Optional[AvpDict]:
        """
        Internally uses xpath.
        <avp code="319" mandatory-flag="must" may-encrypt="no" name="Maximum-Number-Accesses" protected-flag="-"
            sect="10.1.38" type="Unsigned32" vendor="TGPP" vendor-flag="must"></avp>
            :param avp_code:
            :param application_id: application id
            :rtype: object
            :return: Avp definition from dictionary
        """
        if application_id < 0:
            raise ValueError("application_id must be greater or equal to 0.")

        if avp_code < 0:
            raise ValueError("avp_code is None or empty.")

        dictionary: ElementTree = super().get_dictionary()
        query_xpath_avp: str = f"xmlns:application[@id='{application_id}']/" \
                               f"xmlns:avps/xmlns:avp[@code='{avp_code}']"

        avp_xml: Element = dictionary.find(query_xpath_avp, self._ns)

        if avp_xml is None:  # find next (recursion)
            query_xpath_extends: str = f"xmlns:application[@id='{application_id}']/[@extends]"
            attr_extends: Element = dictionary.find(query_xpath_extends, self._ns)
            if not attr_extends:
                return None

            extends_value: str = attr_extends.get("extends")
            query_xpath_next: str = f"xmlns:application/[@name='{extends_value}']"
            attr_next: Element = dictionary.find(query_xpath_next, self._ns)
            next_id: int = int(attr_next.get("id"))
            avp_dict: AvpDict = self.find_avp_by_code(next_id, avp_code)
            if avp_dict:
                return avp_dict

        avp_name: str = avp_xml.get("name")
        vendor: str = avp_xml.get("vendor")
        avp_vendor_flag: bool = avp_xml.get("vendor-flag") == "must"

        #   find vendor id
        query_xpath_vendor: str = f"xmlns:vendors/xmlns:vendor[@name='{vendor}']"
        vendor_xml: Element = dictionary.find(query_xpath_vendor, self._ns)
        avp_vendor_id: int = int(vendor_xml.get("id"))

        avp_type: str = avp_xml.get("type")
        content_type: str = avp_xml.get("contenttype", "")
        avp_mandatory_flag: bool = avp_xml.get("mandatory-flag") == "must"

        enums: dict = self.__enums(avp_xml)

        return AvpDict(application_id,
                       avp_code,
                       avp_name,
                       avp_type,
                       content_type,
                       avp_vendor_id,
                       avp_vendor_flag,
                       avp_mandatory_flag,
                       enums)

    def find_avp_by_name(self, application_id: int, avp_name: str) -> Optional[AvpDict]:
        """
        Internally uses xpath.
        <avp code="319" mandatory-flag="must" may-encrypt="no" name="Maximum-Number-Accesses" protected-flag="-"
        sect="10.1.38" type="Unsigned32" vendor="TGPP" vendor-flag="must"></avp>
           :param avp_name:
           :param application_id: application id
           :rtype: object
           :return: Avp definition from dictionary
           """
        if application_id < 0:
            raise ValueError("application_id must be greater or equal to 0.")

        if not avp_name:
            raise ValueError("avp_name is None or empty.")

        dictionary: ElementTree = super().get_dictionary()
        query_xpath_avp: str = f"xmlns:application[@id='{application_id}']/" \
                               f"xmlns:avps/xmlns:avp[@name='{avp_name.strip()}']"

        avp_xml: Element = dictionary.find(query_xpath_avp, self._ns)

        if avp_xml is None:  # find next (recursion)
            query_xpath_extends: str = f"xmlns:application[@id='{application_id}']/[@extends]"
            attr_extends: Element = dictionary.find(query_xpath_extends, self._ns)
            if not attr_extends:
                return None

            extends_value: str = attr_extends.get("extends")
            query_xpath_next: str = f"xmlns:application/[@name='{extends_value}']"
            attr_next: Element = dictionary.find(query_xpath_next, self._ns)
            next_id: int = int(attr_next.get("id"))
            avp_dict: AvpDict = self.find_avp_by_name(next_id, avp_name)
            if avp_dict:
                return avp_dict

        avp_code: int = int(avp_xml.get("code"))
        vendor: str = avp_xml.get("vendor")
        avp_vendor_flag: bool = avp_xml.get("vendor-flag") == "must"

        #   find vendor id
        query_xpath_vendor: str = f"xmlns:vendors/xmlns:vendor[@name='{vendor}']"
        vendor_xml: Element = dictionary.find(query_xpath_vendor, self._ns)
        avp_vendor_id: int = int(vendor_xml.get("id"))

        avp_type: str = avp_xml.get("type")
        content_type: str = avp_xml.get("contenttype", "")
        avp_mandatory_flag: bool = avp_xml.get("mandatory-flag") == "must"

        enums: dict = self.__enums(avp_xml)

        return AvpDict(application_id,
                       avp_code,
                       avp_name,
                       avp_type,
                       content_type,
                       avp_vendor_id,
                       avp_vendor_flag,
                       avp_mandatory_flag,
                       enums)
