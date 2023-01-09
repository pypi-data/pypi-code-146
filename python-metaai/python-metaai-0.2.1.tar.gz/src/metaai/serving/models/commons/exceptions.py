from fastapi import HTTPException


class ServingHttpError(HTTPException):
    pass
