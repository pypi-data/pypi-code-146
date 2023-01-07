# -*- coding: utf-8 -*-
# :Project:   SoL -- SoL2 compatibility test
# :Created:   sab 07 lug 2018 12:13:18 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Lele Gaifax
#

from os import fspath
from pathlib import Path

from sol.models.bio import load_sol


def test_load(session):
    testdir = Path(__file__).parent.parent
    fullname = testdir / 'scr' / 'Mouraly-2016-03-19+6.sol'
    tourneys, skipped = load_sol(session, fspath(fullname))
    assert len(tourneys) == 1
    assert skipped == 0
