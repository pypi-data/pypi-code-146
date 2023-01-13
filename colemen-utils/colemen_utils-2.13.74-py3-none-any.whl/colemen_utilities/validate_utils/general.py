# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
'''
    A module of utility methods used for parsing and converting python types.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: type_utils
'''
import re
from typing import Union
import colemen_utilities.dict_utils as _obj
import colemen_utilities.string_utils as _csu

def is_email(value:str)->bool:
    '''
        Determine if the value is an email address.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to validate

        Return {bool}
        ----------------------
        True if it is an email, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:53:20
        `memberOf`: general
        `version`: 1.0
        `method_name`: is_email
        * @xxx [01-06-2023 09:54:06]: documentation for is_email
    '''
    if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',value) is None:
        return False
    return True

def alpha_only(value:str)->bool:
    return False if re.match(r'^[a-zA-Z]*$',value) is None else True


def alphanumeric_only(value:str)->bool:
    return False if re.match(r'^[a-zA-Z0-9]*$',value) is None else True

def is_integer(value:Union[str,int],negatives=True):
    '''
        Determine if the value provided is an integer.

        ----------

        Arguments
        -------------------------
        `value` {str,int}
            The value to validate

        [`negatives`=True] {bool}
            If False, negative numbers are not allowed.

        Return {bool}
        ----------------------
        True if the value is an integer or string containing an integer, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:38:36
        `memberOf`: general
        `version`: 1.0
        `method_name`: is_integer
        * @xxx [01-06-2023 09:39:49]: documentation for is_integer
    '''

    if isinstance(value,(int)):
        if negatives is False:
            if value < 0:
                return False
        return True

    # @Mstep [] determine the appropriate regex to use.
    reg = r'^[0-9]*$'

    if negatives is True:
        reg = r'^[0-9-]*$'


    # @Mstep [IF] if the value is a string.
    if isinstance(value,(str)):
        # @Mstep [] strip leading and trailing spaces.
        value = _csu.strip(value,[" "])
        return False if re.match(reg,value) is None else True

def is_float(value:Union[str,float],negatives=True):
    '''
        Determine if the value provided is a float.

        ----------

        Arguments
        -------------------------
        `value` {str,int}
            The value to validate

        [`negatives`=True] {bool}
            If False, negative numbers are not allowed.

        Return {bool}
        ----------------------
        True if the value is an float or string containing an float, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:38:36
        `memberOf`: general
        `version`: 1.0
        `method_name`: is_float
        * @xxx [01-06-2023 09:39:49]: documentation for is_float
    '''

    if isinstance(value,(int)):
        if negatives is False:
            if value < 0:
                return False
        return True

    if isinstance(value,(str)):

        # @Mstep [] determine the appropriate regex to use.
        reg = r'^[0-9\.]*$'

        if negatives is True:
            reg = r'^[0-9-\.]*$'

        # @Mstep [] strip leading and trailing spaces.
        value = _csu.strip(value,[" "])
        return False if re.match(reg,value) is None else True
    return isinstance(value,(int))

def numeric_only(value:str,negatives=True)->bool:
    '''
        Determine if the value is an integer or float.

        ----------

        Arguments
        -------------------------
        `value` {str,int}
            The value to validate

        [`negatives`=True] {bool}
            If False, negative numbers are not allowed.


        Return {bool}
        ----------------------
        True if the value contains an integer or float, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2023 09:48:24
        `memberOf`: general
        `version`: 1.0
        `method_name`: numeric_only
        * @xxx [01-06-2023 09:49:15]: documentation for numeric_only
    '''
    if is_integer(value,negatives):
        return True
    if is_float(value,negatives):
        return True
    return False
    # return False if re.match(r'^[0-9]*$',value) is None else True

def phone_number(value:str)->bool:
    return False if re.match(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',value) is None else True

# def alpha_only(value:str)->bool:
# def alpha_only(value:str)->bool:

def ip_address(value:Union[str,int])->bool:
    import ipaddress
    try:
        ipaddress.ip_address(value)
        # print("Valid IP Address")
        return True
    except ValueError:
        pass
        # print("Invalid IP Address")
    return False

def future_unix(value:int)->bool:
    '''
        Determine if the value provided is a unix timestamp set in the future.
        ----------


        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-05-2022 13:58:56
        `memberOf`: cerberus
        `version`: 1.0
        `method_name`: future_unix
        * @TODO []: documentation for future_unix
    '''
    import time
    return False if value <= time.time() else True

def past_unix(value:int)->bool:
    '''
        Determine if the value provided is a unix timestamp set in the past.
        ----------


        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-05-2022 13:58:56
        `memberOf`: cerberus
        `version`: 1.0
        `method_name`: past_unix
        * @TODO []: documentation for past_unix
    '''
    import time
    return False if value >= time.time() else True

def to_hash_id(value:str,prefix:str):
    if prefix not in value:
        value= f"{prefix}_{value}"

def crud_type(value:str):
    if isinstance(value,(str)) is False:
        return False
    value = _csu.strip(value,[" "])
    valids = ["create","read","update","delete"]
    if value.lower() not in valids:
        return False
    return True


