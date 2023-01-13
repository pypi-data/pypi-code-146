from dataclasses import Field,dataclass

@dataclass
class FieldInput:
    field_val : str
    field_name : str = None
    
def collect_input(field : Field,is_valid_fxn=None):
    is_valid_input = False
    new_val=''
    while not is_valid_input:
        new_val=input(f'{field.name}: ')
        if is_valid_fxn is None:
            is_valid_input=True
        else:
            is_valid_input=is_valid_fxn(FieldInput(field_name=field.name,field_val=new_val))
    return new_val
    
def is_valid_non_empty(field_input : FieldInput):
    field_val = field_input.field_val
    if field_val is None or field_val=='':
        return False
    return True