import json
import re
import qdi_sdk
from qdi_sdk.clients import models
import Definition
class Transformation(object):
    hddProject = Definition.Project
    def __init__(self, project: Definition.Project):
        self.hddProject = project
################################ Cloud - Create Transformation #################################
        
        print('********** Creating a transformation **********')
        self.hddProject.project_id.transform.create(
            transform_name=self.hddProject.transformation_name,
            source_tables='*',
            source_name=self.hddProject.storage_name,
            source_type=qdi_sdk.models.DataAppType.STORAGE
        )
        print('********** Transformation is created successfully**********')
        
        print('********** Creating relations **********')
        checkDuplicate=[]
        for relation in self.hddProject.relationList:
            if f'{relation.source_entity_name}_{relation.target_entity_name}_{relation.prefix}{relation.source_column_name}' not in checkDuplicate and relation.source_column_name is not None:
                try:
                    self.hddProject.project_id.transform.model.create_relationship(
                        source_entity_name=relation.source_entity_name,
                        source_column_name=relation.source_column_name,
                        target_entity_name=relation.target_entity_name,
                        target_column_name=relation.prefix+relation.target_column_name,
                        relationship_name=f'R_{relation.source_entity_name}_{relation.target_entity_name}_{relation.prefix}{relation.source_column_name}'
                        )
                    checkDuplicate.append(f'{relation.source_entity_name}_{relation.target_entity_name}_{relation.prefix}{relation.source_column_name}')
                except Exception  as ex:
                    print (ex)
                    continue

        print('********** The relations were created successfully **********')
        
        
        
        ################################## Cloud - Create Mappings #################################
        #
        print('********** Mapping **********')
        try:
            # add entity
            # compose tables list - find map - add entity for the trans
            for table in self.hddProject.tableList.values():#source # get compose tables
                if table.mappedName != table.physicalName and table.isFromSrc == True:
                    self.hddProject.project_id.transform.local_rules.rename_table(
                        table_name=table.physicalName,
                        new_table_name=table.mappedName ,
                        #rule_name=f'T_{table.logicalName}_To_{table.mappedName}'
                    )
                if table.isFromSrc == False:
                    self.hddProject.project_id.transform.add_entity(
                        source_entity_name=table.physicalName,
                        new_entity_name=table.mappedName # optional, if not added will create new with increasing number
                        )
                    for col in table.colList:   
                        if col.colName != col.mappedName:
                                self.hddProject.project_id.transform.local_rules.rename_column(
                                    old_col_name=col.colName,
                                    new_col_name=col.mappedName,
                                    table_name=table.mappedName
                                    #rule_name=f'T_{table.mappedName}_C_{col.colName}_To_{col.mappedName}'
                                    )
                    for sTable in self.hddProject.tableList.values():
                        if sTable.physicalName == table.physicalName and sTable.isFromSrc == True:
                            srcColList = sTable.colList #and exist
                    for sCol in srcColList:
                        needToDrop=True
                        for newCol in table.colList:
                            if sCol.colName == newCol.colName:
                                needToDrop = False
                                break
                        if(needToDrop == True):
                            self.hddProject.project_id.transform.local_rules.drop_column(
                                col_to_drop=sCol.colName,
                                table_name=table.mappedName,
                                #rule_name=f'Drop_C_{sCol.colName}_From_T_{table.mappedName}'
                                )

                    column = Definition.Column()
                    try:
                        for column in table.colList:
                            self.hddProject.project_id.transform.local_rules.rename_column(
                                old_col_name=column.colName,
                                new_col_name=column.mappedName,
                                table_name=table.mappedName,
                                #rule_name=f'T_{table.mappedName}_{column.colName}_To_{column.mappedName}'
                                )
                    except Exception as ex:
                        print(ex)
                        continue
        except Exception as ex:
            print(ex)
        print('********** Mapping is DONE! **********')