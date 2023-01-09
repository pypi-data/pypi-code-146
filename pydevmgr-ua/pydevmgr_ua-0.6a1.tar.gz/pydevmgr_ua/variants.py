from opcua import ua 
from pydevmgr_ua.register import  register
from valueparser import BaseParser
from typing import Callable
from pydantic import validator

_extra_variants = {
    "INT" : ua.VariantType.Int16 ,
    "DINT" : ua.VariantType.Int32 ,
    "LINT" : ua.VariantType.Int64 ,
    "UINT" : ua.VariantType.UInt16 ,
    "UDINT" : ua.VariantType.UInt32 ,
    "ULINT" : ua.VariantType.UInt64 ,
    "REAL" :  ua.VariantType.Float,
    "LREAL" : ua.VariantType.Double,
    }

def _string_to_variant(s):
    try:
        return getattr(ua.VariantType, s)
    except AttributeError:
        try:
            return _extra_variants[s]
        except KeyError:
            raise ValueError(f"Unknown variant type {s!r}")


@register
class VariantParser(BaseParser):
    class Config(BaseParser.Config):
        type = "Variant"
        variant: ua.VariantType = ua.VariantType.Variant
        py_type: Callable = lambda x:x 
        toto: Callable = float 
        @validator("variant", pre=True, always=True)
        def _validate_variant(cls, value):
            if isinstance(value, str):
                return _string_to_variant(value)
            return value
        
    @staticmethod
    def __parse__(value, config: Config):
        return ua.Variant(config.py_type(value), config.variant)

@register       
class UaInt16(BaseParser, type="UaInt16"):
    """ Parser for Int16 Variant type"""
    @staticmethod
    def __parse__(value, _):
        return ua.Variant(int(value), ua.VariantType.Int16)

@register   
class UaInt32(BaseParser, type="UaInt32"):
    """ parser for Int32 Variant type """
    @staticmethod
    def __parse__(value, _):
        return ua.Variant(int(value), ua.VariantType.Int32)

@register   
class UaInt64(BaseParser, type="UaInt64"):
    """ Parser for Int64 Variant type"""
    @staticmethod
    def __parse__(value, _):
        return ua.Variant(int(value), ua.VariantType.Int64)
   
@register   
class UaUInt16(BaseParser, type="UaUInt16"):
    """ Parser for UInt16 Variant type"""
    @staticmethod
    def __parse__(value, _):
        return ua.Variant(int(value), ua.VariantType.UInt64)
   
@register   
class UaUInt32(BaseParser, type="UaUInt32"):
    """ parser for UInt32 Variant type """
    @staticmethod
    def __parse__(value, _):
        return ua.Variant(int(value), ua.VariantType.UInt32)

@register   
class UaUInt64(BaseParser, type="UaUInt64"):
    """ Parser for UInt64 Variant type"""
    @staticmethod
    def __parse__(value, _):
        return ua.Variant(int(value), ua.VariantType.UInt64)

        
@register   
class UaFloat(BaseParser, type="UaFloat"):
    """ Parser for Float Variant type"""
    @staticmethod
    def __parse__(value, _):
        return ua.Variant(float(value), ua.VariantType.Float)
   
@register   
class UaDouble(BaseParser, type="UaDouble"):
    """ Parser for Double Variant type"""
    @staticmethod
    def __parse__(value, _):
        return ua.Variant(float(value), ua.VariantType.Double)

        
@register   
class UaString(BaseParser, type="UaString"):
    """ Parser for String Variant type"""
    @staticmethod
    def __parse__(value, _):
        return ua.Variant(str(value), ua.VariantType.String)


if __name__ == "__main__":
    print( UaUInt32().parse(4.3))
