from pydantic import BaseModel, Field, Extra
import datetime as dt
import logging

logger = logging.getLogger(__name__)


class BaseResponseSchema(BaseModel):
    message: str = Field(...)
    errors: dict | None = Field(None)

    def dict(self, *args, **kwargs) -> dict[str, any]:
        kwargs.pop('exclude_none', None)
        return super().dict(*args, exclude_none=True, **kwargs)


class ValidationErrorResponseSchema(BaseModel):
    errors: dict


class ConfigSchema:
    anystr_strip_whitespace = True
    extra = Extra.ignore
    # 'ignore' (default) will silently ignore any extra attributes.
    # 'forbid'           will cause validation to fail if extra attributes are included.
    # 'allow'            will assign the attributes to the model.
    json_encoders = {
        dt.datetime: lambda d: "{:%d %B %Y, %H:%M}".format(d),
        dt.date: lambda d: "{:%b %d, %Y}".format(d),
        float: lambda f: "{:.2f}".format(f)
    }
