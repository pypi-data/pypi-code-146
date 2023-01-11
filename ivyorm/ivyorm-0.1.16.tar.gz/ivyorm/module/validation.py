from .util import Console

class Validation:


    

    def __init__(self, schemaFile):
        Console.info('Validation instance.................')

        self.model = {}
        self.field_spec = {}
        self.table_spec = {}
        self.database_spec = {}

    '''
    returns a list of fields that exist from a str or list input of fields
    '''
    def fieldExists(self, field: str or list):

        field_copy: list = []
        if type(field) == str:
            field_copy.append(field)
            field = field_copy
        elif type(field) == list:
            field_copy: list = field
        else:
            return    


        for key in list(field):
            if key not in self.field_spec:
                field_copy.remove(key)

        return field_copy


    def check(self, dataDict: dict):
        errorDict = {}

        for field in self.field_spec:
            for operation, operation_value in self.field_spec[field]['back'].items():
                do = f"_check_{operation}"
                data_value = dataDict.get(field, None)

                if hasattr(self, do) and callable(func := getattr(self, do)):
                    dataDict[field], error = func(operation_value, data_value)

                    if error is not None:
                        errorDict[field] = error
                else:
                    # function not found
                    pass

        return dataDict, errorDict
        
    
    def _check_type(self, option, value:any):
        if value is None:
            return None, None

        error = None

        match option:
            case 'char':
                pass

            case 'varchar':
                value = value.strip()

            case 'var':
                value = value.strip()

            case 'integer':
                if type(value) is int:
                    pass
                else:
                    error = 'A numeric value is required'

            case 'int':
                if type(value) is int:
                    pass
                else:
                    error = 'A numeric value is required (int)'

            case 'decimal':
                if type(value) is int:
                    pass
                else:
                    error = 'A numeric value is required'

            case 'float':
                if type(value) is float:
                    pass
                else:
                    error = 'A float is required'

        return value, error


    def _check_size(self, option, value:any):
        if value is None:
            return None, None

        error = None
        return value, error


    def _check_auto(self, option, value:any):
        if value is None:
            return None, None

        error = None
        return value, error


    def _check_required(self, option, value:any):
        error = None

        if option is True and value is None:
            error = 'A value is required'
        
        return value, error


    def _check_arraytouse(self, option, value:any):
        if value is None:
            return None, None

        error = None
        return value, error


    def _check_default(self, option, value:any):
        if value is None:
            return None, None

        error = None
        return value, error