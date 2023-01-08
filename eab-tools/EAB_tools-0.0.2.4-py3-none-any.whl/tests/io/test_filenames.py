"""Tests for file io"""

import pytest

from EAB_tools import (
    sanitize_filename,
    sanitize_xl_sheetname,
)


class TestSanitizeFilename:
    """Test EAB_tools.io.filenames.sanitize_filename"""

    def test_sanitize_filename_very_simple(self) -> None:
        """A (relatively) valid filename should remain untouched."""
        dirty_str = "EAB_tools are cool.csv"
        expected = dirty_str
        assert sanitize_filename(dirty_str) == expected

    def test_sanitize_filename_simple(self) -> None:
        """Basic troublesome chars should be replaced"""
        dirty_str = "EAB_tools are cool?.csv"
        expected = "EAB_tools are cool_.csv"
        assert sanitize_filename(dirty_str) == expected

    def test_sanitize_filename_blank(self) -> None:
        """A blank str should be untouched"""
        assert sanitize_filename("") == ""

    def test_sanitize_filename_dirty_unicode(self) -> None:
        """Special unicode characters should be removed"""
        dirty_str = "foo\0@🐍bar.png"
        assert sanitize_filename(dirty_str) == "foo___bar.png"


class TestSanitizeXlSheetname:
    """Test EAB_tools.io.filenames_sanitize_xl_sheetname"""

    def test_simple(self) -> None:
        """Simple sheetnames can be left as-is"""
        dirty_str = "Sheet 1"
        expected = dirty_str
        assert sanitize_xl_sheetname(dirty_str) == expected

    def test_too_long(self) -> None:
        """Long sheetnames must be truncated to 31 chars or fewer"""
        dirty_str = (
            "This is my sheet name it's a very long sheet name "
            "I wish it could be shorter"
        )
        expected = "name I wish it could be shorter"
        sanitized = sanitize_xl_sheetname(dirty_str)
        assert expected == sanitized and len(sanitized) <= 31

    def test_blank(self) -> None:
        """A worksheet name cannot be left blank"""
        with pytest.raises(ValueError):
            sanitize_xl_sheetname("")

    @pytest.mark.parametrize("sn", ["History", "History", "HiStOrY"])
    def test_history(self, sn: str) -> None:
        """A worksheet cannot have the name 'history', regardless of case"""
        with pytest.raises(ValueError):
            sanitize_xl_sheetname(sn)

    strs = [
        "'This is bad'",
        "this's ok",
        "can't end'",
        "'can't start",
        "this is all good",
        "abba",
    ]

    @pytest.mark.parametrize("sn", strs)
    def test_apostrophe_on_ends(self, sn: str) -> None:
        """The apostrophe cannot be used at the beginning or end of a
        worksheet name, but can be used in the middle of a name"""
        clean = sanitize_xl_sheetname(sn)
        assert clean[0] != "'" and clean[-1] != "'"

    strs = [
        r"No /slashes!",
        r"Of\any kind",
        r"C:\Windows\sys32",
        r"/bin/python3",
        r"No q marks?",
        r"No *****'n stars!",
        r"square =] brackets =[",
        "9:00 AM",
    ]

    @pytest.mark.parametrize("sn", strs)
    def test_illegal_chars(self, sn: str) -> None:
        r"""The following chars are forbidden: \/?*[]:"""
        illegal = list(r"/\?*[]:")
        assert all(bad_char not in sanitize_xl_sheetname(sn) for bad_char in illegal)
