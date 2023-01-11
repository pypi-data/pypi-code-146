"""Python wrapper for the QuickBase JSON API.
For detailed API information, see:
https://developer.quickbase.com/
"""
import traceback
from typing import Any, Dict, List
import xml.etree.ElementTree as ET
try:
    import requests
except ImportError:
    print("You must install requests before using this package.")

from requests.exceptions import ConnectionError

import time

from requests.packages import urllib3 as urllib3

urllib3.disable_warnings()


class QBError(Exception):
    """A QuickBase API error. Negative error codes are non-QuickBase codes internal to
    this module. For the list of QuickBase error codes, see:
    https://developer.quickbase.com/errors
    """

    def __init__(self, code, msg, response=None):
        self.args = (code, msg)
        self.code = code
        self.msg = msg
        self.response = response


class ConnectionError(QBError):
    pass


class ResponseError(QBError):
    pass


class QuickBaseError(QBError):
    pass


class MissingValueException(Exception):
    """Exception raised when a value is missing from an API call. Define custome message if needed."""

    def __init__(self, message="Missing value"):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class Client(object):
    """Client to the QuickBase API."""

    def __init__(self, username=None, base_url='https://www.quickbase.com',
                 timeout=90, database=None, realmhost=None, user_token=None):
        """Initialize a Client with user_token rather than username and password.
        """
        self.username = username

        self.base_url = base_url
        self.timeout = timeout
        self.database = database
        self.user_token = user_token
        self.realmhost = realmhost

        self.headers = {
            'QB-Realm-Hostname': self.realmhost,
            'Content-Type': 'application/json',
        }

        if user_token is not None:
            self.headers.update(
                {'Authorization': f'QB-USER-TOKEN {user_token}'})
        else:
            print("In order to use this SDK, you must provide a Quickbase user token.")

    def request(self, action, database, data):
        """Do a QuickBase request and return the parsed JSON response. Raises appropriate
        Error subclass on HTTP, response or QuickBase error. If fields list given,
        return dict with all fields in list (raises ResponseError if any not present),
        otherwise return parsed JSON Element.
        """

        if action == "query":
            url = "https://api.quickbase.com/v1/records/query"

        if action == "add" or action == "edit":
            url = "https://api.quickbase.com/v1/records"

        tries = 0
        while True:
            try:

                response = requests.post(
                    url, json={"to": database,
                               "data": data}, headers=self.headers, timeout=None)

                break
            except ConnectionError as e:

                if tries > 10:
                    raise

                print("re-trying request connection")
                time.sleep(1)
                tries += 1

                pass

        return response

    def denest(self, data):
        """
        Converts data from {'fid': {'value': actual_value}} format. -> {'fid': actual_value}
        credit: https://github.com/robswc/quickbase-json-api-client
        """

        if type(data) is list:
            for record in data:
                for key, value in record.items():
                    record.update({key: value.get('value')})
        return data

    def nest(self, data):
        """
        Converts data from {'fid': actual_value} format. -> {'fid': {'value': actual_value}}
        credit: https://github.com/robswc/quickbase-json-api-client
        """

        if type(data) is list:
            for record in data:
                for key, value in record.items():
                    record.update({key: {'value': value}})

        return data

    def get_schema(self, database=None, include_permissions=False):
        """
        Returns the schema from the given table
        if include_permissions=True, field permissions will be returned in the response
        """

        params = {
            'tableId': database,
            'includeFieldPerms': include_permissions
        }

        tries = 0
        while True:
            try:

                response = requests.get(
                    'https://api.quickbase.com/v1/fields',
                    params=params,
                    headers=self.headers
                )
                break
            except ConnectionError as e:

                if tries > 10:
                    raise

                print("re-trying request connection")
                time.sleep(1)
                tries += 1

                pass

        return response.json()

    def get_primary_key(self, database=None):
        """Returns the primary key of a given table"""
        schema = self.get_schema(database)

        for record in schema:
            if record['properties']['primaryKey']:
                return record['id']

    def fix_nums(self, data):
        """replaces all values that are NoneTypes to 0"""
        for record in data:
            for field, value in record.items():
                if value['value'] == None:
                    record[field] = {'value': 0}
        return data

    def round_ints(self, data):
        """takes a list of record dicts(nested) and checks for any numbers that may have an unnecessary decimal,
        then returns the data"""
        for record in data:
            for field, value in record.items():
                if type(value['value']) in [int, float] and int(value['value']) - value['value'] == 0:
                    record[field] = {'value': int(value['value'])}
        return data

    def get_sort_list(self, fids, ascending):
        if ascending:
            order = 'ASC'
        else:
            order = 'DESC'

        if fids:
            return [{'fieldId': fid, 'order': order} for fid in fids]
        else:
            return []

    def do_query(self, query=None, qid=None, columns=None, sort=[3],
                 num=None, skip=None, ascending=True,
                 database=None, round_ints=False, require_all=False):
        """Perform query and return results (list of dicts)."""

        if len([q for q in (query, qid) if q]) != 1:
            raise TypeError('must specify one of query, qid')
        # regular query
        if query:
            try:
                body = {
                    "from": database,
                    "select": [
                        column for column in (columns or [])
                    ],
                    "where": query,
                    "sortBy": self.get_sort_list(sort, ascending)
                }

                data = self.get_data(body, require_all=require_all, skip=skip, top=num)

                if round_ints:
                    data = self.round_ints(data)

                return self.denest(data)
            except Exception as e:
                print(f"Error during query: {traceback.format_exc()}")

        # run a report, keep report columns
        if qid and columns is None:
            try:
                url = f"https://api.quickbase.com/v1/reports/{qid}/run"

                data = self.get_data(url=url, database=database, require_all=require_all, 
                                     skip=skip, top=num, report=True)

                if round_ints:
                    data = self.round_ints(data)

                return self.denest(data)

            except Exception as e:
                print(traceback.format_exc())

        # run a report with custom columns
        elif qid and columns:
            try:
                url = f"https://api.quickbase.com/v1/reports/{qid}"
                params = {
                    'tableId': database,
                }
                response = requests.get(
                    url,
                    params=params,
                    headers=self.headers)
                response = response.json()

                fields = columns
                where = response['query']['filter']
                sortBy = response['query']['sortBy']
                groupBy = response['query']['groupBy']

                body = {
                    "from": database,
                    "select": fields,
                    "where": where,
                    "sortBy": list(sortBy) if sortBy else [],

                }

                if groupBy:
                    body.update({"groupBy": groupBy})

                data = self.get_data(body, require_all=require_all, skip=skip, top=num)

                if round_ints:
                    data = self.round_ints(data)

                return self.denest(data)


            except Exception as e:
                print(traceback.format_exc())

    def get_data(self, body=None, url=None, database=None, 
                 require_all=False, skip=None, top=None, report=False):
        '''
        Intermediate function to separate parsing logic from do_query
        Calls one of the api functions run_report or perform_query,
        then returns the data after parsing. 
        Will loop through multiple api calls for a single query if 
        the response does not contain all records and require_all is True
        '''
        # default offset and goal are set to skip and top
        offset = skip if skip else 0
        goal = top if top else 0

        # get response
        if report:
            response = self.run_report(url, database=database, skip=offset, top=top)
        else:
            
            body.update({'options': {
                'skip': offset,
                'top': goal
            }})

            response = self.perform_query(body=body)

        # get the number of records received and the total number
        metadata = response.get('metadata', {})
        num_records = metadata.get('numRecords', 0)
        total_records = metadata.get('totalRecords', 0)
        
        # if goal is not already zero and not greater than the possible number of records, 
        # subtract the received records from the goal
        if goal and goal <= total_records - offset:
            goal -= num_records
        # otherwise reset goal as total records - received records - skipped records
        else:
            goal = total_records - num_records - offset
        
        # add received records to offset number so they get skipped later
        offset += num_records

        # set data to received records
        data = self.fix_nums(response.get('data'))

        # if all records are required:
        if require_all:
            # loop until goal reaches 0
            while goal > 0:
                # get response
                if report:
                    response = self.run_report(url, database=database, skip=offset, top=goal)
                else:
                    
                    body.update({'options': {
                        'skip': offset,
                        'top': goal
                    }})

                    response = self.perform_query(body=body)

                # get number of received records
                metadata = response.get('metadata', {})
                num_records = metadata.get('numRecords', 0)

                # add received records to offset so they're skipped in following queries
                # and subtract received records so that the goal approaches 0
                offset += num_records
                goal -= num_records

                # add received records to data
                data.extend(self.fix_nums(response.get('data')))

        return data

    def run_report(self, url=None, database=None, skip=None, top=None):
        """Uses the QB endpoint to actually get resulting report data from QB"""
        response = requests.post(url, params={
            'tableId': database,
            'skip': skip,
            'top': top
        }, headers=self.headers)

        return response.json()

    def perform_query(self, body=None):

        response = requests.post(
            'https://api.quickbase.com/v1/records/query',
            headers=self.headers,
            json=body
        )

        return response.json()

    def add_record(self, fields, database=None, uploads=None, safemode=False):
        """
        Adds record(s) to quickbase database.
        :param fields: key, value dict, i.e. {'19': 'value'}
        :param database: quickbase table
        :param uploads: list of dicts: {fid: {"value" : { "fileName": filename, "data": base64encoded_file_content }}
        :param safemode: if safemode=True, will not add record if keyfield is one of the field parameters
        :returns rid of the created record
        """

        # if safemode is true, check if keyfield has been passed in as parameter
        if safemode:
            primarykey = self.get_primary_key(
                database=database or self.database)
            keylist = list(fields.keys())
            for key in keylist:
                if int(key) == int(primarykey):
                    raise QBError(
                        msg=f'One of the fields in the record you are trying to add is a key field, FID: {primarykey}',
                        code=-1)

        # create record object to be passed to request method
        record = {}

        # add fields and field values to record
        for field, value in fields.items():
            record.update({field: {"value": value}})
        # add uploads to record
        if uploads:
            for upload in uploads:
                record.update({upload['field']: {
                    "value": {"fileName": upload['filename'], "data": upload['value']}}})

        # upload record via request, store response to return
        response = self.request(
            action='add', database=database or self.database, data=[record])

        # convert the response to a json object
        response = response.json()

        try:

            # raise error if more than one record created
            if len(response["metadata"]["createdRecordIds"]) > 1:
                raise QBError(
                    msg=f'More than one record was created. Something went wrong. Review records: {response["metadata"]["createdRecordIds"]}',
                    code=-2)

                # should only be one

            # raise error if a record was edited and not created
            elif len(response["metadata"]['updatedRecordIds']) > 0:
                raise QBError(
                    msg=f'A record was edited, not created.. Review records: {response["metadata"]["updatedRecordIds"]}',
                    code=-4)

            # return the RID of the created record
            return response["metadata"]["createdRecordIds"][0]

        # catchall error
        except Exception as e:
            raise QBError(

                msg=f"Error creating records. Response: {response}",
                code=-3)

    def upload_file(self, rid, upload, database=None):
        """Uploads a file to QB with a given RID
        file should be b64 encoded string
        upload should be in the format:
        upload = {'filename': 'test.txt',
            'value': encoded_string, 'field': '30'}
        returns the response from QB
        """
        record = {}

        # builds record object for upload
        record.update({
            3: {"value": rid},
            upload['field']:
                {"value": {"fileName": upload['filename'],
                           "data": upload['value']
                           }
                 }
        })

        # uploads file via the response function
        response = self.request(
            action="edit", database=database or self.database, data=[record])

        # return the response from the request
        return response

    def delete_record(self, database, record):
        """
        deletes record from the specified table based on its id
        params:
        database: table id
        record: record id
        """

        headers = self.headers

        body = {
            'from': database,
            'where': "{3.EX.%s}" % record
        }
        url = 'https://api.quickbase.com/v1/records'

        print('performing call')
        response = requests.delete(url, headers=headers, json=body)
        return response

    def purge_records(self, database, query=None, rids: List = None):
        """
        deletes records in a table based on either a query or a list of record ids
        if both a query and a list are given, the list takes precedence
        response will have a 400 status if neither are given
        params:
        database: table id
        optional params(at least one is required):
        query: quickbase query, e.g. '{3.EX.450}'
        rids: list of integer record ids to search
        """

        headers = self.headers

        url = 'https://api.quickbase.com/v1/records'

        records = ""
        if rids:
            "OR".join(["{3.EX.%s}" % rid for rid in rids])
        elif query:
            records = query
        else:
            raise MissingValueException(
                message="Must provide values to delete, either with query or list of record ids.")

        body = {
            'from': database,
            'where': records
        }

        response = requests.delete(url, headers=headers, json=body)

        res_json = response.json()

        return res_json.get("numberDeleted")

    def get_file(self, url=None, database=None, record=None, field=None, version=1):
        """
        fetches a file from a record
        params:
        url: can just provide complete file url -or-
        database: table id
        record: record id
        field: field id
        the latter will be used to create url
        optional params:
        version: version of the file attachment(in case the file has been replaced), defaults to version 1

        **Important, json endpoint returns base64 encoded file, will need to b64 decode the bytes

        """

        headers = self.headers

        if not url:

            url = f"https://api.quickbase.com/v1/files/{database}/{record}/{field}/{version}"

        else:
            url = f"https://api.quickbase.com/v1{url}"

        response = requests.get(url=url, headers=headers)
        return response, response.content

    def import_from_csv(self, database, csv_str, clist):
        """
        parses records from a csv string and formats them to be passed into add_multiple_records
        params:
        database: table id
        csv_str: list of records separated by newlines, with fields separated by commas, in str
        clist: list of integers representing field ids of desired fields, should be in order corresponding to the data for each record in csv_str
        """
        # parses a csv record and sends it to add_multiple_records

        # splits the csv_str at line breaks
        csv = csv_str.splitlines()

        data = []
        record = {}
        # iterates through each record, then iterates through each piece of field data
        # and assigns them to the corresponding field id from clist
        # after iterating through each record, the data list will be formatted in the way add_multiple_records requires
        try:
            for recordData in csv:
                for fieldkey, field in enumerate(recordData.split(',')):
                    record[f'{clist[fieldkey]}'] = {'value': field}

                if len(record) != len(clist):
                    raise IndexError

                data.append(record)
                record = {}
        except IndexError:
            print("csv string or clist is invalid")
        try:
            response = self.add_multiple_records(database=database, data=data)
        except IndexError:
            response = False
        return response

    def add_multiple_records(self, database, data, return_fields=None, round_ints=False, safemode=False):
        """
        takes records in the following format and uploads to the specified table:
        [
            {
                'fid': {
                    'value':'value'
                },
                'fid': {
                    'value':'value'
                },
                'fid': {
                    'value':'value'
                }
            }
        ]
        params:
        database: table id
        data: list of record data formatted like above
        (optional) return_fields: list of integer field ids to return in response
        """

        # if the first field in the first record is not a dictionary, or it is a dictionary but does not contain a 'value' key, nest all values
        first_field = list(data[0].values())[0]
        if type(first_field) != dict or (type(first_field) == dict and 'value' not in first_field):
            data = self.nest(data)

        # if safemode is true, check if keyfield has been passed in as parameter
        if safemode:
            primarykey = self.get_primary_key(
                database=database or self.database)
            for record in data:
                for fid in record.keys():
                    if int(fid) == int(primarykey):
                        raise QBError(
                            msg=f'One of the fields in the record you are trying to add is a key field, FID: {primarykey}',
                            code=-1)

        headers = self.headers

        body = {
            'to': database,
            'data': data,
            'fieldsToReturn': return_fields
        }

        url = 'https://api.quickbase.com/v1/records'

        response = requests.post(url=url, headers=headers, json=body)
        response = response.json()

        if round_ints:
            response['data'] = self.round_ints(response['data'])
        return response

    def edit_multiple_records(self, database, data, return_fields=None, round_ints=False):
        """
        You must include the key field in the data, otherwise you will receive an error.
        takes records in the following format and uploads to the specified table:
        [
            {
                'fid': {
                    'value':'value'
                },
                'fid': {
                    'value':'value'
                },
                'fid': {
                    'value':'value'
                }
            }
        ]
        params:
        database: table id
        data: list of record data formatted like above
        (optional) return_fields: list of integer field ids to return in response

        """

        # get the table's primary key
        primary_key = self.get_primary_key(
            database=database or self.database)

        # return an error if any record is missing its primary key
        for record in data:
            if str(primary_key) not in record:
                raise QBError(
                    code=-5,
                    msg=f'One or more records is missing a primary key. Review your data. Primary key FID: {primary_key}, Raised by record: {record}'
                )

        # if the first field in the first record is not a dictionary, or it is a dictionary but does not contain a 'value' key, nest all values
        first_field = list(data[0].values())[0]
        if type(first_field) != dict or (type(first_field) == dict and 'value' not in first_field):
            data = self.nest(data)

        headers = self.headers

        body = {
            'to': database,
            'data': data,
            'fieldsToReturn': return_fields
        }

        url = 'https://api.quickbase.com/v1/records'

        response = requests.post(url=url, headers=headers, json=body)
        response = response.json()

        if round_ints:
            response['data'] = self.round_ints(response['data'])

        # raise an error if a record was created, as of now, this only seems to occur when the key field has an invalid value
        if len(response['metadata']['createdRecordIds']) > 0:
            raise QBError(
                code=-6,
                msg=f"A record was created instead of updated. Review your data and review the created record(s): {response['metadata']['createdRecordIds']}"
            )

        return response

    def edit_record(self, rid=None, key=None, fields=None, database=None, uploads=None):
        """
        Edit a record by providing rid of record, and other necessary data
        If both a key and a rid are provided, key will be prioritized
        The primary key fid is where either value would get pushed
        :param rid: record ID of the desired record required if no key is provided
        :param key: value of the primary key field, required if no rid is provided
        :param fields: key, value dict, i.e. {'19': 'value'}
        :param database: quickbase table
        :param uploads: list of dicts: {fid: {"value" : { "fileName": filename, "data": base64encoded_file_content }}
        :returns rid of the edited record
        """
        if fields is None:
            raise MissingValueException(
                message="Must provide a value to the fields param to edit record.")

        if key is None and rid is None:
            raise MissingValueException(
                message="Must provide a value to the key param or rid param to edit record.")

        else:

            # get the table's primary key
            primary_key = self.get_primary_key(
                database=database or self.database)
            # create record object to be passed to request method
            record = {
                f'{primary_key}': {"value": key if key else rid}
            }

            # add fields and field values to record
            for field, value in fields.items():
                record.update({field: {"value": value}})
            # add uploads to record
            if uploads:
                for upload in uploads:
                    record.update({upload['field']: {
                        "value": {"fileName": upload['filename'], "data": upload['value']}}})

            # upload record via request, store response to return
            response = self.request(
                action='edit', database=database or self.database, data=[record])

            # convert the response to a json object
            response = response.json()

            try:

                # raise error if more than one record created
                if len(response["metadata"]['updatedRecordIds']) > 1:
                    raise QBError(
                        msg=f'More than one record was modified. Something went wrong. Review records: {response["metadata"]["createdRecordIds"]}',
                        code=-2)

                    # should only be one

                # return the RID of the created record
                try:
                    return response["metadata"]["updatedRecordIds"][0]
                except IndexError:
                    return response["metadata"]["unchangedRecordIds"][0]

            # catchall error
            except Exception as e:
                raise QBError(

                    msg=f"Error editing records. Response: {response}",
                    code=-3)

    def change_record_owner(self, rid, database, new_owner):
        """Change record owner
        :param rid - required, the record being modified
        :param database - the table id where record is being edited
        :param new_owner - provided as email value of user in Quickbase realm
        Documentation:
        https://help.quickbase.com/api-guide/change_record_owner.html#URL_Alternative
        """
        if not rid:
            raise MissingValueException(
                message="A record id is needed to mofidy a record!")

        url = f"https://{self.realmhost}/db/{database}?a=API_ChangeRecordOwner&rid={rid}&newowner={new_owner}&usertoken={self.user_token}"

        response = requests.get(url)
        # read xml response
        root = ET.fromstring(response.text)

        error_code = root.find('errcode')

        if error_code.text != "0":
            error_text = root.find('errtext')
            error_text = error_text.text if error_text is not None else '[no error text]'
            return f"Quickbase error: {error_text}"

        return "Successfully changed record owner."
