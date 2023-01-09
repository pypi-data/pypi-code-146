from typing import Any
from enum import Enum

class GeneralEnum(Enum):
    
    __aliases__ = {
    }

    @classmethod
    def on_parse_exception(cls, expr:str):
        options = cls.get_members()
        raise RuntimeError(f"invalid option \"{expr}\" for the enum class \"{cls.__name__}\" "
                           f"(allowed options: {', '.join(options)})")
    
    @classmethod
    def parse(cls, expr:str):
        if isinstance(expr, cls):
            return expr
        elif isinstance(expr, int):
            return cls(expr)
        _expr = expr.strip().lower()
        members = cls.get_members_map()
        if _expr in members:
            return cls(members[_expr])
        else:
            # check aliases
            aliases = cls.get_aliases_map()
            if _expr in aliases:
                return cls(cls.parse(aliases[_expr]))
        cls.on_parse_exception(expr)
            
    @classmethod
    def get_members(cls):
        return [i.lower() for i in cls.__members__]
    
    @classmethod
    def get_members_map(cls):
        return {k.lower():v for k, v in cls.__members__.items()}
    
    @classmethod
    def get_aliases_map(cls):
        return {k.lower():v for k, v in cls.__aliases__.items()}
    
    @classmethod
    def has_member(cls, name:str):
        return name in cls.__members__
    
    @classmethod
    def get_member_by_attribute(cls, attribute:str, value:Any):
        members = cls.__members__
        return next((x for x in members.values() if getattr(x, attribute) == value), None)
    
class DescriptiveEnum(GeneralEnum):
    
    def __new__(cls, value:int, description:str=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def on_parse_exception(cls, expr:str):
        enum_descriptions = "".join([f"    {key.lower()} - {val.description}\n" \
                                     for key, val in cls.__members__.items()])
        raise RuntimeError(f"invalid option \"{expr}\" for the enum class \"{cls.__name__}\"\n"
                           f"  Allowed options:\n{enum_descriptions}")