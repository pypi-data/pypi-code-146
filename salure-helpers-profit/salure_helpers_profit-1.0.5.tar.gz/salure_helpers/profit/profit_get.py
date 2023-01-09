import base64
import json
import time
from urllib import parse
import requests
from salure_helpers.salureconnect import SalureConnect
from typing import Union, List


class GetConnector(SalureConnect):
    def __init__(self, label: Union[str, List], test_environment: bool = False, debug: bool = False):
        super().__init__()
        if test_environment:
            self.base_url = 'resttest.afas.online'
        else:
            self.base_url = 'rest.afas.online'
        credentials = self.get_system_credential(system='profit', label=label, test_environment=test_environment)
        self.environment = credentials['environment']
        base64token = base64.b64encode(credentials['token'].encode('utf-8')).decode()
        self.headers = {'Authorization': 'AfasToken ' + base64token}
        self.debug = debug

    def get_metadata(self, connector: str = None):
        url = f"https://{self.environment}.{self.base_url}/profitrestservices/metainfo{f'/get/{connector}' if connector is not None else ''}"
        vResponse = requests.get(url, headers=self.headers).json()[f"{'getConnectors' if connector is None else 'fields'}"]

        return vResponse

    def get_data(self, connector, fields=None, values=None, operators=None, orderbyfields=None):
        """
        Possible filter operators are:
        1: is gelijk aan
        2: is groter of gelijk aan
        3: is kleiner of gelijk aan
        4: is groter dan
        5: is kleiner dan
        6: tekst komt voor in veld	                                Plaats de filterwaarde tussen %..%, bijvoorbeeld %Microsoft%
        7: is niet gelijk aan / Tekst komt niet voor in veld	    Plaats de filterwaarde tussen %..%, bijvoorbeeld %Microsoft%
        8: veld is leeg	                                            Geef filterfieldid, filtervalue en operatortype op. De waarde bij filtervalue is altijd null
        9: veld is niet leeg	                                    Geef filterfieldid, filtervalue en operatortype op
        10 :veld begint met tekst	                                Plaats het teken % aan het einde van de filterwaarde, bijvoorbeeld Microsoft%
        12 :veld begint niet met tekst	                            Plaats het teken % aan het einde van de filterwaarde, bijvoorbeeld Microsoft%
        13 :veld eindigt met tekst	                                Plaats het teken % aan het begin van de filterwaarde, bijvoorbeeld %Microsoft
        14 :veld eindigt niet met tekst	                            Plaats het teken % aan het begin van de filterwaarde, bijvoorbeeld %MiMicrosoft

        If you use a skip and take, highly recommended to specify orderbyfields. This makes the requests much faster.
        You should use unique fields or combinations of most unique fields in the dataset

        Using ';' between filters is OR, ',' is AND
        """

        total_response = []
        loop_boolean = True
        no_of_loops = 0
        no_of_results = 0

        if fields is not None:
            parameters = {"filterfieldids": fields, "filtervalues": values, "operatortypes": operators}
        else:
            parameters = {}

        if orderbyfields is not None:
            parameters["orderbyfieldids"] = "-{}".format(orderbyfields)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, connector)

        while loop_boolean:
            loop_parameters = {"skip": 40000 * no_of_loops, "take": 40000}
            parameters.update(loop_parameters)
            response = requests.get(url.encode("utf-8"), parameters, headers=self.headers, timeout=30000)
            if response.status_code == 200:
                response_json = response.json()['rows']
                no_of_loops += 1
                no_of_results += len(response_json)
                loop_boolean = True if len(response_json) == 40000 else False

                if self.debug:
                    print(time.strftime('%H:%M:%S'), 'Got next connector from profit: ', connector, ' With nr of rows: ', no_of_results)
                total_response += response_json
            else:
                return response.text

        return total_response

    def get_complex_filtered_data(self, connector: str, fields: list, values: list, operators: list, orderbyfields: str = None):
        """
        This method is meant for complex combined filters like (a and b) or (a and c)

        Possible filter operators are:
        1: is gelijk aan
        2: is groter of gelijk aan
        3: is kleiner of gelijk aan
        4: is groter dan
        5: is kleiner dan
        6: tekst komt voor in veld	                                Plaats de filterwaarde tussen %..%, bijvoorbeeld %Microsoft%
        7: is niet gelijk aan / Tekst komt niet voor in veld	    Plaats de filterwaarde tussen %..%, bijvoorbeeld %Microsoft%
        8: veld is leeg	                                            Geef filterfieldid, filtervalue en operatortype op. De waarde bij filtervalue is altijd null
        9: veld is niet leeg	                                    Geef filterfieldid, filtervalue en operatortype op
        10 :veld begint met tekst	                                Plaats het teken % aan het einde van de filterwaarde, bijvoorbeeld Microsoft%
        12 :veld begint niet met tekst	                            Plaats het teken % aan het einde van de filterwaarde, bijvoorbeeld Microsoft%
        13 :veld eindigt met tekst	                                Plaats het teken % aan het begin van de filterwaarde, bijvoorbeeld %Microsoft
        14 :veld eindigt niet met tekst	                            Plaats het teken % aan het begin van de filterwaarde, bijvoorbeeld %MiMicrosoft

        If you use a skip and take, highly recommended to specify orderbyfields. This makes the requests much faster.
        You should use unique fields or combinations of most unique fields in the dataset

        Using ';' between filters is OR, ',' is AND
        :param connector: name of connector
        :param fields: list of filters. each listitem is one filterblock. example: ['naam, woonplaats', 'achternaam, einddatum']
        :param values: list of filters. each listitem corresponds to one filterblock. example: ['Jan, Gouda', 'Janssen, 2019-01-01T00:00']
        :param operators: list of filters. each listitem corresponds to one filterblock. example: ['1, 1', '1, 3']
        :param orderbyfields: string of fields to order result by
        :return: data in json format
        """

        total_response = []
        loop_boolean = True
        no_of_loops = 0
        no_of_results = 0

        parameters = {"Filters": {"Filter": []}}

        for filter_no in range(0, len(fields)):
            filter = {"@FilterId": 'Filter {}'.format(filter_no + 1), "Field": []}
            fields_values = fields[filter_no].split(',')
            operators_values = operators[filter_no].split(',')
            values_values = values[filter_no].split(',')
            for number in range(0, len(fields_values)):
                filter["Field"].append({"@FieldId": fields_values[number],
                                        "@OperatorType": operators_values[number],
                                        "#text": values_values[number]})
            parameters['Filters']['Filter'].append(filter)

        url = 'https://{}.{}/profitrestservices/connectors/{}'.format(self.environment, self.base_url, connector)
        # Dit stukje hieronder heeft JJ een paar uur van zn leven gekost. Do not touch
        querystring = parse.quote(json.dumps(parameters, separators=(',', ':')))
        if orderbyfields is not None:
            querystring = querystring + '&orderbyfieldids={}'.format(orderbyfields)

        while loop_boolean:
            loop_parameters = "&skip={}&take={}".format(40000 * no_of_loops, 40000)
            response = requests.get(url, data='', headers=self.headers, timeout=30000, params="filterjson={}{}".format(querystring, loop_parameters))
            if response.status_code == 200:
                response_json = response.json()['rows']
                no_of_loops += 1
                no_of_results += len(response_json)
                loop_boolean = True if len(response_json) == 40000 else False

                if self.debug:
                    print(time.strftime('%H:%M:%S'), 'Got next connector from profit: ', connector, ' With nr of rows: ', no_of_results)
                total_response += response_json
            else:
                return response.text

        return total_response

    def get_dossier_attachments(self, dossieritem_id, dossieritem_guid) -> requests.Response:
        """
        This method returns base64encoded binary data in the filedata key of the json response. You can process this by decoding it and writing it to a file using:
        blob = base64.b64decode(response.json()['filedata'])
        with open('{}/{}'.format(self.file_directory, filename), 'wb') as f:
            f.write(blob)
        :param dossieritem_id: dossieritem_id
        :param dossieritem_guid: dossieritem_guid
        :return: response object
        """
        url = f"https://{self.environment}.{self.base_url}/profitrestservices/subjectconnector/{dossieritem_id}/{dossieritem_guid}"
        response = requests.get(url=url, headers=self.headers)

        return response



