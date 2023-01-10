import boto3
from ..models.scan_object import Scan_Object

class Dynamo_Handler:
    def __init__(self):
        self.client = boto3.client("dynamodb")
    
    def add_item(self, **kwargs):
        table_name_key = "table_name"
        fields_key = "fields"
        
        if table_name_key not in kwargs:
            assert("Error: Table name must be provided to create a new entry")    
        table_name = kwargs[table_name_key]
        
        if fields_key not in kwargs:
            assert("Error: Must provide fields for new entry")
        fields = kwargs[fields_key]
        
        name_key = 'item_name'
        type_key = 'item_type'
        val_key = 'item_value'
         
        item = {f'{field[name_key]}': {f'{field[type_key]}': f'{field[val_key]}'} for field in fields }
        
        self.client.put_item(
            TableName = table_name,
            Item=item
        )
    
    def get_item(self, table_name, partition, sort_field = ""):
        keyword_name_key = 'name'
        keyword_value_key = 'value'
        keyword_type_key = 'type'
        
        if keyword_name_key not in partition:
            assert(f"Error: {keyword_name_key} missing in partition argument")
        if keyword_type_key not in partition:
            assert(f"Error: {keyword_type_key} missing in partition argument")
        if keyword_value_key not in partition:
            assert(f"Error: {keyword_value_key} missing in partition argument")
        
        key = {partition[keyword_name_key]: {partition[keyword_type_key]: partition[keyword_value_key]}}
        if sort_field != '':
            
            if keyword_name_key not in sort_field:
                assert(f"Error: {keyword_name_key} missing in sort_field argument")
            if keyword_type_key not in sort_field:
                assert(f"Error: {keyword_type_key} missing in sort_field argument")
            if keyword_value_key not in sort_field:
                assert(f"Error: {keyword_value_key} missing in sort_field argument")
            
            
            key[sort_field[keyword_name_key]] = {sort_field[keyword_type_key]: sort_field[keyword_value_key]}
            
        response = self.client.get_item(
            TableName = table_name,
            Key = key
        )
        
        return response
         
    def create_table(self, **kwargs):
        #List of keyword keys required for create a table
        table_key = "table_name"
        schema_key = "key_schema"
        attributes_key ="attributes"
        provisioned_key = "provisioned"
        
        #Checks to make sure required keys are passed to create_table method
        keys = [table_key, schema_key, attributes_key, provisioned_key]
        for key in keys:
            if key not in kwargs:
                assert(f"Error: Please provide {key} as an argument")
    
        #Retrieves the arguments from kwargs
        table_name = kwargs[table_key]
        schema = kwargs[schema_key]
        attributes = kwargs[attributes_key]
        provisoned = kwargs[provisioned_key]
        
        #Creates the schema and attribute dictionary 
        schema_list = [{'AttributeName': key, 'KeyType': val} for key, val in schema.items()]
        attribute_list = [{'AttributeName': key, 'AttributeType': val} for key, val in attributes.items()]
        
        #creates the new table with the elemets provided
        table = self.client(
            TableName = table_name,
            KeySchema=schema_list,
            AttributeDefinitions=attribute_list,
            ProvisionedThroughput=provisoned
        )                
        
        #waits and confirms table exists
        table.wait_until_exists()
        
        return table.item_count
    
    def scan_table(self, table_name, scan_filters, display_filters=""):
        scan = self.__build_scan(table_name, scan_filters, display_filters)
        items = scan.get_scan_object()
        
        return self.client.scan(**items)
        
    def __build_scan(self, table_name, scan_filters, display_filters=""):
        request_dict = {}
        
        attribute_short_key = "short_name"
        attribute_name_key = "name"
        attribute_value_key = "value"
        
        if len(scan_filters) == 0:
            assert("Error: scan_filters can not be empty")
        
        #Checks for keys and assigns the value
        if attribute_name_key not in scan_filters:
            assert(f"Error: {attribute_name_key} required for scan_filters")
        scan_filter_name = scan_filters[attribute_name_key]
        
        if attribute_short_key not in scan_filters:
            assert(f"Error: {attribute_short_key} required for scan_filters")
        scan_filter_short_name = scan_filters[attribute_short_key]
        
        if attribute_value_key not in scan_filters:
            assert(f"Error: {attribute_value_key} required for scan_filters")
        scan_filter_value = scan_filters[attribute_value_key]
        
        #creats the sca_filter_dict for the ExpressionAttributeValues
        scan_filter_dict = {scan_filter_short_name: scan_filter_value}
        #creates the scan_filter_string for the FilterExpression
        scan_filter_string = f'{scan_filter_name} = {scan_filter_short_name}'
        
        #Creats the scan_object and adds the initial values
        scan_object = Scan_Object(table_name, scan_filter_dict, scan_filter_string)
        
        #Checks to see if display filters exist
        if display_filters != "":
            attribute_names = {}
            expression_string = ""
            
            #Loops through filters to confirm there are not missing keys
            for filter in display_filters:
                if attribute_short_key not in filter:
                    assert(f"Errror: [{attribute_name_key}] required for all display_filters.")
                if attribute_name_key not in filter:
                    assert(f"Errror: [{attribute_short_key}] required for all display_filters.")
                        
                attribute_names[attribute_short_key] = attribute_name_key
                expression_string += f'{filter[attribute_short_key]},'
            
            expression_string = expression_string[:-1]
            
            #Creates the expression attribute names and ProjectExpression string
            scan_object.ExpressionAttributeNames = attribute_names
            scan_object.ProjectionExpression = expression_string
        
        #returns the scan_object to initiate the scan
        return scan_object
        
        
        
        