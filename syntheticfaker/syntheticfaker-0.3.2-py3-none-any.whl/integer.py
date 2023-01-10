from faker import Faker
import random

fake = Faker()

class integer_fake_data:
    
    def __init__(self, num, field_object,column, field_name, data_dict):
        
        self.num = num
        self.field_object = field_object
        self.column = column
        self.field_name = field_name
        self.data_dict=data_dict
        self.number_list = []

    def my_lib(code):
        return random.choice(data_dict['model'][code])

    def integer_fake(self):
        
        for n in range(self.num):
            if self.column not in self.field_object:
                self.number_list.append(fake.random_number())
                
            elif self.field_name['fields'][self.column] == 'harcoded_value':
                hard_code=self.field_name['constraints'][self.column]
                self.number_list.append(hard_code)
                
            elif self.field_name['fields'][self.column] == 'random_number':
                length=self.field_name['constraints'][self.column]['digits']
                self.number_list.append(fake.random_number(digits=length))
                
            elif self.field_name['fields'][self.column] == 'barcode13':
                self.number_list.append(fake.ean13())
                
            elif self.field_name['fields'][self.column] == 'barcode8':
                self.number_list.append(fake.ean8())    
                
            elif self.field_name['fields'][self.column] == 'credit_card_number':
                self.number_list.append(fake.credit_card_number())  
                
            elif self.field_name['fields'][self.column] == 'day_of_month':
                self.number_list.append(fake.day_of_month()) 
                
            elif self.field_name['fields'][self.column] == 'month':
                self.number_list.append(fake.month()) 
                
            elif self.field_name['fields'][self.column] == 'phone_number':
                self.number_list.append(fake.msisdn())
                
            elif self.field_name['fields'][self.column] == 'float_number':
                self.number_list.append(fake.pyfloat())
                
            elif self.field_name['fields'][self.column] == 'decimal_number':
                self.number_list.append(fake.pydecimal())
            
            elif self.field_name['fields'][self.column] == 'random_int':
                minimum=self.field_name['constraints'][self.column]['min']
                maximum=self.field_name['constraints'][self.column]['max']
                steps=self.field_name['constraints'][self.column]['step']
                self.number_list.append(fake.random_int(min=minimum, max=maximum, step=steps))
                    
            elif self.field_name['fields'][self.column] == 'day_of_month':
                self.number_list.append(fake.day_of_month())
                
            elif self.field_name['fields'][self.column] == 'barcode13':
                self.number_list.append(fake.ean13())
                
            elif self.field_name['fields'][self.column] == 'barcode8':
                self.number_list.append(fake.ean8())    
                
            elif self.field_name['fields'][self.column] == 'credit_card_number':
                self.number_list.append(fake.credit_card_number())  
                
            elif self.field_name['fields'][self.column] == 'month':
                self.number_list.append(fake.month()) 
                
            elif self.field_name['fields'][self.column] == 'phone_number':
                self.number_list.append(fake.msisdn())
                
            elif self.field_name['fields'][self.column] == 'float_number':
                self.number_list.append(fake.pyfloat())
                
            elif self.field_name['fields'][self.column] == 'decimal_number':
                self.number_list.append(fake.pydecimal())
                    
        return (self.number_list)


