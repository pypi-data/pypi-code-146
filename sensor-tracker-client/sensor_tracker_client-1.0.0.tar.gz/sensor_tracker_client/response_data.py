import json
import requests
import csv
from .exceptions import ServerIssue


class Datum:
    def __init__(self, raw_data, status_code):
        self.raw = raw_data
        self.status_code = status_code


class ResponseData:
    def __init__(self):
        self._raw = []
        self.pages = False

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, value):
        self._raw.append(value)

    @property
    def dict(self):
        if not hasattr(self, "_dict"):
            if self.pages:
                self._dict = []
                for a in self.raw:
                    status_code, data = a
                    if status_code == 200:
                        self._dict.extend(data["results"])
            else:
                self._dict = []
                for a in self.raw:
                    status_code, data = a
                    if status_code == 200:
                        self._dict.append(data)
        return self._dict

    @property
    def json(self):
        return json.dumps(self.dict)

    def to_csv(self, output_file_path):
        with open(output_file_path, 'w') as f:
            csvwriter = csv.writer(f)
            if self.dict:
                csvwriter.writerow(self.dict[0].keys())
                for x in self.dict:
                    csvwriter.writerow(x.values())

    def to_json(self, output_file_path):
        with open(output_file_path, 'w') as f:
            f.write(self.json)


class DataFactory:
    def __init__(self, response):
        self.response = response

    def generate(self):
        new_data = ResponseData()
        try:
            response_json = self.response.json()
        except ValueError as e:
            msg = "status code: {}\nreturn content: {}\nUnable able decode return data: {}".format(self.response.status_code,
                                                                                        self.response.raw.data, e)
            raise ServerIssue(msg)
        except Exception as e:
            msg = "status code: {}\nurl {}\nexception content: {}".format(self.response.status_code, self.response.url,
                                                                           e)
            raise ServerIssue(msg)
        new_data.raw = (self.response.status_code, response_json)

        if "next" in response_json:
            new_data.pages = True
            the_next = response_json["next"]
            if the_next:
                self._generate(the_next, new_data)
        elif len(response_json) == 1 and "detail" in response_json:
            raise AttributeError(response_json)
        elif len(response_json):
            new_data.pages = False
        else:
            msg = "api error {}".format(response_json)
            raise AttributeError(msg)

        return new_data

    def _generate(self, url, data_obj):
        response = requests.get(url)
        response_json = response.json()
        data_obj.raw = (self.response.status_code, response_json)
        if response_json["next"]:
            self._generate(response_json["next"], data_obj)
        return data_obj
