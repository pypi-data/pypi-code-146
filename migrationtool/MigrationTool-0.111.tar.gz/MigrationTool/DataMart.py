import json
import re
import qdi_sdk
from qdi_sdk.clients import models
import Definition
import Parser
class DataMart(object):
    hddProject = Definition.Project
    def __init__(self, project: Definition.Project):
        self.hddProject = project
        print('********** Create DM **********')
        for dm in self.hddProject.datamartList.values():
            self.hddProject.project_id.data_mart.create(
                data_mart_name=dm.Name,
                source_name=self.hddProject.transformation_name,
                source_type = qdi_sdk.models.DataAppType.TRANSFORM
                )
            for fact in dm.factList:
                print('********** Create start schema **********')
                try:
                    self.hddProject.project_id.data_mart.create_star_schema(
                        star_schema_name=fact.starSchemaName,
                        root_entity=fact.rootEntity,
                        transactional_date_name=fact.trasactionDate,
                        tables_to_denormalize=fact.linkedEntities, ## ?
                        tables_in_schema=fact.linkedEntities,
                        data_mart_name=dm.Name
                    )
                    print('********** The start schema was created successfully **********')
                except:
                     print(f'EEEEEEEEE The table: {fact.starSchemaName}  TransactionDate: {fact.trasactionDate}  EEEEEEEEE')
                     continue
            try:
                for dim in dm.dimensionList:
                    print('********** Create dimension **********')
                    self.hddProject.project_id.data_mart.create_dimension(
                        dimension_name=dim.displayName,
                        dimension_base_table=dim.name,
                        tables_in_schema=dim.linkedEntities,
                        history_type=qdi_sdk.models.DimensionType.TYPE1,
                        data_mart_name=dm.Name
                        )
                    print('********** The dimension was created successfully **********')
            except:
                continue
            try:
                for fact in dm.factList:
                    for connect in fact.connectDimList:
                        self.hddProject.project_id.data_mart.connect(
                            star_schema_name=connect.star_schema_name,
                            dimension_name=connect.dimension_name,
                            data_mart_name=dm.Name
                            )
                    print('********** Connected **********')
            except:
                continue
