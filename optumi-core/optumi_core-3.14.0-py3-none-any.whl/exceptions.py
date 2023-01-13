##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##


class OptumiException(Exception):
    def __init__(self, message: str):
        super().__init__(
            message
            if message
            else "Optumi encountered an unexpected error - customer support has been notified"
        )


class ServiceException(OptumiException):
    def __init__(self, message: str = None):
        super().__init__(
            message
            if message
            else "Unable to contact Optumi services, please try again later"
        )


class NotLoggedInException(OptumiException):
    def __init__(self, message: str = None):
        super().__init__(
            message if message else "Please use login() to access Optumi services"
        )


class OperationCanceled(OptumiException):
    def __init__(self, message: str, pathToRemove: str = None):
        super().__init__(message)
        self.pathToRemove = pathToRemove


class NoAgreementException(OptumiException):
    def __init__(self, message: str):
        super().__init__(
            message
            if message
            else "Please sign in to portal.optumi.net to review Terms and Conditions of Service"
        )
