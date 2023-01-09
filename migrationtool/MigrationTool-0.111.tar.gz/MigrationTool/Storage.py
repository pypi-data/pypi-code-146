import json
import re
import qdi_sdk
from qdi_sdk.clients import models
import Definition
import Parser
class Storage(object):
    hddProject = Definition.Project
    def __init__(self, project: Definition.Project):
        self.hddProject = project

        #timeOut = 50

        ################################## Cloud - Create Storage #################################
        print('********** Creating a storage **********')
        self.hddProject.project_id.storage.create(
            storage_name=self.hddProject.storage_name
        )
        print('********** The storage was created successfully **********')
    
        ################################## Cloud - Prepare Storage #################################
        
        #print('********** Prepare a storage **********')
        #self.hddProject.project_id.storage.prepare()
        #print('********** The storage was prepared successfully **********')
        
        ################################### Cloud - Run Storage #################################
        #
        #print('********** Run a storage **********')
        #project_id.run_data_app(
        #    data_app_name=storage_name
        #)
        #print('********** The storage was run successfully **********')


