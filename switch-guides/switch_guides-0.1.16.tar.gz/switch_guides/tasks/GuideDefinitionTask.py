# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from abc import abstractmethod
from io import StringIO
import json
import logging
import sys
import pandas
import requests
from ..models.guide import SwitchGuideDefinition
import switch_api as sw
from ..utils.utils import ApiInputs, _column_name_cap, get_journeys_endpoint
from switch_api.pipeline.pipeline import Task

class GuideDefinitionTask(Task):
    logger = None

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(logging.INFO)
        self.logger.handlers.clear()
        self.logger.addHandler(consoleHandler)
        formatter = logging.Formatter('%(asctime)s  switch_guides.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
                                      datefmt='%Y-%m-%dT%H:%M:%S')
        consoleHandler.setFormatter(formatter)

    @property
    @abstractmethod
    def definition(self) -> SwitchGuideDefinition:
        """"Structure of the Journey"""
        return None

    def register(self, api_inputs: ApiInputs):
        if api_inputs == None or api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
            self.logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        script_response = sw.pipeline.Automation.register_task(api_inputs, self)
        _, register = (0, script_response) if type(script_response) is pandas.DataFrame else script_response
        self.logger.info(register)

        headers = api_inputs.api_headers.default

        json_payload = {
            "scriptDriverId": str(self.id)
        }

        journey_endpoint = get_journeys_endpoint(api_inputs=api_inputs)
        
        url = f"{journey_endpoint}/projects/{api_inputs.api_project_id}/definitions/register"
        self.logger.info("Sending request: POST %s", url)

        response = requests.post(url, json=json_payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            self.logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                              response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            self.logger.error(
                'No data returned for this API call. %s', response.request.url)
            return response_status, pandas.DataFrame()
        
        response_data = pandas.read_json(StringIO(response.text), typ='Series').to_frame().T

        response_data.rename(columns = {'driverId':'guideDefinitionId'}, inplace = True)

        response_data.columns = _column_name_cap(response_data.columns)

        return response_status, response_data
