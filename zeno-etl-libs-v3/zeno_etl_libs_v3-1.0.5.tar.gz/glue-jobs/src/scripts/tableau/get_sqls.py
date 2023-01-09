import argparse
import os
import sys

import requests

sys.path.append('../../../..')
from zeno_etl_libs.helper.tableau.tableau import Tableau
from zeno_etl_libs.logger import get_logger

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stag, prod)")
parser.add_argument('-ts', '--table_suffix', default="", type=str, required=False,
                    help="Table suffix for testing.")
args, unknown = parser.parse_known_args()

env = args.env
os.environ['env'] = env
logger = get_logger()
table_suffix = args.table_suffix

logger.info(f"env: {env}")

tableau = Tableau()
tableau.login()

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Tableau-Auth': tableau.token
}

# workbook data list
response = requests.get(
    f'{tableau.url}/api/3.7/sites/{tableau.site_id}/workbooks?pageSize=3',
    headers=headers
)

if response.status_code != 200:
    raise Exception(f"workbook_response: {response.text}")
workbook_data = response.json()

wb_count = 0
for workbook in workbook_data['workbooks']['workbook']:
    wb_count += 1
    logger.info(f"{workbook['id']}")


    # # Make a GET request to the workbook data endpoint
    response = requests.get(
        f'{tableau.url}/api/{tableau.api_version}/sites/{tableau.site_id}/workbooks/{workbook["id"]}/datasources')
    w_data = response.json()
    print(w_data)

    connection_response = requests.get(
        f"{tableau.url}/api/{tableau.api_version}/sites/{tableau.site_id}/workbooks/{workbook['id']}/connections?pageSize=10",
        headers=headers)
    connection_data = connection_response.json()
    for connection in connection_data['connections']['connection']:
        response = requests.get(
            f"{tableau.url}/api/{tableau.api_version}/sites/{tableau.site_id}/workbooks/{workbook['id']}/connections?pageSize=10",
            headers=headers)
        # /datasources/{id}/query

    # response = requests.get(
    #     f"{tableau.url}/api/{tableau.api_version}/sites/{tableau.site_id}/workbooks/{workbook['id']}/views",
    #     headers=headers)
    # views_data = response.json()

    response = requests.get(
        f"{tableau.url}/api/{tableau.api_version}/sites/{tableau.site_id}/views",
        headers=headers)
    data = response.json()

    logger.info(f"wb_count: {wb_count}")
    v_count = 0
    for view in data['views']['view']:
        v_count += 1
        logger.info(f"v_id: {view['id']}")

        # https://{server}/api/{version}/sites/{site-id}/workbooks/{workbook-id}/views/{view-id}/sql
        # # /api/api-version/sites/site-id/views/view-id/data

        # response = requests.get(f"{tableau.url}/api/{tableau.api_version}/sites/{tableau.site_id}/views/{view['id']}",
        #                         headers=headers)
        response = requests.get(
            f"{tableau.url}/api/{tableau.api_version}/sites/{tableau.site_id}/views/{view['id']}/data",
            headers=headers)
        sql_data = response.json()
        logger.info(f"v_count: {v_count}")
        logger.info(f"sql_data: {sql_data}")

tableau.logout()
