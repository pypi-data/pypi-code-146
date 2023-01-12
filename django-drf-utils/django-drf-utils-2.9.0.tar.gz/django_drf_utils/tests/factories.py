import factory

from django.db.models import signals
from django.dispatch import Signal


@factory.django.mute_signals(
    *[var for var in vars(signals).values() if isinstance(var, Signal)]
)
class DjangoModelFactoryNoSignals(factory.django.DjangoModelFactory):
    """Extends DjangoModelFactory by preventing all side-effects due to Django
    signals. Useful to make tests behavior more predictable"""
