class TableNotFoundError(Exception):
    def __init__(self, table_name):
        self.message = f"Table '{table_name}' does not exist"
    
    def __str__(self):
        return self.message

class FieldNotFoundError(Exception):
    def __init__(self, field_name):
        self.message = f"Field '{field_name}' does not exist"
    
    def __str__(self):
        return self.message
