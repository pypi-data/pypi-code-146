"""This package contains everything regarding temporary jobs (mandates).
"""
# Make this a package.
from waeup.kofa.mandates.container import MandatesContainer
from waeup.kofa.mandates.mandate import Mandate

__all__ = [
    'MandatesContainer',
    'Mandate',
    ]
