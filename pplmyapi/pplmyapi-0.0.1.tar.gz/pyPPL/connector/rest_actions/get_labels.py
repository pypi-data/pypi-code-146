import logging
from time import sleep
from pyPPL.models.package import Package
from pyPPL.conf import (LabelReturnChanel, LabelSettingModel, ImportStatus, LABEL_SERVICES )
import requests
import json
import base64

class RESTActionGetLabels:
    
    url = 'https://api.dhl.com/ecs/ppl/myapi2/shipment/batch'

    def keep_or_remove_services(self, package: Package):
        svc = package.package_services

        if svc is None or len(svc) == 0:
            return
        
        new_svc = []
        for s in svc:
            # validate service code againts LABEL_SERVICES list of enum item
            if s.get_type() in LABEL_SERVICES:
                # remove service from package
                new_svc.append(s)
        package.package_services = new_svc
        return package


    def validate_package(self, package: Package):
        return self.keep_or_remove_services(package)


    def __init__(self, 
        token: str = None,
        packages: list[Package] = [], 
        return_chanel_type: LabelReturnChanel = LabelReturnChanel.HTTP,
        return_chanel_address: str = None,
        return_chanel_format: LabelSettingModel = LabelSettingModel.PDF,
        return_chanel_dpi: int = 300,
        session = None,
    ):
        self.packages = packages
        self.return_chanel_type = return_chanel_type
        self.return_chanel_address = return_chanel_address
        self.return_chanel_format = return_chanel_format
        self.return_chanel_dpi = return_chanel_dpi
        
        for package in self.packages:
            package = self.validate_package(package)

        if token is None:
            raise Exception('Token is required')

        if session is None and token is not None:
            self.session = requests.Session()
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
        else:
            self.session = session

        

        self.label_settings = {
            "format": return_chanel_format.value,
            "dpi": return_chanel_dpi,
            "completeLabelSettings": {
                "isCompleteLabelRequested": True,
                "pageSize": "A4",
                "position": 1
            }
        }
        # return chanel
        if return_chanel_type != LabelReturnChanel.HTTP:
            if not return_chanel_address:
                raise Exception('return_chanel_address is required')
            self.label_settings['returnChanel'] = {
                "type": return_chanel_type.value,
                "address": return_chanel_address,
            }

    def fetch_label_pickup_response(self, label_url):
        # method used for the first step of obtaining label status and possible URL
            response = self.session.get(label_url)
            if response.status_code != 200:
                raise Exception(f'Error while getting labels: {response.text}')
            return response.json()

    def parse_label_pickup(self, response):
        # method used for the second step of obtaining label status and possible URL
        # iterate over response and check if all labels have Complete status
        # if not, return None
        # if yes, return list of label URLs
        label_urls = None

        if 'items' in response:
            for item in response['items']:
                # check if all items have Complete status
                if item['importState'] == 'Error':
                    return None, ImportStatus.ERROR
                if item['importState'] == 'Accepted':
                    return None, ImportStatus.ACCEPTED
                if item['importState'] == 'InProcess':
                    return None, ImportStatus.INPROCESS
                if item['importState'] == 'Complete':
                    continue
        
        # looks like all items have Complete status
        
        if 'completeLabel' in response:
            if 'labelUrls' in response['completeLabel']:
                return response['completeLabel']['labelUrls'], ImportStatus.COMPLETE

        return label_urls, ImportStatus.COMPLETE
    
    def get_labels_and_status(self, location):
        label_urls = None
        label_response = None
        status = None
        
        # do this max 10 times
        count = 0
        while label_urls is None or status is ImportStatus.INPROCESS or status is ImportStatus.ACCEPTED and count < 10:
            label_response = self.fetch_label_pickup_response(location)
            label_urls, status = self.parse_label_pickup(
                label_response
            )
            logging.debug(f'Label status: {status} - {label_urls}')
            # wait 2 seconds
            if status != ImportStatus.COMPLETE or status != ImportStatus.ERROR:
                sleep(2)
            count += 1
        
        return label_urls, label_response, status

    def get_labels_from_url(self, label_urls):
        # get labels for packages - call api
        labels = []
        for label_url in label_urls:
            response = self.session.get(label_url)
            if response.status_code != 200:
                raise Exception(f'Error while getting labels: {response.text}')
            labels.append(base64.b64encode(response.content).decode('utf-8'))
        return labels

    def __call__(self):
        # POST data to the self.url
        # obtain response, get label url from response (Location header)
        # if return_chanel_type == LabelReturnChanel.HTTP:
        #   fetch label url and return base64
        # else:
        #   return response (status)

        # get labels for packages - call api

        print('packages', [package.to_json() for package in self.packages])


        response = self.session.post(
            self.url,
            json = {
                "labelSettings": self.label_settings,
                "shipments": [package.to_json() for package in self.packages],
            }
        )
        if response.status_code != 201:
            # try to get error message in response
            error = None
            try:
                error = response.json()
            except:
                raise Exception(f'Error while getting labels: {response.text}')
            
            if 'errors' in error:
                raise Exception(f'Error while getting labels: {error["errors"]}')
            else:
                raise Exception(f'Error while getting labels: {error}')

        # response was success
        # get Location from headers and fetch it
        if not 'Location' in response.headers or response.headers['Location'] == '':
            raise Exception(f'Error while getting labels: Location header not found in response')

        # wait for label to be ready
        # sleep(2)
        label_urls, label_response, status = self.get_labels_and_status(response.headers['Location'])

        if status == ImportStatus.ERROR:
            raise Exception(f'Error while getting labels: {label_response}')

        if self.return_chanel_type == LabelReturnChanel.HTTP and label_urls is not None and len(label_urls) > 0:
            # fetch label url (every url from the list) and return base64
            labels = self.get_labels_from_url(label_urls)
        else:
            return label_response

        return {'labels': labels, 'status': status}