import json
import re
import qdi_sdk
from qdi_sdk.clients import models
import Parser 
import Definition
class Landing(object):
    ### Properties 
    #timeOut = 50
    hddProject = Definition.Project
    def __init__(self, project: Definition.Project):
        self.hddProject = project
        print('********** Creating a landing **********')
        
        print(f'Number of Adding Entity to Landing: {len(self.hddProject.tables)}')
        self.hddProject.project_id.landing.create(
            landing_platform=self.hddProject.sql_server,
            tables=self.hddProject.tables
        )
        print('********** The landing was created successfully **********')

        ################################## Cloud - Prepare Landing #################################
        
        #print('********** Prepare a Landing **********')
        #self.hddProject.project_id.landing.prepare()
        #print('********** The landing was prepared successfully **********')
        
        ################################### Cloud - Run Landing #################################
        
        #print('********** Run a Landing **********')
        #project_id.run_data_app(
        #    data_app_name=landing_name
        #)
        #print('********** The landing was run successfully **********')