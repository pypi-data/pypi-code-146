import re
import qdi_sdk
from qdi_sdk.clients import models

class Project:
    def __init__(self):
        project_id=qdi_sdk.qdi.Project
        project_name=''
        project_description=''
        data_connection_platform=''
        space_name=''
        tableList=[]
        datamartList=[DataMart()]
        relationList=[Relation()]
        landing=Landing()
        storage=Storage()
        transformation=''
        settings=qdi_sdk.qdi_settings

class Table:
    def __init__(self):
        id =''
        logicalName = ''
        physicalName = ''
        mappedName = ''
        colList = [Column()]
        isFromSrc = False

class Relation:
    def __init__(self):
        storage_name=''
        source_entity_name=''
        source_column_name=''
        target_entity_name=''
        target_column_name=''
        prefix=''


class Column:
    def __init__(self):
        id = ''
        colName = ''
        mappedName =''
        mappedId=''
        table = ''
        tableId=''
        isPk=False
        data_type=qdi_sdk.models.DatatypeType.WSTRING
        length=25
        

class Landing:
    def __init__(self):
        landing_name=''
        tables=[]
        sql_server=qdi_sdk.models.SqlServer

class Storage:
    def __init__(self):
        storage_name=''

class Transformation:
    def __init__(self):
        transformation_name=''

class Dimension:
    def __init__(self):
        id=''
        name=''
        displayName=''
        rootTable=''
        linkedEntities=[]


class Fact:
    def __init__(self):
        id =''
        name =''
        starSchemaName=''
        linkedEntities=[]
        trasactionDate=''
        connectDimList=[]
        rootEntity=''


class DmConnect:
    def __init__(self):
        star_schema_name=''
        dimension_name=''

class DataMart:
    def __init__(self):
        id =''
        Name =''
        factList=[]
        dimensionList=[]


class input:
    def __init__(self):
        project_description =''
        landing_name =''
        storage_name =''
        transformation_name =''
        qem_server_name =''
        storage_connection_name =''
        source_connection_name =''
        space_name =''
        host =''
        api_version =''
        bearer_token =''
        project_name =''
        json_path =''
        input_path=''
        manual=False
        online=False


    


