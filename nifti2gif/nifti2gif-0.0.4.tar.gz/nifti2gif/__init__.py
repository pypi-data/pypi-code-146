"""For having the version."""

import pkg_resources

__version__ = pkg_resources.require("nifti2gif")[0].version
