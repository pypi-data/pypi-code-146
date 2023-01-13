# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import json
import time
import datetime
import re

# from apricity_labs import main as _main
from cerberus import Validator
import colemen_utilities.dict_utils as _obj

def single_value(field,schema:dict,value):
    '''
        validate a value using the cerberus library
        ----------

        Arguments
        -------------------------
        `field` {str}
            The field name to validate.

        `schema` {dict}
            A dictionary of validation rules to use.

            {
                'type': 'string',
                'empty': False,
                'nullable': False,
                'required': True,
                'minlength': 3,
                'maxlength': 255,
            }

        `value` {any}
            The value to be validated.

        Return {tuple}
        ----------------------
        (result,Validator)

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 11-23-2022 08:47:13
        `memberOf`: cerberus
        `version`: 1.0
        `method_name`: single_value
        * @TODO []: documentation for single_value
    '''
    vdict = {field:value}
    if field not in schema:
        schema = {field:schema}
    sdict = {field:schema[field]}
    return validate_from_schema(sdict,vdict)


def validate_from_schema(schema:dict,value:dict,**kwargs):
    # ra = _result.Result()
    # print("schema:")
    # print(schema)
    errors = {}
    purge_unknown =_obj.get_kwarg(['purge_unknown'],True,(bool),**kwargs)
    v = Validator(schema,purge_unknown=purge_unknown)
    output_data = {}
    success = v.validate(value)
    if success is False:
        for field,val in v.errors.items():
            if field not in errors:
                errors[field] = []
            errors[field].append(val[0])
    else:
        for field,val in v.document.items():
            output_data[field] = val
        
        # print(v.__dict__)
        # print(v.document)


    # ra.set_key('errors',errors)
    return success,errors,output_data



def is_email(field,value,error):
    from colemen_utilities.validate_utils.general import is_email
    if is_email(value) is False:
        error(field,"invalid email")

def alpha_only(field,value,error):
    from colemen_utilities.validate_utils.general import alpha_only
    if alpha_only(value) is False:
        error(field,"non alphabetic characters")

def alphanumeric_only(field,value,error):
    from colemen_utilities.validate_utils.general import alphanumeric_only
    if alphanumeric_only(value) is False:
        error(field,"non alphanumeric characters")

def numeric_only(field,value,error):
    from colemen_utilities.validate_utils.general import numeric_only
    if numeric_only(value) is False:
        error(field,"non-numeric characters")

def phone_number(field,value,error):
    from colemen_utilities.validate_utils.general import phone_number
    if phone_number(value) is False:
        error(field,"invalid phone number")

def ip_address(field,value,error):
    from colemen_utilities.validate_utils.general import ip_address
    if ip_address(value) is False:
        error(field,"Invalid IP Address")

def future_unix(field,value,error):
    from colemen_utilities.validate_utils.general import future_unix
    if future_unix(value) is False:
        error(field,"Timestamp in the past.")

def past_unix(field,value,error):
    from colemen_utilities.validate_utils.general import past_unix
    if past_unix(value) is False:
        error(field,"Timestamp in the future.")

def coerce_current_timestamp(value):
    return datetime.datetime.now(tz=datetime.timezone.utc)


