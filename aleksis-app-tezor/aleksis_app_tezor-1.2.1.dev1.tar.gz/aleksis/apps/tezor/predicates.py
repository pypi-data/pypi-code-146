from django.contrib.auth import get_user_model

from rules import predicate

from .models.invoice import Invoice

User = get_user_model()


@predicate
def is_own_invoice(user: User, obj: Invoice):
    """Predicate which checks if the invoice is linked to the current user."""
    return obj.get_person() == user.person


@predicate
def has_no_payment_variant(user: User, obj: Invoice):
    """Predicate which checks that the invoice has no payment variant."""
    return not obj.variant


def is_in_payment_status(status: str):
    """Predicate which checks whether the invoice is in a specific state."""

    @predicate
    def _predicate(user: User, obj: Invoice):
        return obj.status == status

    return _predicate


def has_payment_variant(variant: str):
    """Predicate which checks whether the invoice has a specific variant."""

    @predicate
    def _predicate(user: User, obj: Invoice):
        return obj.variant == variant

    return _predicate
