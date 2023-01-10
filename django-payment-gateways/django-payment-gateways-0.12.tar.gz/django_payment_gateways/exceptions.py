from django.db import IntegrityError


class InsufficientBalance(IntegrityError):
    """Raised when a wallet has insufficient balance to
    run an operation.
    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """


class DriverNotFoundException(Exception):
    """Driver not selected or default driver does not exist."""


class InvoiceNotFoundException(Exception):
    """invoice not found"""


class PurchaseFailedException(Exception):
    """purchase failed"""


class InvalidPaymentException(Exception):
    """invalid payment"""
