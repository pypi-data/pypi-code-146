import json
import logging

import urllib.request
from urllib.error import  URLError

from ..step_input import StepInput

"""
the base step for LOCAL execution
provides base functionality for step types that register or query
artifacts from the modelstore, evaluationstore or datastore services
check service-compute/api/flowcompilers for the equivalent cloud step compilers
"""

class CallStep():

    def __init__(self, step_type):
        self.step_type = step_type

    def call_service(self, entry, service_endpoint="http://127.0.0.1:8080"):

        """
        registers or queries metadata from services in sync fashion
        """

        api_endpoint = service_endpoint + "/v1.0/genome/pipelineSpec"

        operationURI = {
          "pushmodel": service_endpoint + "/v1.0/genome/modelArtifact",
          "pushdata": service_endpoint + "/v1.0/genome/dataArtifact",
          "pushevaluation": service_endpoint + "/v1.0/genome/evaluationArtifact",
          "pushcard": service_endpoint + "/v1.0/genome/cardArtifact",

          "querymodel": service_endpoint + "/v1.0/genome/search?artifactType=modelArtifact",
          "querydataartifact": service_endpoint + "/v1.0/genome/search-data",
          "queryevaluation": service_endpoint + "/v1.0/genome/search-validation",
          "querycard": service_endpoint + "/v1.0/genome/search-validation"
        }[self.step_type.lower()]

        #perform an http call to service from this step
        reqMeta = urllib.request.Request(operationURI)

        reqMeta.add_header(
            'Content-Type',
            'application/json',
        )

        try:

            response_meta = urllib.request.urlopen(reqMeta, json.dumps(entry).encode('utf-8'))
            logging.info(f'saved pipelineSpec at endpoint: {api_endpoint}')


            return response_meta


        except URLError as e:
            logging.info(f'failed to reach endpoint: {api_endpoint}')
            if hasattr(e, 'reason'):
                logging.info('Reason: ' + str(e.reason))

            if hasattr(e, 'code'):
                logging.info('Error code: ' + str(e.code))

            if hasattr(e, 'msg'):
                logging.info('Error message: ' + str(e.msg))

            # still throw it
            raise e



class PushStep(CallStep):

    def push_entry(self, entry, service_endpoint="http://127.0.0.1:8080"):

        dict_entry  = entry.get_meta() if isinstance(entry, StepInput) else entry

        push_prop = None

        if getattr(dict_entry, "model_artifact"):
            push_prop = "model_artifact"

        if getattr(dict_entry, "data_artifact"):
            push_prop = "data_artifact"

        if getattr(dict_entry, "evaluation_artifact"):
            push_prop = "evaluation_artifact"

        if getattr(dict_entry, "card_artifact"):
            push_prop = "card_artifact"

        if getattr(dict_entry, "pipeline_meta"):
            push_prop = "pipeline_meta"


        resp_entry = super().call_service(dict_entry[push_prop])

        # if the response contains the resource id add it to the input and return that
        if "id" in resp_entry and resp_entry["id"]:
            dict_entry[push_prop]["id"] = resp_entry["id"]

        return StepInput.from_meta(dict_entry)



class QueryStep(CallStep):

    def query(self, entry, service_endpoint="http://127.0.0.1:8080"):

        dict_entry  = entry.get_meta() if isinstance(entry, StepInput) else entry

        push_prop = "query_spec"

        #call the service with the query contained in the query_spec object
        resp_entry = super().call_service(dict_entry[push_prop])
        dict_results = {
          "cls_name": "QueryOutput",
          "query_results": resp_entry
        }

        return StepInput.from_meta(dict_results)
