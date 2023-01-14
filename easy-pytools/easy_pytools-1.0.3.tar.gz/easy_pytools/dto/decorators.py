from ._internal import *


def transfer_object(cls: ClassVar):
    fields = public_fields(cls)
    for name, value in fields.items():
        if (cname := contr_name(name)) not in cls.__dict__:
            if isinstance(value, tuple) and len(value) >= 2:
                setattr(cls, cname, value[0])
                setattr(cls, name, value[1])
            else:
                setattr(cls, cname, f'{name}')
                setattr(cls, name, value)
        else:
            setattr(cls, name, value)

        if (ctype := contr_type(name)) not in cls.__dict__:
            setattr(cls, ctype, type(cls.__dict__[name]))

        if isinstance(value, tuple) and len(value) >= 3:
            setattr(cls, allowed_values(name), value[2])
        elif (alname := allowed_values(name)) not in cls.__dict__:
            setattr(cls, alname, tuple())

    cls.get_contract = get_contract
    cls.as_dict = public_fields
    cls.set_value = set_value
    cls.write_tuple = write_tuple
    cls.__setattr__ = set_value
    cls.__init__ = contract_init

    return cls



