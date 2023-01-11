import os
import requests
import logging
from retrying import retry
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

class logconfiguration():
    def __init__(self):
        
        #session configurations
        self.session_total_retries=5
        self.session_connect_retries=15
        self.session_read_retries=15
        self.backoff_factor=12
        self.status_forcelist=[429, 500, 502, 503, 504]
        self.stop_max_attempt_number=5
        self.success_code=200
        
        #logging level configurations
        self.APIM_baseurl=None
        self.LogInformation=False
        self.LogDebugInfo=False
        self.LogDebugErrors=False

        self.environment=os.environ.get('Environment','Development')

        self.APIM_baseurl=os.environ.get('APIMGateway','https://gwdev.skypointcloud.com')
        self.cosmosloggingurl=self.APIM_baseurl+"/internal/api/instances/manage/workflow"
        self.cosmosorchestratorparamsloggingurl=self.APIM_baseurl+"/internal/api/instances/manage/workflow/createazurefunctioninstance"
        self.WorkflowLogLevel = os.environ.get('WorkflowLogLevel','Information')

        if self.WorkflowLogLevel=='Information':
            self.LogInformation=True

        elif self.WorkflowLogLevel=='DebugInfo':
            self.LogInformation=True
            self.LogDebugInfo=True

        elif self.WorkflowLogLevel=='DebugErrors':
            self.LogInformation=True
            self.LogDebugErrors=True
            
        elif self.WorkflowLogLevel=='Verbose':
            self.LogInformation = True
            self.LogDebugInfo = True
            self.LogDebugErrors = True

    @retry(stop_max_attempt_number=5)
    def cosmoslogging(self):
        session = requests.Session()
        session.headers.update(self.headers)
        retries = Retry(total=self.session_total_retries,connect=self.session_connect_retries,
                        read=self.session_read_retries,backoff_factor=self.backoff_factor,
                        status_forcelist=self.status_forcelist)
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://",adapter)
        response_lists = session.post(self.cosmosloggingurl,json=self.payload)
        
        if response_lists.status_code == self.success_code:
            message="current task status written to cosmosdb successfully"
            logging.info(message)
        else:
            message="writing current task status to cosmosdb is not successfull"
            logging.error(message)
            response_lists.raise_for_status()

    @retry(stop_max_attempt_number=5)
    def cosmosorchestratorlogging(self):
        session = requests.Session()
        session.headers.update(self.headers)
        retries = Retry(total=self.session_total_retries,connect=self.session_connect_retries,
                        read=self.session_read_retries,backoff_factor=self.backoff_factor,
                        status_forcelist=self.status_forcelist)
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://",adapter)
        response_lists = session.post(self.cosmosorchestratorparamsloggingurl,json=self.payload)
        
        if response_lists.status_code == self.success_code:
            message="orchestrator URLS updated to cosmosdb successfully"
            logging.info(message)
        else:
            message="orchestrator URLS not updated to cosmosdb successfully"
            logging.error(message)
            response_lists.raise_for_status()