
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
from kraken_datatype import _datatype_text
from kraken_datatype import _guess_engine




def validate(datatype, data):
    """Returns True if valid datatype, None if can't figure out
    """

    _data = _datatype_data.normalize(data)

    _datatype = _datatype_datatype.normalize(datatype)

    if not _data or not _datatype:
        return None


    module_name = '_datatype_' + _datatype 
    
    result = globals()[module_name].validate(_data)

    return result


def normalize(datatype, data):

    _data = _datatype_data.normalize(data)

    _datatype = _datatype_datatype.normalize(datatype)

    if not _data or not _datatype:
        return None

    module_name = '_datatype_' + _datatype 
    
    result = globals()[module_name].normalize(_data)

    return result


def guess(data):

    _data = _datatype_data.normalize(data)
    
    return _guess_engine.guess(_data)



    