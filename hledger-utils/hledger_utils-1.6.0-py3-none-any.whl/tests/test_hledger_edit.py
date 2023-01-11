# SPDX-FileCopyrightText: 2023 Yann Büchau <nobodyinperson@posteo.de>
# SPDX-License-Identifier: GPL-3.0-or-later

# system modules
import unittest
import itertools
import os
import tempfile
import shlex
import logging
from contextlib import contextmanager

# internal modules
import hledger_utils

# external modules
import rich

logger = logging.getLogger(__name__)


@contextmanager
def environment(**env):
    old_values = {k: os.environ.get(k) for k in env}
    os.environ.update(env)
    yield
    for k, v in old_values.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


@contextmanager
def nothing():
    yield


class HledgerEditTest(unittest.TestCase):
    def assert_hledger_edit(
        self,
        content,
        editor,
        expected_result,
        query="",
        allowed_exitcodes=None,
    ):
        try:
            with (
                nothing()
                if allowed_exitcodes is None
                else self.assertRaises(SystemExit)
            ) as cm:
                files = {
                    tempfile.mkstemp(
                        prefix="hledger-edit-test-",
                        suffix=".hledger",
                    )[1]: c
                    for c in zip(
                        ([content] if isinstance(content, str) else content),
                        (
                            [expected_result]
                            if isinstance(expected_result, str)
                            else expected_result
                        ),
                    )
                }

                for tmpfilePath, (content, expected) in files.items():
                    with open(tmpfilePath, "w") as fh:
                        fh.write(content)
                        fh.flush()
                with environment(
                    EDITOR=editor,
                    VISUAL=editor,
                    HLEDGER_EDIT_LOGLEVEL="CRITICAL",
                    HLEDGER_EDIT_NOTTY="yes",
                ):
                    hledger_utils.commands.edit.cli(
                        list(
                            itertools.chain.from_iterable(
                                ("-f", f) for f in files
                            )
                        )
                        + shlex.split(query)
                        if isinstance(query, str)
                        else query
                    )
                for i, (tmpfilePath, (content, expected)) in enumerate(
                    files.items(), start=1
                ):
                    with open(tmpfilePath) as fh:
                        self.assertEqual(
                            fh.read(),
                            expected,
                            f"File {i} ({tmpfilePath!r}) has wrong content after hledger-edit",
                        )
            if allowed_exitcodes is not None:
                self.assertIn(cm.exception.code, allowed_exitcodes)
        except SystemExit as e:
            if allowed_exitcodes is not None:
                self.assertIn(e.code, allowed_exitcodes)
        finally:
            try:
                for tmpfilePath in files:
                    try:
                        logger.debug(f"🗑️  Removing {tmpfilePath!r}")
                        os.remove(tmpfilePath)
                    except (OSError, FileNotFoundError):
                        logger.exception(
                            f"Couldn't remove tempfile {tmpfilePath}"
                        )
            except Exception:
                logger.exception(f"Couldn't remove tempfiles")

    def test_hledger_edit_single(self):
        self.assert_hledger_edit(
            content=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food
""",
            editor="perl -pi -e 's|Cost:|COST:|g'",
            expected_result=f"""
2022-12-12  Food
    Cash        -10 €
    COST:Food
""",
        )

    def test_hledger_edit_single_strip(self):
        self.assert_hledger_edit(
            content=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food
""".strip(),
            editor="perl -pi -e 's|Cost:|COST:|g'",
            expected_result=f"""
2022-12-12  Food
    Cash        -10 €
    COST:Food
""".strip(),
        )

    def test_hledger_edit_single_add_newline_above(self):
        self.assert_hledger_edit(
            content=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food
""",
            editor=r"perl -pi -e 's|^(2022)|\n$1|g'",
            expected_result=f"""

2022-12-12  Food
    Cash        -10 €
    Cost:Food
""",
        )

    def test_hledger_edit_single_add_newline_below(self):
        self.assert_hledger_edit(
            content=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food
""",
            editor=r"perl -pi -e 's|(:Food)|$1\n|g'",
            expected_result=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food

""",
        )

    def test_hledger_edit_single_many_newlines(self):
        self.assert_hledger_edit(
            content=f"""




2022-12-12  Food
    Cash        -10 €
    Cost:Food




""",
            editor="perl -pi -e 's|Cost:|COST:|g'",
            expected_result=f"""




2022-12-12  Food
    Cash        -10 €
    COST:Food




""",
        )

    def test_hledger_edit_two_files_with_one_tx_each(self):
        self.assert_hledger_edit(
            content=[
                f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food
""",
                f"""
2022-12-13  Drink
    Cash        -5 €
    Cost:Drink
""",
            ],
            editor="perl -pi -e 's|Cost:|COST:|g'",
            expected_result=[
                f"""
2022-12-12  Food
    Cash        -10 €
    COST:Food
""",
                f"""
2022-12-13  Drink
    Cash        -5 €
    COST:Drink
""",
            ],
        )

    def test_hledger_edit_one_of_two_files_with_one_tx_each(self):
        self.assert_hledger_edit(
            content=[
                f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food
""",
                f"""
2022-12-13  Drink
    Cash        -5 €
    Cost:Drink
""",
            ],
            editor="perl -pi -e 's|Drink|Beverage|g'",
            expected_result=[
                f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food
""",
                f"""
2022-12-13  Beverage
    Cash        -5 €
    Cost:Beverage
""",
            ],
        )

    def test_hledger_edit_last_tx_in_big_file(self):
        self.assert_hledger_edit(
            content=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food

2022-12-13  Drink
    Cash        -5 €
    Cost:Drink

2022-12-14  Sweets
    Cash        -3 €
    Cost:Sweets
""",
            editor="perl -pi -e 's|Cost:Sweets|Cost:Yummy|g'",
            expected_result=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food

2022-12-13  Drink
    Cash        -5 €
    Cost:Drink

2022-12-14  Sweets
    Cash        -3 €
    Cost:Yummy
""",
        )

    def test_hledger_edit_first_tx_in_big_file(self):
        self.assert_hledger_edit(
            content=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food

2022-12-13  Drink
    Cash        -5 €
    Cost:Drink

2022-12-14  Sweets
    Cash        -3 €
    Cost:Sweets
""",
            editor="perl -pi -e 's|2022-12-12|2022-12-10|g'",
            expected_result=f"""
2022-12-10  Food
    Cash        -10 €
    Cost:Food

2022-12-13  Drink
    Cash        -5 €
    Cost:Drink

2022-12-14  Sweets
    Cash        -3 €
    Cost:Sweets
""",
        )

    def test_hledger_edit_middle_tx_in_big_file(self):
        self.assert_hledger_edit(
            content=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food

2022-12-13  Drink
    Cash        -5 €
    Cost:Drink

2022-12-14  Sweets
    Cash        -3 €
    Cost:Sweets
""",
            editor="perl -pi -e 's|Cost:Drink|Cost:Beverages|g;s|2022-12-13|2022-12-15|g'",
            expected_result=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food

2022-12-15  Drink
    Cash        -5 €
    Cost:Beverages

2022-12-14  Sweets
    Cash        -3 €
    Cost:Sweets
""",
        )

    def test_hledger_edit_all_tx_in_big_file(self):
        self.assert_hledger_edit(
            content=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food

2022-12-13  Drink
    Cash        -5 €
    Cost:Drink

2022-12-14  Sweets
    Cash        -3 €
    Cost:Sweets
""",
            editor="perl -pi -e 's|Cash|Mash|g'",
            expected_result=f"""
2022-12-12  Food
    Mash        -10 €
    Cost:Food

2022-12-13  Drink
    Mash        -5 €
    Cost:Drink

2022-12-14  Sweets
    Mash        -3 €
    Cost:Sweets
""",
        )

    def test_hledger_edit_forecasted_not_edited(self):
        self.assert_hledger_edit(
            content=f"""
2022-12-12  Food
    Cash        -10 €
    Cost:Food

~ monthly    Snacks
    Cash                -20 €
    Cost:Food:Snacks
""",
            editor="perl -pi -e 's|Snacks|SNAACKSSSSS!!!|g;s|10 €|30 €|g'",
            query="--forecast",
            expected_result=f"""
2022-12-12  Food
    Cash        -30 €
    Cost:Food

~ monthly    Snacks
    Cash                -20 €
    Cost:Food:Snacks
""",
        )
