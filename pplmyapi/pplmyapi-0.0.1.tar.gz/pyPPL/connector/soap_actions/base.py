import logging
import requests
import requests.adapters
from abc import (ABC, abstractmethod, )
from datetime import datetime
import xmltodict
import json
import copy
# import xml.etree.ElementTree as ET
from lxml import etree

from pyPPL.conf import (
    SOAP_API_URL,
    SOAP_HEADERS,
    SOAP_AUTH_TOKEN_MAX_AGE,
)

class SOAPAction(ABC):
    ACTION = None
    HEADERS = None
    URL = SOAP_API_URL
    data = ''
    soap_body = None

    def __init__(self) -> None:
        
        self.HEADERS = copy.deepcopy(SOAP_HEADERS) # copy headers to avoid changing original headers in conf
        
        if self.ACTION is None:
            raise NotImplementedError('SOAPAction.ACTION must be set')
        self.HEADERS['SOAPAction'] =  f"{self.HEADERS['SOAPAction']}{self.ACTION}" # add action to SOAPAction header

    def header(self) -> None:
        """
        Make SOAP header                        
        """
        self.data += f"""<?xml version="1.0" encoding="utf-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://myapi.ppl.cz/v1" xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
        <soapenv:Header/>
        <soapenv:Body>"""
    def footer(self) -> None:
        """
        Make SOAP footer
        """
        self.data += f"""</soapenv:Body>
        </soapenv:Envelope>"""

    def make_data(self) -> str:
        """
        Make SOAP text/xml data from header, body and footer for request
        """
        self.header()
        self.make_soap_body()
        self.footer()

        # encode to XML in UTF-8 and pretty print
        data = etree.fromstring(bytes(self.data, encoding='utf-8'))
        new_xml = etree.tostring(data, xml_declaration=False, encoding="UTF-8", pretty_print=True)
        self.data = new_xml#.decode('utf-8')

        return self.data

    @abstractmethod
    def make_soap_body(self) -> str:
        """
        Make SOAP body from self.soap_body with possibly some variables embedded
        """
        raise NotImplementedError('make_soap_body must be implemented')

    @abstractmethod
    def parse_success_response(self, response: str) -> object:
        """
        Parse success response from SOAP API and return object
        """
        raise NotImplementedError('parse_response must be implemented')

    def parse_error_response(self, response: str) -> object:
        """
        Parse generic error response from SOAP API and return object

        """
        response_object = json.dumps(xmltodict.parse(response))
        return {'code': response_object['s:Fault'], 'message': response_object['s:Fault']['faultstring']}
    
    def get_body(self, response: str) -> str:
        """
        Get SOAP body from response
        """
        return response.split('<s:Body>')[1].split('</s:Body>')[0]

    def __call__(self) -> object:
        """
        Call SOAP action
        """

        if self.soap_body is None:
            raise ValueError('data must be set')
        
        self.make_data()
        logging.debug(f"")
        logging.debug(f"Calling SOAP action {self.ACTION} with data: {self.data} and headers: {self.HEADERS} and URL: {self.URL}")
        logging.debug(f"")
        # print(self.data)
        response = requests.post(
            self.URL,
            data=self.data,
            headers=self.HEADERS,
            timeout=10,
        )
        # print(response.request.headers)
        if response.status_code != 200:
            # raise Exception(f"SOAP API returned status code {response.status_code}")
            logging.error(f"SOAP API returned status code {response.status_code}")
            logging.error(f"SOAP API returned content {response.text}")
            response_body = self.parse_error_response(
                self.get_body(response.text)
            )
            logging.error(f"JSON response body: {response_body}")
            return response_body

        logging.debug(f"SOAP response: {response.text}")
        response_body = self.parse_success_response(
            self.get_body(response.text)
        )
        logging.debug(f"JSON response body: {response_body}")
        return response_body
