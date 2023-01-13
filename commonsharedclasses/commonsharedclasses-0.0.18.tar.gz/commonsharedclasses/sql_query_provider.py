import os
import logging
import traceback
import json


class QueryProvider():
    
    def __init__(self, project_attributes, aggregation, order_attributes, skip_count, numrows, delta_table_name, filter_attributes, facet_attribute):
        self.project_attributes = project_attributes
        self.aggregation = aggregation
        self.order_attributes = order_attributes
        self.skip_count = skip_count
        self.numrows = numrows
        self.delta_table_name = delta_table_name
        self.filter_attributes = filter_attributes
        self.facet_attributes = facet_attribute

    def createQuery(self,pagination):
        # Building the query based on the parameters passed
        query = "SELECT "

        if self.project_attributes is not None:
            query += '*' if '*' in self.project_attributes else ','.join(
                [name + " as " + alias for name, alias in self.project_attributes.items()])

        if self.aggregation is not None:
            query += ',' if self.project_attributes is not None else ''
            query += ','.join(["{fn}({attr}) as {alias}".format(fn=agg['function'],
                            attr=agg['attribute'], alias=agg['alias']) for agg in self.aggregation])

        if self.order_attributes is not None and self.filter_attributes is not None and self.aggregation is None:
            query += " FROM "
            colValueOrderBy = ','.join([att + " " + dir for att, dir in self.order_attributes.items()])
            query += " (SELECT * ,row_number() OVER (ORDER BY {colOrderBy}) AS rankcol FROM {tablename} where {filter}) x".format(colOrderBy = colValueOrderBy,tablename=self.delta_table_name,filter=self.filter_attributes)
            query += " WHERE x.rankcol > {skip}".format(skip=self.skip_count)
            query += " LIMIT {numrows}".format(numrows=self.numrows)
        elif self.order_attributes is not None and self.aggregation is None:
            query += " FROM "
            colValueOrderBy = ','.join([att + " " + dir for att, dir in self.order_attributes.items()])
            query += " (SELECT * ,row_number() OVER (ORDER BY {colOrderBy}) AS rankcol FROM {tablename}) x".format(colOrderBy = colValueOrderBy,tablename=self.delta_table_name)
            query += " WHERE x.rankcol > {skip}".format(skip=self.skip_count)
            query += " LIMIT {numrows}".format(numrows=self.numrows)        
        else: 
            if self.filter_attributes is not None:
                query += " FROM "
                if pagination == True:
                    query += " (SELECT * ,row_number() OVER (ORDER BY skypoint_delta_index) AS rankcol FROM {tablename} where {filter}) x".format(tablename=self.delta_table_name,filter=self.filter_attributes)
                else:
                    query += " (SELECT * ,row_number() OVER (ORDER BY (SELECT NULL)) AS rankcol FROM {tablename} where {filter}) x".format(tablename=self.delta_table_name,filter=self.filter_attributes)
                
                if self.skip_count is not None:
                    query += " WHERE x.rankcol > {skip}".format(skip=self.skip_count)                
            else:
                query += " FROM {tablename}".format(tablename=self.delta_table_name)
                if self.skip_count is not None and pagination == True:
                    query += " WHERE skypoint_delta_index > {skip}".format(
                        skip=self.skip_count)

            if self.facet_attributes is not None and self.aggregation is not None:
                query += " GROUP BY {}".format(self.facet_attributes)

            if self.order_attributes is not None:
                query += " ORDER BY {}".format(','.join([att + " " + dir for att, dir in self.order_attributes.items()]))

            if self.numrows is not None:
                query += " LIMIT {numrows}".format(numrows=self.numrows)

        logging.info(str(query))
        return query