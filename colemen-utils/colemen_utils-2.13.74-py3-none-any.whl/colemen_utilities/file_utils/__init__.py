# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
'''
    A module of utility methods used for manipulating files locally or over FTP.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: dtstamp
    `memberOf`: file_utils
'''

import colemen_utilities.file_utils.file_read as read
import colemen_utilities.file_utils.file_write as writer
import colemen_utilities.file_utils.file_image as image
import colemen_utilities.file_utils.file_convert as convert
import colemen_utilities.file_utils.file_search as search
import colemen_utilities.file_utils.file_compression as compress

# import colemen_utilities.file_utils.file_string_facade
# from colemen_utilities.string_utils import windows_file_name as format_windows_file_name
# from colemen_utilities.string_utils import extension as format_extension
# from colemen_utilities.string_utils import file_path as format_file_path
# from colemen_utilities.string_utils import url as format_url


# import colemen_utilities.file_utils.file_read
# import colemen_utilities.file_utils.file_write
# import colemen_utilities.file_utils.file_image
# import colemen_utilities.file_utils.file_convert
# import colemen_utilities.file_utils.file_search
# import colemen_utilities.file_utils.file_compression

from colemen_utilities.file_utils.file_read import *
from colemen_utilities.file_utils.file_write import *
from colemen_utilities.file_utils.file_image import *
from colemen_utilities.file_utils.file_convert import *
from colemen_utilities.file_utils.file_search import *
from colemen_utilities.file_utils.file_compression import *

# from colemen_utilities.file_utils.File import *
from colemen_utilities.file_utils.file_utils import *
from colemen_utilities.file_utils.resources import *
import colemen_utilities.file_utils.exiftool as _exiftool



