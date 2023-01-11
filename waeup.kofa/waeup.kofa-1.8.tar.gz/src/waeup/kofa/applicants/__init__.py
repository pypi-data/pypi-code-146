"""This package contains everything regarding university applicants.
"""
# Make this a package.
from waeup.kofa.applicants.applicant import (
    Applicant, ApplicantFactory, ApplicantImageStoreHandler,
    ApplicantImageNameChooser,
    )
from waeup.kofa.applicants.container import ApplicantsContainer
from waeup.kofa.applicants.root import ApplicantsRoot
from waeup.kofa.applicants.dynamicroles import (
    ApplicantPrincipalRoleManager,)

__all__ = [
    'Applicant',
    'ApplicantFactory',
    'ApplicantImageNameChooser',
    'ApplicantImageStoreHandler',
    'ApplicantPrincipalRoleManager',
    'ApplicantsContainer',
    'ApplicantsRoot',
    ]
