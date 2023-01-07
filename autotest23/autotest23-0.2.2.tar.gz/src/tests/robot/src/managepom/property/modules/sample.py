
from testdata.abstract.test_data import TestData

class Sample(TestData):
        
    def display_all_data(self):
        print("This is Sample file for testing only")
    
    def variable_validator(self, first_row_value: str):
        return super().variable_validator(first_row_value)
        
    def variable_converter(self, first_row_value: str):
        return super().variable_converter(first_row_value)
    
    def get_all_data(self):
        print("This is Sample file for testing only")
        
    def arrange_data_set(self, arrange_type: str):
        print("This is Sample file for testing only")
    
    def get_data_by_column(self, column_name: str):
        print("This is Sample file for testing only")
    
    def get_data_with_condition(self, column_name: str, condition: str, operator: str):
        print("This is Sample file for testing only")