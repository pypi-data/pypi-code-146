import sys
from argparse import Namespace
from unittest.mock import patch

import gb_lib.GbLib as lib


def test_parse_with_no_args():
    test_sys_argv = ['prog']
    try:
        with patch.object(sys, "argv", test_sys_argv):
            ap = lib.GbParserBase()
            ap.add_argument("--dummy", nargs='?', default=lib.GbParserBase.NO_ARG_GIVEN)
            ap.init()
    except ValueError as ve:
        si = sys.exc_info()
        assert "when no values given on command line" in si[1].args[0]

def test_parse_with_args():
    test_sys_argv = ['prog', 'some_value']
    with patch.object(sys, "argv", test_sys_argv):
        ap = lib.GbParserBase()
        ap.add_argument("dummy", nargs='?', default=lib.GbParserBase.NO_ARG_GIVEN)
        parsed_args: Namespace = ap.init()
        assert parsed_args.dummy



