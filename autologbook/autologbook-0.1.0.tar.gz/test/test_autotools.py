#  Copyright (c) 2022.  Antonio Bulgheroni.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from configparser import ConfigParser, MissingSectionHeaderError

import pytest

from autologbook.autoerror import NotAValidConfigurationFile
from autologbook.autotools import generate_default_conf, safe_configread


def test_generate_default_conf():
    config = generate_default_conf()
    assert isinstance(config, ConfigParser)


def test_safe_configread():
    default_config = generate_default_conf()

    with pytest.raises(TypeError):
        # reading a file without name (None)
        safe_configread(conffile=None)

    with pytest.raises(MissingSectionHeaderError):
        # reading an invalid file
        safe_configread(__file__)

    # write an empty configuration file
    empty_config = ConfigParser()
    empty_config_filename = 'empty_config.ini'
    empty_config.write(empty_config_filename)

    # safe_read the empty configuration file
    with pytest.raises(NotAValidConfigurationFile):
        read_config = safe_configread(empty_config_filename)
