import json
import re
import qdi_sdk
from qdi_sdk.clients import models
from Definition import *
import InputForm


class Parser(object):
    hddProject=Project
    tableNameList=[] #list of table names
    physicalTables=[] #list of physical table names
    
    physicalTablesId=dict() #[id] = name
    tableMappings = dict()
    colIdNameArr = dict()
    colMappingNameByName=dict()
    colIdPoeArr=dict()
    srcColMap=dict()
    dmIDName=dict()
    factIDName=dict()
    starSchemaIDName=dict()
    dimIDName=dict()
    dimSchemaIDName=dict()
    linkedDMFact=dict()
    linkedFactDims=dict()
    factIdDateColName=dict()
    rootentityIDbyFact=dict()
    starSchemaByDm=dict()
    dimensionByDm=dict()
    mappedTablesLogicalNameToPhysical=dict()
    tablePkIds=dict()
    sourceTablesLogical=[]
    testTables=[]
    hddProject.manual=False
    hddProject.online = False
    
    
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    #                                                                                         #
    #                       Manual Fields filled by the User!!                                #
    #                                                                                         #
    #                                                                                         #
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    InputForm.InputForm(hddProject)
    hddProject=InputForm.InputForm.hddProject
    if(hddProject.manual is not None and hddProject.manual == True ):
        inputFilePath=hddProject.input_path #"C:/Users/EWX/OneDrive - QlikTech Inc/Desktop/inp/input.json"
        inputFile = open(inputFilePath)
        # returns JSON object as a dictionary
        inputFileData = json.load(inputFile)

        project_description =inputFileData['project_description'] 
        landing_name = inputFileData['landing_name']
        storage_name = inputFileData['storage_name']
        transformation_name = inputFileData['transformation_name']
        qem_server_name = inputFileData['qem_server_name']
        storage_connection_name = inputFileData['storage_connection_name']
        source_connection_name = inputFileData['source_connection_name']
        space_name = inputFileData['space_name']
        host=inputFileData['host'] 
        api_version=inputFileData['api_version']
        bearer_token=inputFileData['bearer_token']
        project_name = inputFileData['project_name']
        jsonPath = inputFileData['jsonPath']

    if(hddProject.online is not None and hddProject.online == True ):
        project_description =hddProject.project_description 
        landing_name = hddProject.landing_name
        storage_name = hddProject.storage_name
        transformation_name = hddProject.transformation_name
        qem_server_name = hddProject.qem_server_name
        storage_connection_name = hddProject.storage_connection_name
        source_connection_name = hddProject.source_connection_name
        space_name = hddProject.space_name
        host=hddProject.host
        api_version=hddProject.api_version
        bearer_token=hddProject.bearer_token
        project_name = hddProject.project_name
        jsonPath = hddProject.json_path
    #project_description ='Moving compose to Cloud'
    #landing_name = 'landing_Test_new'
    #storage_name = 'storage_Test_new'
    #transformation_name = 'Transformation_CRD'
    #qem_server_name = 'lina_us_stage_1'
    #storage_connection_name = 'ComposeToHDD'
    #source_connection_name = 'SQL_Source'
    #space_name = 'Lina'
    #host='https://4hqjowglfqqi41f.us.qlik-stage.com'
    #api_version=1
    #bearer_token='eyJhbGciOiJFUzM4NCIsImtpZCI6ImFjMWRlMWZlLWMyM2ItNDliYi1iMmI1LWFiODU3YTFiZDI5NiIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiOGRaanA3TEE5VEhoRmV0T2JuV3VPQ0tNYk4ydWt5Vk0iLCJqdGkiOiJhYzFkZTFmZS1jMjNiLTQ5YmItYjJiNS1hYjg1N2ExYmQyOTYiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjJhNzE4OTIzNzJkOWY0MmU1YWI2ZjJjIn0.eF7PvuCZCu96e-KsrT8mSrY8BdJU7DUBYtM99QH5yfrSnoTSbcdgUqGPwK9qJikbqR9bRCh9_xUcSdb6fwwDHiL5SJTSJ-JEM76geyAetnAypDFrIKrPXV9iycHInhOY'
    #project_name ='TEST_AUTH'
    
    
    ###########################################################################################
    ###########################################################################################
    ###########################################################################################
    ##############################################################
    if((hddProject.online == False and hddProject.manual == False) is not True):

        data_connection_platform=qdi_sdk.models.Snowflake(connection_name=storage_connection_name)
        
        settings = qdi_sdk.qdi_settings(
        host=host,
        api_version=api_version,
        bearer_token=bearer_token
        )

        sql_server = qdi_sdk.models.SqlServer(
        connection_name = source_connection_name
        )
        ##############################################################


        tablesId=dict() #[id] = name
        dataMartList = dict()
        hddProject.data_connection_platform = data_connection_platform
        hddProject.space_name = space_name
        hddProject.settings = settings
        hddProject.project_description=project_description
        hddProject.landing_name=landing_name
        hddProject.sql_server=sql_server
        hddProject.storage_name=storage_name
        hddProject.transformation_name=transformation_name
        hddProject.tables=[]
        hddProject.relationList=[]
        hddProject.tableList=dict()

        
        #jsonPath=inputFileData['jsonPath'] 
        #jsonPath="C:/Users/EWX/OneDrive - QlikTech Inc/Desktop/inp/NORTHWIND-SNOWFLAKE.json" #North_Test  #DW_Core_CASE_18443 , NORTHWIND-SNOWFLAKE
            
        #def __Init__(self):
        # Opening JSON file
        jsonFile = open(jsonPath)
        # returns JSON object as a dictionary
        composeData = json.load(jsonFile)
        project = composeData['objects']
        # Iterating through the json list
        
        for i in project:
            if i['type'] == 'ExecutionServiceDto':
                hddProject.project_name =project_name
            if i['type'] == 'Entity':
                table = Definition.Table()
                table.id = str(i['id'])
                table.logicalName=i['name']
                table.physicalName=''
                table.mappedName=i['name']
                table.colList=[]
                table.isFromSrc=False
                if i['inner_item']['$type'] == 'EntityFull':
                    sourceTablesLogical.append(i['name'])
                    table.isFromSrc=True
                print(f'Adding Entity {table.logicalName}')
                tableNameList.append(i['name'])
                tablesId[str(i['id'])] = table
            if i['type'] == 'Mapping':
                columns = dict()
                tablename=tablesId[str(i['inner_item']['entity_id'])]
                physicalTablesId[i['inner_item']['entity_id']]=i['inner_item']['table_name']
                table = tablesId[str(i['inner_item']['entity_id'])]
                table.physicalName = i['inner_item']['table_name']
                testTables.append(i['inner_item']['table_name'])
                for m in i['inner_item']['mapping_fields']:
                    try: 
                        if m['mapping_type'] == 'DIRECT' and m['staging_col_name_int'] is not None:
                            s=m['staging_col_name_int']
                            if s != 'FD':
                                colIdArr=s.split('_')
                                columns[colIdArr[1]] = m['source_col_name']
                                colMappingNameByName[colIdArr[len(colIdArr)-2]]=colIdArr[len(colIdArr)-1]
                                srcColMap[str(m['source_col_name'])]=[colIdArr[len(colIdArr)-2],colIdArr[len(colIdArr)-1]]
                                col = Definition.Column()
                                col.id = colIdArr[len(colIdArr)-1]
                                col.colName= m['source_col_name']
                                col.mappedId = colIdArr[len(colIdArr)-2]
                                table.colList.append(col)
                    except:
                        continue
                tablesId[str(i['inner_item']['entity_id'])] = table
                tableMappings[tablename]=columns
            if i['type'] == 'DomainAttribute':
                colIdNameArr[str(i['id'])] = str(i['name'])
            if i['type'] == 'TableColumn':
                colIdPoeArr[str(i['id'])] = i['inner_item']['poe'] 
                if i['inner_item']['is_primary'] == True and str(i['inner_item']['pbe']) in colIdNameArr.keys():
                    tablePkIds[tablesId[str(i['inner_item']['poe'])].logicalName] = colIdNameArr[str(i['inner_item']['pbe'])]
            if i['type'] == 'DataMartInfo':
                dmIDName[i['id']]=i['name']
                dm=Definition.DataMart()
                dm.id = str(i['id'])
                dm.Name = i['name']
                dm.dimensionList=[]
                dm.factList=[]
                dataMartList[str(dm.id)] = dm
            if i['type'] == 'FactDim':
                if i['inner_item']['type'] == 'DIMENSION':
                    dimIDName[str(i['id'])] =i['name'].split('_',1)[1]
                    dimSchemaIDName[str(i['id'])] = i['inner_item']['display_name']
                    linkedFactDims[str(i['id'])] = i['inner_item']['linked_entities']
                    if(len(dimensionByDm) == 0 or not i['inner_item']['datamart_id'] in dimensionByDm.keys()):
                        dimensionByDm[i['inner_item']['datamart_id']]=[str(i['id'])]
                    else:
                        dimensionByDm[i['inner_item']['datamart_id']].append(str(i['id']))
                    dim = Definition.Dimension()
                    dim.id = str(i['id'])
                    dim.displayName = i['inner_item']['display_name']
                    dim.name = i['name'].split('_',1)[1]
                    dim.rootTable = i['inner_item']['root_entity_id']
                    dim.linkedEntities = i['inner_item']['linked_entities']
                    dm=dataMartList[str(i['inner_item']['datamart_id'])]
                    dm.dimensionList.append(dim)
                    dataMartList[str(i['inner_item']['datamart_id'])] = dm
                if i['inner_item']['type'] == 'FACT':
                    starSchemaIDName[str(i['id'])] = i['inner_item']['display_name']
                    factIDName[str(i['id'])] = i['name'].split('_')[1]
                    rootentityIDbyFact[str(i['id'])]=i['inner_item']['datamart_id']
                    if(len(starSchemaByDm) == 0 or not i['inner_item']['datamart_id'] in starSchemaByDm.keys()):
                        starSchemaByDm[i['inner_item']['datamart_id']]=[str(i['id'])]
                    else:
                        starSchemaByDm[i['inner_item']['datamart_id']].append(str(i['id']))
                    try:
                        factIdDateColName[str(i['id'])] = colMappingNameByName[i['inner_item']['txdate_path'].split(' ')[-1]]
                    except:
                        test=""
                    if len(linkedDMFact)== 0 or not(i['inner_item']['datamart_id'] in linkedDMFact.keys()):
                        linkedDMFact[i['inner_item']['datamart_id']]=[str(i['id'])]
                    else:
                        val = linkedDMFact[i['inner_item']['datamart_id']]
                        val.append(str(i['id']))
                        linkedDMFact[i['inner_item']['datamart_id']]=val
                    linkedFactDims[str(i['id'])] = i['inner_item']['linked_entities']
                    fact=Definition.Fact()
                    fact.connectDimList=[]
                    fact.id=str(i['id'])
                    fact.name=i['name'].split('_', 1)[1]
                    fact.starSchemaName=i['inner_item']['display_name']
                    fact.linkedEntities=i['inner_item']['linked_entities']
                    if str(i['inner_item']['txdate_path'].split(' ')[-1]) in colMappingNameByName.keys():
                        fact.trasactionDate=colIdNameArr[colMappingNameByName[str(i['inner_item']['txdate_path'].split(' ')[-1])]]
                    fact.rootEntity = str(i['name'].split('_',1)[-1])
                    dm=dataMartList[str(i['inner_item']['datamart_id'])]
                    dm.factList.append(fact)
                    dataMartList[str(i['inner_item']['datamart_id'])] = dm

        for i in project:
            if i['type'] == 'TableColumn' and i['inner_item']['block'] ==0:
                if str(i['inner_item']['pbe']) in tablesId.keys():
                    tableN=tablesId[str(i['inner_item']['poe'])].logicalName
                    try:
                        prefix=""
                        colName=''
                        if i['inner_item']['attribute_name'] is not None:
                            colName=i['inner_item']['attribute_name']
                    except:
                        try:
                            test1=tablesId[str(i['inner_item']['poe'])]
                            test2=tableMappings[test1]
                            test3=test2[str(i['id'])]
                            colName =  tableMappings[tablesId[str(i['inner_item']['poe'])]][str(i['id'])]
                        except:
                            continue
                    try:
                         if i['inner_item']['prefix'] is not None:
                             prefix=str(i['inner_item']['prefix'])
                             colName=colName
                    except:
                        colName=colName
                    source_entity_name = tablesId[str(i['inner_item']['poe'])].physicalName
                    target_entity_name=tablesId[str(i['inner_item']['pbe'])].physicalName
                    relation = Definition.Relation()
                    relation.source_entity_name = source_entity_name
                    relation.prefix=prefix
                    if colName in tablePkIds.keys():
                        relation.source_column_name = tablePkIds[colName]
                    else:
                        relation.source_column_name =colName
                    relation.target_entity_name = target_entity_name
                    if colName in tablePkIds.keys():
                        relation.target_column_name = tablePkIds[colName]
                    else:
                        relation.target_column_name =colName
                    if relation not in hddProject.relationList and relation.source_column_name is not None and relation.source_column_name != '':
                        hddProject.relationList.append(relation)

        ### Closing file

        jsonFile.close()
        print(f'Logical Tables in Total: {len(tableNameList)}')
        print(f'Physical Tables in Total: {len(physicalTablesId.keys())}')
        updatedList = list(tablesId.values())
        for rTable in updatedList:
            if rTable.physicalName == '':
                del tablesId[rTable.id]
        hddProject.tableList=tablesId
        hddProject.datamartList = dataMartList
        for table in hddProject.tableList.values():
            newColList=[]
            for col in table.colList:
                col.mappedName = f'{colIdNameArr[srcColMap[col.colName][1]]}'
                newColList.append(col)
            table.colList=newColList
            hddProject.tableList[table.id] = table
        
        #list of tablesName:
        checkDuplicate=[]
        for table in hddProject.tableList.values():
            if table.physicalName is not None and table.physicalName !='' and table.physicalName not in checkDuplicate:
                hddProject.tables.append(table.physicalName)
                checkDuplicate.append(table.physicalName)
        print(f'{len(hddProject.tables)}')
        print(f'{len(hddProject.tableList)}')
        hddProject.tables=testTables

        #open file and read the content in a list
        #with open(r'C:\Users\EWX\OneDrive - QlikTech Inc\Desktop\inp\tables1.txt', 'w') as f:
        #    for tab in hddProject.tables:
        #        f.write(f'select count(*) from [dbo].[{tab}]; \n')

        for id in tablesId:
            if int(id) in physicalTablesId.keys():
                mappedTablesLogicalNameToPhysical[tablesId[id].mappedName]=physicalTablesId[int(id)]
        for dm in hddProject.datamartList.values():
            for fact in dm.factList:
                for dim in fact.linkedEntities:
                    connect = Definition.DmConnect()
                    connect.star_schema_name=starSchemaIDName[fact.id]
                    if dimSchemaIDName[str(dim)] in mappedTablesLogicalNameToPhysical.keys():
                        connect.dimension_name=dimSchemaIDName[str(dim)]
                    else:
                        continue
                    fact.connectDimList.append(connect)

print("End of Parse!")

    