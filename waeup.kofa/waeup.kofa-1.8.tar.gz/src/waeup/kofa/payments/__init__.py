"""This package contains everything regarding payments.
"""
# Make this a package.
from waeup.kofa.payments.container import PaymentsContainer
from waeup.kofa.payments.payment import OnlinePayment

__all__ = [
    'PaymentsContainer',
    'OnlinePayment',
    ]
