from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
# Internal build variable to help choose the correct target code for
# syntactically differing code in AIO and REST builds
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
BUILD_GCLOUD_REST = not __package__ or 'rest' in __package__
