"""
Access codes are special objects used for identifying users. Each
access code has a portal-wide unique number.

Main content components are defined in
:mod:`waeup.kofa.accesscodes.accesscode`. This subpackage also
provides a _catalog_ to lookup any access code quickly and a
_workflow_ to guarantee consistent states and transitions when dealing
with it.

We also provide UI components to generate, archive, import and
reimport access codes or batches thereof. These parts are defined in
:mod:`waeup.kofa.accesscodes.browser`.

The interfaces of this subpackage are defined in
:mod:`waeup.kofa.accesscodes.interfaces`.
"""
from waeup.kofa.accesscodes.accesscode import (
    get_access_code, invalidate_accesscode, disable_accesscode,
    reenable_accesscode, create_accesscode,
    AccessCode, AccessCodeBatch, AccessCodeBatchContainer)

# Public API of this submodule
__all__ = [
    'AccessCodeBatchContainer',
    'AccessCodeBatch',
    'AccessCode',
    'get_access_code',
    'invalidate_accesscode',
    'disable_accesscode',
    'reenable_accesscode',
    'create_accesscode',
    ]
