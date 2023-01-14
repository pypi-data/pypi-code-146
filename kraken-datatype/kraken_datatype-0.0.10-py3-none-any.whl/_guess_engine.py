from kraken_datatype import _datatype_datatype
from kraken_datatype import _datatype_bool 
from kraken_datatype import _datatype_address 
from kraken_datatype import _datatype_country 
from kraken_datatype import _datatype_date
from kraken_datatype import _datatype_data
from kraken_datatype import _datatype_domain
from kraken_datatype import _datatype_email
from kraken_datatype import _datatype_telephone
from kraken_datatype import _datatype_url

import datetime

def guess(data):

    if isinstance(data, datetime.datetime):
        return _guess_datetime(data)

    elif isinstance(data, int):
        return _guess_int(data)

    elif isinstance(data, str):
        return _guess_str(data)


def _guess_datetime(data):

    if _datatype_date.validate(data):
        return 'date'
    
    return None


def _guess_int(data):

    return 'int'


def _guess_str(data):

    if _datatype_url.validate(data):
        return 'url'
    
    if _datatype_email.validate(data):
        return 'email'

    if _datatype_country.validate(data):
        return 'country'

    if _datatype_bool.validate(data):
        return 'bool'

    if _datatype_telephone.validate(data):
        return 'telephone'

    if _datatype_date.validate(data):
        return 'date'

    return None