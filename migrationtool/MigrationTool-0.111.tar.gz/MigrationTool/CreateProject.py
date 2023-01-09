import json
import re
import qdi_sdk
from qdi_sdk.clients import models
import Parser
import Landing
import Definition
import Storage
import DataMart
import Transformation


def CreateProject(project : Definition.Project):
     print('********** Creating a project **********')
     project_id = qdi_sdk.qdi.Project(
         project_name=project.project_name,
         project_description=project.project_description,
         data_connection_platform= project.data_connection_platform,
         space_name=project.space_name ,
         settings=project.settings
     )
     Parser.Parser.hddProject.project_id = project_id
     print('********** The project was created successfully **********')

Parser
hddProject = Parser.Parser.hddProject
CreateProject(hddProject)
Landing.Landing(hddProject)
Storage.Storage(hddProject)
Transformation.Transformation(hddProject)
DataMart.DataMart(hddProject)
print('Done!!!')
