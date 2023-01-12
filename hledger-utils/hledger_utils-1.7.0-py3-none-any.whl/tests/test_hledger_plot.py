# SPDX-FileCopyrightText: 2023 Yann Büchau <nobodyinperson@posteo.de>
# SPDX-License-Identifier: GPL-3.0-or-later

# system modules
import logging
import unittest
import shlex
import subprocess

# internal modules
import hledger_utils

# external modules


logger = logging.getLogger(__name__)


class HledgerPlotTest(unittest.TestCase):
    def test_invocation_script(self):
        subprocess.check_output(shlex.split("hledger-plot --help"))

    def test_invocation_via_python(self):
        subprocess.check_output(
            shlex.split("python -m hledger_utils.commands.plot --help")
        )

    def test_invocation_via_hledger(self):
        subprocess.check_output(shlex.split("hledger plot --help"))
