import urllib.parse
import warnings
import requests
import json
from typing import Union, List
from salure_helpers.salureconnect import SalureConnect
import pandas as pd
import os


class Salesforce(SalureConnect):
    """
    This class is meant to be a simple wrapper around the Salesforce API. In order to start using it, authorize your application is Salureconnect.
    You will receive a code which you can use to obtain a refresh token using the get_refresh_token method. Use this refresh token to refresh your access token always before you make a data call.
    """
    def __init__(self, label: Union[str, List], debug: bool = False):
        super().__init__()
        self.credentials = self.get_system_credential(system='salesforce', label=label)
        self.credential_id = self.credentials['id']
        self.customer_url = self.credentials['auth']['instance_url']
        self.debug = debug
        self.api_version = 56.0

    def __get_headers(self) -> dict:
        credentials = self.refresh_system_credential(system='salesforce', system_id=self.credential_id)
        headers = {"Authorization": f"Bearer {credentials['access_token']}",
                   "Content-Type": "application/json"}
        if self.debug:
            print(f"Headers: {headers}")

        return headers

    def query_data(self, query: str) -> pd.DataFrame:
        """
        This method is used to send raw queries to Salesforce.
        :param query: Querystring. Something like: 'select+Name,Id+from+Account'
        :return: data or error
        """
        params = {
            "q": query
        }
        if self.debug:
            print(f"Query: {query}")
        params_str = urllib.parse.urlencode(params, safe=':+')
        df = pd.DataFrame()
        done = False
        url = f"{self.customer_url}/services/data/v37.0/query/?"
        while done is False:
            response = requests.get(url=url, params=params_str, headers=self.__get_headers())
            response.raise_for_status()
            response = response.json()
            done = response['done']
            if done is False:
                url = f"{self.customer_url}{response['nextRecordsUrl']}"
            df = pd.concat([df, pd.DataFrame(response['records'])])

        return df

    def get_data(self, fields: Union[str, List], object_name: str, filter: str = None) -> pd.DataFrame:
        """
        This method is used to send queries in a somewhat userfriendly wayt to Salesforce.
        :param fields: fields you want to get
        :param object_name: table or object name that the fields need to be retrieved from
        :param filter: statement that evaluates to True or False
        :return: data or error
        """
        fields = ",".join(fields) if isinstance(fields, List) else fields
        params = {
            "q": f"SELECT {fields} FROM {object_name}{' WHERE ' + filter if filter is not None else ''}"
        }
        if self.debug:
            print(f"Query: {params['q']}")
        params_str = urllib.parse.urlencode(params, safe=':+')
        df = pd.DataFrame()
        done = False
        url = f"{self.customer_url}/services/data/v37.0/query/?"
        while done is False:
            response = requests.get(url=url, params=params_str, headers=self.__get_headers())
            response.raise_for_status()
            response = response.json()
            done = response['done']
            if done is False:
                url = f"{self.customer_url}{response['nextRecordsUrl']}"
            df = pd.concat([df, pd.DataFrame(response['records'])])

        return df

    def create_contact(self, data: dict) -> json:
        """
        This method is used to send queries in a somewhat userfriendly wayt to Salesforce.
        :param data: fields you want to update
        :return: data or error
        """
        allowed_fields = {
            'salure_customer': 'Klant_van_Salure__c',
            # 'full_name': 'Name',
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'phone': 'Phone',
            'email': 'Email',
            'salesforce_account_id': 'AccountId',
            'organisation_person_id': 'AFAS_persoons_ID__C'
        }
        required_fields = []

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        body = {}

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            body.update({allowed_fields[field]: data[field]})

        body = json.dumps(body)
        if self.debug:
            print(f"Payload: {body}")

        response = requests.post(url=f"{self.customer_url}/services/data/v37.0/sobjects/Contact", data=body, headers=self.__get_headers())
        response.raise_for_status()
        if self.debug:
            print(f"Response: {response.content, response.text}")

        return response.json()

    def update_contact(self, data: dict):
        """
        This method is used to send queries in a somewhat userfriendly way to Salesforce.
        :param data: fields you want to update
        :return: nothing is returned when update is successful, otherwise raises error
        """
        allowed_fields = {
            'salure_customer': 'Klant_van_Salure__c',
            # 'full_name': 'Name',
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'phone': 'Phone',
            'email': 'Email',
            'salesforce_account_id': 'AccountId',
            'organisation_person_id': 'AFAS_persoons_ID__C'
        }
        required_fields = ['contact_id']

        self.__check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        body = {}

        # Add allowed fields to the body
        for field in (allowed_fields.keys() & data.keys()):
            body.update({allowed_fields[field]: data[field]})

        body = json.dumps(body)
        if self.debug:
            print(f"Payload: {body}")

        response = requests.patch(url=f"{self.customer_url}/services/data/v37.0/sobjects/Contact/{data['contact_id']}", data=body, headers=self.__get_headers())
        response.raise_for_status()
        if self.debug:
            print(f"Response: {response.content, response.text}")

    @staticmethod
    def __check_fields(data: Union[dict, List], required_fields: List, allowed_fields: List):
        if isinstance(data, dict):
            data = data.keys()

        for field in data:
            if field not in allowed_fields and field not in required_fields:
                warnings.warn('Field {field} is not implemented. Optional fields are: {allowed_fields}'.format(field=field, allowed_fields=tuple(allowed_fields)))

        for field in required_fields:
            if field not in data:
                raise ValueError('Field {field} is required. Required fields are: {required_fields}'.format(field=field, required_fields=tuple(required_fields)))

    def query_table_metadata(self, table: str) -> requests.Response:
        """
        This method is used to get the metadata of a table in Salesforce.
        :param table: table or object name that the fields need to be retrieved from
        :return: data or error
        """
        url = f"{self.customer_url}/services/data/v{self.api_version}/sobjects/{table}/describe/"
        response = requests.get(url, headers=self.__get_headers())
        return response

    def query_table(self, data_dir: str, table: str, fields: str, filter: str = '*', filename: str = None) -> pd.DataFrame:
        """
        for information about the tables, see: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_query.htm
        With this method, you give a certain table you want to retrieve data from. This function contains a list of tables that are available in this function.
        If you want to use an table that is not in this list, you can use the query_data method. In this function, there is extra information available per table like if it is
        possible to get a full or an incremental load. This function will also check your previous loaded data and add new data to the previous data. Deleted data will also be deleted from
        your dataset
        :param data_dir: directory where the data will be stored. Both the full and incremental data will be stored here
        :param table: table (it's a SQL query) you want to retrieve data from. If you call an table which is not in the approved tables, you will always get the full (not incremental) dataset.
        :param fields: fields you want to get from the table
        :param filter: possible filter you want to apply to the table
        :param filename: filename you want to use for the data. If not given, the table will be used as filename
        return: the dataset in pandas format
        """
        approved_tables = {
            'Account': 'incremental',
            'AccountHistory': 'full',
            'Appliaction__c': 'incremental',
            'Beneficiary__c': 'incremental',
            'Campaign': 'incremental',
            'CampaignMember': 'incremental',
            'Case': 'incremental',
            'Contact': 'incremental',
            'cpm__Installment__c': 'incremental',
            'cpm__Payment__c': 'incremental',
            'Document__c': 'incremental',
            'Donaction_contracts__c': 'incremental',
            'Donor_Type_Budget__c': 'incremental',
            'Dorcas_Exchange_Rates__c': 'incremental',
            'Dorcas_Report__c': 'incremental',
            'General_Ledger_Account__c': 'incremental',
            'npe03__Recurring_Donation__c': 'incremental',
            'npsp__General_Accounting_Unit__c': 'incremental',
            'Opportunity': 'incremental',
            'pmnc__Project__c': 'incremental',
            'Project_Budget__c': 'incremental',
            'Project_Budget_Line__c': 'incremental',
            'Project_Expense__c': 'incremental',
            'Project_Indicator__c': 'incremental',
            'Project_Result__c': 'incremental',
            'Reporting_Unit__c': 'incremental',
            'Result_Framework__c': 'incremental',
            'Stakeholder__c': 'incremental',
            'Volunteer_Assignment__c': 'incremental',
            'User': 'full'
        }
        if table not in approved_tables.keys():
            approved_tables[table] = 'full'

        # First create a folder for the raw feather files
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(f'{data_dir}/cache/', exist_ok=True)

        # Check if there is allready a file for the called table. If not, it's always the first and thus full load
        filename = table if filename is None else filename
        load_type = approved_tables[table]
        initial_load = False if os.path.exists(f'{data_dir}/cache/{filename}.ftr') else True

        # If it is the initial load but in the future we want to do incremental loads and there is no filter, Add the fields ID, CreatedDate and LastModifiedDate to the fields
        if initial_load and load_type == 'incremental' and filter == '*':
            params = {"q": f"SELECT+{fields},Id,CreatedDate,LastModifiedDate+FROM+{table}"}
        # If it is the initial load but in the future we want to do incremental loads and there is a filter, Add the fields ID, CreatedDate and LastModifiedDate to the fields and also apply the filter for the initial load
        elif initial_load and load_type == 'incremental' and filter != '*':
            params = {"q": f"SELECT+{fields},Id,CreatedDate,LastModifiedDate+FROM+{table}+WHERE+{filter}"}
        # If it is the initial load and in the future we want the full load also, don't add the fields CreatedDate and LastModifiedDate because most of the times, they are not available for full load tables
        elif initial_load and load_type == 'full':
            params = {"q": f"SELECT+{fields},Id+FROM+{table}"}
        # If it's an incremental load with a filter, load the records that are created or updated in the last 14 days (double records will be removed later) and apply the filter
        elif initial_load is False and load_type == 'incremental' and filter != '*':
            params = {"q": f"SELECT+{fields},Id,CreatedDate,LastModifiedDate+FROM+{table}+WHERE+LastModifiedDate+>=+LAST_N_DAYS:14+AND+{filter}"}
        # If it's an incremental load without a filter, load the records that are created or updated in the last 14 days (double records will be removed later)
        elif initial_load is False and load_type == 'incremental' and filter == '*':
            params = {"q": f"SELECT+{fields},Id,CreatedDate,LastModifiedDate+FROM+{table}+WHERE+LastModifiedDate+>=+LAST_N_DAYS:14"}
        # If it's a full load with a filter, apply the filter
        elif initial_load is False and load_type == 'full' and filter != '*':
            params = {"q": f"SELECT+{fields},Id+FROM+{table}+WHERE+{filter}"}
        # In all other cases, just load the full dataset without any filter and any field which is needed for incremental loads
        else:
            params = {"q": f"SELECT+{fields},Id+FROM+{table}"}

        params_str = urllib.parse.urlencode(params, safe=':+')
        url = f'{self.customer_url}/services/data/v{self.api_version}/query/?'
        done = False
        df = pd.DataFrame()

        # With the created URL and parameters, call the API
        while done is False:
            response = requests.get(url=url, params=params_str, headers=self.__get_headers())
            response.raise_for_status()
            done = response.json()['done']
            df_temp = pd.DataFrame(response.json()['records'])
            if 'attributes' in df_temp.columns:
                del df_temp['attributes']
            if done is False:
                url = f"{self.customer_url}{response.json()['nextRecordsUrl']}"
            df = pd.concat([df_temp, df])

        if load_type == 'incremental':
            # Now get the previously fetched data which is stored in feather files and concat it with the new data. keep only the new data in case of duplicates
            if os.path.exists(f'{data_dir}/cache/{filename}.ftr'):
                df_old = pd.read_feather(f'{data_dir}/cache/{filename}.ftr')
                df = pd.concat([df, df_old])
                df.sort_values(by=['Id', 'LastModifiedDate'], ascending=False, inplace=True)
                df = df.drop_duplicates(subset=['Id'], keep='first')

            # Get the deleted rows from the table with a new call to Salesforce. Get all the deleted records and not only recent deleted ones because very old rows can be deleted as well since the last time the data was fetched
            params = {"q": f"SELECT+Id,isDeleted+FROM+{table}+WHERE+isDeleted+=TRUE"}
            params_str = urllib.parse.urlencode(params, safe=':+')
            done = False
            df_del = pd.DataFrame()
            url = f'{self.customer_url}/services/data/v{self.api_version}/queryAll/?'
            while done is False:
                response = requests.get(url=url, params=params_str, headers=self.__get_headers())
                response.raise_for_status()
                done = response.json()['done']
                df_temp = pd.DataFrame(response.json()['records'])
                if done is False:
                    url = f"{self.customer_url}{response.json()['nextRecordsUrl']}"
                df_del = pd.concat([df_temp, df_del])

            # Join the deleted rows to the dataframe and filter out the deleted rows
            if len(df_del) > 0:
                del df_del['attributes']
                df = df.merge(df_del, how='left', on='Id')
                df = df[df['IsDeleted'].isna()].copy()
                del df['IsDeleted']

        # Save the final result to the cache as a feather file and to csv
        if 'attributes' in df.columns:
            del df['attributes']
        df.reset_index(drop=True, inplace=True)
        try:
            df.to_feather(f'{data_dir}cache/{filename}.ftr')
        except Exception as e:
            df = df.astype(str)
            df.to_feather(f'{data_dir}cache/{filename}.ftr', compression='lz4')

            return df
