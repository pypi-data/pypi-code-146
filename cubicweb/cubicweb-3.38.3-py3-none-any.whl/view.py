from cubicweb_web.view import *  # noqa

from logilab.common.deprecation import (
    TargetMovedDeprecationWarning,
    DeprecationWarningKind,
    send_warning,
)

send_warning(
    'the module "cubicweb.view" is deprecated and has been moved to the cubicweb_web cube, '
    'install it and use "cubicweb_web.view" instead',
    TargetMovedDeprecationWarning,
    deprecation_class_kwargs={
        "kind": DeprecationWarningKind.MODULE,
        "old_name": "view",
        "new_name": "view",
        "old_module": "cubicweb.view",
        "new_module": "cubicweb_web.view",
    },
    stacklevel=3,
    version="3.38",
    module_name="cubicweb",
)
