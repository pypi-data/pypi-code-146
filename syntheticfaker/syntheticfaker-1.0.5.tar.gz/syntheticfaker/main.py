from syntheticfaker import varchar
from syntheticfaker import integer
import pandas as pd
import yaml
import os


class main_data:
    
    def __init__(self,location, number):
        
        self.meta_df = pd.DataFrame()
        
        self.number = number
        self.location = location
        
        self.field_object = self.fields_load
        self.metadata_objects = self.metadata_load
        
        self.synthesise(self.field_object(),self.metadata_objects())
        
        
    def fields_load(self):
        
        field_list=[]
        with open(self.location, 'r') as con:
            connection=yaml.safe_load(con)

        try:
            for fields in connection['fields']: 
                field_list.append(fields)
            return (field_list)
        except:
            print('No fields section in yaml file')
            
          
    def metadata_load(self): 
         
        with open(self.location, 'r') as con:
            connection=yaml.safe_load(con)
        try:
            for meta in connection['metadata']: 
                return (dict(connection['metadata'][meta]))
        except:
            print('No metadata section in yaml file')
            
    def data_dict_load(self,file_name):
        try:
            this_dir, this_filename = os.path.split(__file__)
            DATA_PATH = os.path.join(this_dir+"/data",file_name+".yaml")

            with open(DATA_PATH, 'r') as con:
                 data_dicts=yaml.safe_load(con)

            return data_dicts
        
        except:
            data_dicts=dict()
            return data_dicts
    
    def synthesise(self,field_object,metadata_dict): 

        with open(self.location, 'r') as con:
            connection=yaml.safe_load(con)
        
        for column in metadata_dict:
            data_dict = self.data_dict_load(connection['fields'][column] ) 
            
            if metadata_dict[column].lower() == 'varchar' :
                vr_data = varchar.varchar_fake_data(self.number,field_object, column, connection, data_dict)
                vr_fake_data = vr_data.varchar_fake()
                self.meta_df.insert(0,column,vr_fake_data) 
                
                
            elif metadata_dict[column].lower() == 'integer' or  metadata_dict[column].lower() == 'number':
                ir_data = integer.integer_fake_data(self.number,field_object, column, connection, data_dict)
                ir_fake_data = ir_data.integer_fake()
                self.meta_df.insert(0,column,ir_fake_data) 
                
    def get_data(self):
        return self.meta_df
                
        