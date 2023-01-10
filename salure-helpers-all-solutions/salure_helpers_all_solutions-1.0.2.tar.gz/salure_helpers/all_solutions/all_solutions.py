import hashlib
import json
from typing import List, Union
import requests
from salure_helpers.salureconnect import SalureConnect


class AllSolutions(SalureConnect):
    def __init__(self, label: Union[str, List]):
        super().__init__()
        self.token = None
        self.refresh_token = None
        self.debug = False
        credentials = self.get_system_credential(system='all-solutions', label=label)
        self.url = credentials['url']
        self.client_id = credentials['client_id']
        self.secret_id = credentials['secret_id']
        self.username = credentials['username']
        self.password = credentials['password']
        self.content_type_header = {'Content-Type': 'application/json'}

    def _get_refreshtoken(self):
        signature = hashlib.sha1(f"{self.username}{self.client_id}{self.secret_id}".encode()).hexdigest()
        response = requests.post(url=f"{self.url}login",
                                 headers=self.content_type_header,
                                 data=json.dumps({
                                     "Username": self.username,
                                     "Signature": signature,
                                     "Password": self.password,
                                     "ClientId": self.client_id
                                 }))
        if self.debug:
            print(response.content)
        response.raise_for_status()
        self.token = response.json()['Token']
        self.refresh_token = response.json()['RefreshToken']

    def _get_token(self):
        signature = hashlib.sha1(f"{self.refresh_token}{self.secret_id}".encode()).hexdigest()
        response = requests.post(url=f"{self.url}refreshtoken",
                                 headers=self.content_type_header,
                                 data=json.dumps({
                                     "RefreshToken": self.refresh_token,
                                     "Signature": signature
                                 }))
        if self.debug:
            print(response.content)
        response.raise_for_status()
        self.token = response.json()['Token']
        self.refresh_token = response.json()['RefreshToken']

    def _get_headers(self):
        if self.token is None:
            self._get_refreshtoken()
        else:
            self._get_token()
        headers = {**self.content_type_header, **{'Authorization': f'{self.token}'}}

        return headers

    def get_employees(self, filter: str = None):
        self._get_headers()
        total_response = []
        more_results = True
        params = {"pageSize": 500}
        params.update({"$filter-freeform": filter}) if filter else None
        while more_results:
            response = requests.get(url=f"{self.url}mperso",
                                    headers=self._get_headers(),
                                    params=params)
            if self.debug:
                print(response.content)
            response.raise_for_status()
            more_results = response.json()['Paging']['More']
            params['cursor'] = response.json()['Paging']['NextCursor']
            total_response += response.json()['Data']

        return total_response

    def get_persons(self, filter: str = None):
        total_response = []
        more_results = True
        params = {"pageSize": 500}
        params.update({"$filter-freeform": filter}) if filter else None
        while more_results:
            response = requests.get(url=f"{self.url}mrlprs",
                                    headers=self._get_headers(),
                                    params=params)
            if self.debug:
                print(response.content)
            response.raise_for_status()
            more_results = response.json()['Paging']['More']
            params['cursor'] = response.json()['Paging']['NextCursor']
            total_response += response.json()['Data']

        return total_response

    def create_employee(self, data: dict) -> json:
        """
        Create a new employee in All Solutions
        :param data: all the fields that are required to create a new employee
        :return: response json
        """
        required_fields = ["employee_code", "employee_id_afas", "date_in_service", "termination_date", "email_work", "phone_work", "mobile_phone_work", "costcenter",
                           "function"]
        allowed_fields = {
            "note": "ab02.notitie-edit",
            "birth_date": "ab02.geb-dat",
            "email_private": "ab02.email"
        }
        self.__check_fields(data=data, required_fields=required_fields)

        payload = {
            "Data": [
                {
                    "ab02.persnr": data['employee_code'],
                    "ab02.mail-nr": data['employee_id_afas'],
                    "h-default7": True,
                    "h-default6": True,  # Find corresponding employee details
                    "h-default5": True,  # Find name automatically
                    "h-default1": True,  # check NAW automatically from person
                    "h-corr-adres": True,  # save address as correspondence address
                    # "h-aanw": "32,00", # hours per week
                    "ab02.indat": data['date_in_service'],
                    "ab02.uitdat": data['termination_date'],
                    "ab02.email-int": data['email_work'],
                    "ab02.telefoon-int": data['phone_work'],
                    "ab02.mobiel-int": data['mobile_phone_work'],
                    "ab02.ba-kd": data['costcenter'],
                    "ab02.funktie": data['function'],
                    "ab02.contr-srt-kd": "1",
                    "ab02.srt-mdw": "ms01"
                }
            ]
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            payload['Data'][0].update({allowed_fields[field]: data[field]})

        if self.debug:
            print(json.dumps(payload))
        response = requests.post(url=f"{self.url}mperso",
                                 headers=self._get_headers(),
                                 data=json.dumps(payload))
        if self.debug:
            print(response.content)
        response.raise_for_status()

        return response.json()

    def update_employee(self, data: dict) -> json:
        """
        Update an existing employee in All Solutions
        :param data: data to update
        :return:
        """
        required_fields = ['employee_id']
        allowed_fields = {
            'employee_code': 'ab02.persnr',
            'birth_date': 'ab02.geb-dat',
            'employee_id_afas': 'ab02.mail-nr',
            'date_in_service': 'ab02.indat',
            'date_in_service_custom': 'ab02.kenmerk[62]',
            'termination_date': 'ab02.uitdat',
            'email_work': 'ab02.email-int',
            'email_private': 'ab02.email',
            'phone_work': 'ab02.telefoon-int',
            'mobile_phone_work': 'ab02.mobiel-int',
            'costcenter': 'ab02.ba-kd',
            'function': 'ab02.funktie',
            'note': "ab02.notitie-edit"
        }

        self.__check_fields(data=data, required_fields=required_fields)

        payload = {
            "Data": [
                {
                    "h-default7": True,
                    "h-default6": True,  # Find corresponding employee details
                    "h-default5": True,  # Find name automatically
                    "h-default1": True,  # check NAW automatically from person
                    "h-corr-adres": True,  # save address as correspondence address
                    # "h-aanw": "32,00", # hours per week
                    "ab02.contr-srt-kd": "1",
                    "ab02.srt-mdw": "ms01"
                }
            ]
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            payload['Data'][0].update({allowed_fields[field]: data[field]})

        if self.debug:
            print(json.dumps(payload))
        response = requests.put(url=f"{self.url}mperso/{data['employee_id']}",
                                headers=self._get_headers(),
                                data=json.dumps(payload))
        if self.debug:
            print(response.content)
        response.raise_for_status()

        return response.json()

    def create_person(self, data: dict) -> json:
        """
        Create a new person in All Solutions
        :param data: data of the person
        :return: response json
        """
        required_fields = ["search_name", "employee_id_afas", "employee_code", "birth_date", "initials", "prefix", "city", "lastname",
                           "street", "housenumber", "housenumber_addition", "postal_code"]
        allowed_fields = {
            "note": "ma01.notitie-edit",
            'firstname': "ma01.voornaam",
            'gender': "ma01.geslacht"
        }
        self.__check_fields(data=data, required_fields=required_fields)

        payload = {
            "Data": [
                {
                    "ma01.zoeknaam": data['search_name'],
                    'h-mail-nr': data['employee_id_afas'],
                    "ma01.telefoon": data['phone_private'],
                    "ma01.persnr": data['employee_code'],
                    "ma01.geb-dat": data['birth_date'],
                    "ma01.voorl": data['initials'],
                    "ma01.roepnaam": data['nickname'],
                    "ma01.voor[1]": data['prefix'],
                    "ma01.b-wpl": data['city'],
                    "ma01.persoon[1]": data['lastname'],
                    "ma01.b-adres": data['street'],
                    "ma01.b-num": data['housenumber'],
                    "ma01.b-appendix": data['housenumber_addition'],
                    "ma01.b-pttkd": data['postal_code'],
                    "ma01.mobiel": data['mobile_phone_private'],
                    "ma01.email": data['email_private'],
                    # "h-default7": True,
                    # "h-aanw": "32,00", # hours per week
                    "h-default6": True,
                    "h-default8": True,
                    "ma01.rel-grp": 'Medr',
                    "h-chk-ma01": True  # Check if person already exists
                }
            ]
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            payload['Data'][0].update({allowed_fields[field]: data[field]})

        if self.debug:
            print(json.dumps(payload))
        response = requests.post(url=f"{self.url}mrlprs",
                                 headers=self._get_headers(),
                                 data=json.dumps(payload))
        if self.debug:
            print(response.content)
        response.raise_for_status()

        return response.json()

    def update_person(self, data: dict) -> json:
        """
        Update person in all solutions
        :param data: data to update
        :return: json response
        """
        required_fields = ['person_id']
        allowed_fields = {
            "search_name": "ma01.zoeknaam",
            "employee_id_afas": "ma01.mail-nr",
            "phone_private": "ma01.telefoon",
            "employee_code": "ma01.persnr",
            "birth_date": "ma01.geb-dat",
            "initials": "ma01.voorl",
            "firstname": "ma01.voornaam",
            "nickname": "ma01.roepnaam",
            "prefix": "ma01.voor[1]",
            "city": "ma01.b-wpl",
            "lastname": "ma01.persoon[1]",
            "street": "ma01.b-adres",
            "housenumber": "ma01.b-num",
            "housenumber_addition": "ma01.b-appendix",
            "postal_code": "ma01.b-pttkd",
            "mobile_phone_private": "ma01.mobiel",
            "email_private": "ma01.email",
            "note": "ma01.notitie-edit",
            'gender': "ma01.geslacht"
        }

        self.__check_fields(data=data, required_fields=required_fields)

        payload = {
            "Data": [
                {
                    # "h-default7": True,
                    # "h-aanw": "32,00", # hours per week
                    "h-default6": True,
                    "h-default8": True,
                    "ma01.rel-grp": 'Medr'
                    # "h-chk-ma01": True  # Check if person already exists
                }
            ]
        }

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            payload['Data'][0].update({allowed_fields[field]: data[field]})

        if self.debug:
            print(json.dumps(payload))
        response = requests.put(url=f"{self.url}mrlprs/{data['person_id']}",
                                headers=self._get_headers(),
                                data=json.dumps(payload))
        if self.debug:
            print(response.content)
        response.raise_for_status()

        return response.json()

    @staticmethod
    def __check_fields(data: dict, required_fields: List):
        for field in required_fields:
            if field not in data.keys():
                raise ValueError('Field {field} is required. Required fields are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))
