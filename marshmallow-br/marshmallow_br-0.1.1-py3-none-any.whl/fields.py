# -*- coding: utf-8 -*-
from abc import abstractmethod

from marshmallow.fields import *

from marshmallow_br import validate

__all__ = ("CNH", "CNPJ", "CPF", "Certificate", "Phone")


class Base(String):
    """A base field for documents."""

    def __init__(
        self,
        validator: validate.Validator,
        *args,
        mask: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.mask = mask
        self.validators.insert(0, validator)

    @abstractmethod
    def _mask(self, value: str) -> str:
        ...

    def _validate(self, value: ...) -> str | None:
        if value is None:
            return None
        if not self.validators[0](value):
            raise self.make_error("invalid")
        return value

    def _deserialize(self, value, attr, data, **kwargs) -> str | None:
        value = self._validate(value)
        if value is None:
            return None
        value = "".join([digit for digit in str(value) if digit.isdigit()])
        if self.mask is True:
            return self._mask(value)
        return value


class CNH(Base):
    """A CNH field."""

    default_error_messages = {"invalid": "Not a valid CNH."}

    def __init__(self, *args, **kwargs) -> None:
        validator = validate.CNH(error=self.default_error_messages["invalid"])
        super().__init__(validator, *args, **kwargs)

    def _mask(self, value: str) -> str:
        return value


class CNPJ(Base):
    """A CNPJ field."""

    default_error_messages = {"invalid": "Not a valid CNPJ."}

    def __init__(self, *args, **kwargs) -> None:
        validator = validate.CNPJ(error=self.default_error_messages["invalid"])
        super().__init__(validator, *args, **kwargs)

    def _mask(self, value: str) -> str:
        return f"{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}"


class CPF(Base):
    """A CPF field."""

    default_error_messages = {"invalid": "Not a valid CPF."}

    def __init__(self, *args, **kwargs) -> None:
        validator = validate.CPF(error=self.default_error_messages["invalid"])
        super().__init__(validator, *args, **kwargs)

    def _mask(self, value: str) -> str:
        return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"


class Certificate(Base):
    """A Brazilian birth, marriage and death certificates field."""

    default_error_messages = {"invalid": "Not a valid Brazilian certificate."}

    def __init__(self, *args, **kwargs) -> None:
        validator = validate.Certificate(error=self.default_error_messages["invalid"])
        super().__init__(validator, *args, **kwargs)

    def _mask(self, value: str) -> str:
        return f"{value[:6]}.{value[6:8]}.{value[8:10]}.{value[10:14]}.{value[14]}.{value[15:20]}.{value[20:23]}.{value[23:30]}-{value[30:]}"


class Phone(Base):
    """A Brazilian phone number field."""

    default_error_messages = {"invalid": "Not a valid Brazilian phone number."}

    def __init__(
        self,
        *args,
        require_ddi: bool | None = None,
        require_ddd: bool | None = None,
        **kwargs,
    ) -> None:
        validator = validate.Phone(
            require_ddi=require_ddi,
            require_ddd=require_ddd,
            error=self.default_error_messages["invalid"],
        )
        super().__init__(validator, *args, **kwargs)

    def _mask(self, value: str) -> str:
        validator: validate.Phone = self.validators[0]
        _match = validator.REGEX.match(value)
        ddi = f"+{_match.group(1)}" if _match.group(1) else ""
        ddd = f"({_match.group(2)})" if _match.group(2) else ""
        number = f"{_match.group(3)}-{_match.group(4)}"
        return " ".join([ddi, ddd, number]).strip()

    def _deserialize(self, value, attr, data, **kwargs) -> str | None:
        value = self._validate(value)
        if value is None:
            return None
        if self.mask is True:
            return self._mask(value)
        value = "".join([digit for digit in str(value) if digit.isdigit()])
        return value
