from pydantic import BaseModel
from .info import InfoSuccess, InfoWarning, InfoError
from typing import Union, List, Dict


class ResponseSuccess(BaseModel):
    info: InfoSuccess = InfoSuccess()
    data: Union[List, Dict]


class ResponseWarning(BaseModel):

    info: InfoWarning = InfoWarning()
    data: Union[List, Dict]

    @classmethod
    def set(cls, warnings, data):

        return cls(
            info=InfoWarning(warnings=warnings),
            data=data
        )


class ResponseError(BaseModel):
    info: InfoError = InfoError()

    @classmethod
    def set(cls, errors, warnings=[]):
        return cls(
            info=InfoError(
                warnings=warnings,
                errors=errors
            )
        )
