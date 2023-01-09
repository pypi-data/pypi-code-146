import json

import requests

from zeno_etl_libs.config.common import Config


class Tableau:
    """
    class helps us to integrate with tableau APIs

    NOTES:
    > api_version: 3.7, server_version: v2020.1

    > rest-api fundamental concepts
    https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_fundamentals.htm

    > rest-api-samples
    https://github.com/tableau/rest-api-samples/tree/master/python
    https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_example_requests.htm (rq_bdy xml to json)

    > Pagination
    https://help.tableau.com/v2020.1/api/rest_api/en-us/REST/rest_api_concepts_paging.htm

    > List Data Sources
    https://help.tableau.com/v2020.1/api/rest_api/en-us/REST/rest_api_ref.htm#query_data_sources

    > List Data Source Connections
    https://help.tableau.com/v2020.1/api/rest_api/en-us/REST/rest_api_ref.htm#query_data_source_connections

    > Update a Data Source
    https://help.tableau.com/v2020.1/api/rest_api/en-us/REST/rest_api_ref.htm#update_data_source_connection

    > Sign Out
    https://help.tableau.com/v2020.1/api/rest_api/en-us/REST/rest_api_ref.htm#sign_out
    """

    def __init__(self):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets
        self.url = secrets['TABLEAU_BASE_URL']
        self.password = secrets['TABLEAU_ADMIN_PASSWORD']
        self.site_id = secrets['TABLEAU_SITE_ID']
        self.api_version = "3.7"
        self.token = None

    def login(self):
        self.get_token()

    def get_token(self):
        # sign in
        login_data = {
            "credentials": {
                "name": 'admin',
                "password": self.password,
                "site": {
                    "contentUrl": ""
                }
            }
        }
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(
            f"{self.url}/api/{self.api_version}/auth/signin",
            headers=headers,
            data=json.dumps(login_data)
        )
        login_resp = response.json()
        if response.status_code == 200 and 'credentials' in login_resp:
            login_resp = login_resp["credentials"]
            self.token = login_resp["token"]
            return self.token

        raise f"tableau api call failed with status code: {response.status_code}"

    def logout(self):
        if self.token:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                       'X-Tableau-Auth': self.token}
            response = requests.post(
                f"{self.url}/api/{self.api_version}/auth/signout",
                headers=headers
            )
            print(response)
            # logout_resp = response.json()
            if response.status_code == 204:
                print(f"Tableau logged out successfully.")
            else:
                print(f"Tableau logged failed.")
