"""Test utilities."""
import re

from sphinxcontrib.eval.utils import get_lang_map, replace

TEMPLATE = r"""`!LANG (.*?)`"""


def eval_dummy(input: str) -> str:
    """Eval dummy.

    :param input:
    :type input: str
    :rtype: str
    """
    return str(len(input))


EVAL_FUNCS = {"v": eval_dummy}
CONTENT = """test\n`!v hello`\n"""
PAT = re.compile("`!v (.*?)`", re.M | re.DOTALL)


class Test:
    """Test."""

    def test_get_lang_map(self) -> None:
        """Test get lang map.

        :rtype: None
        """
        rst = get_lang_map(TEMPLATE, EVAL_FUNCS)
        expected = {"v": (PAT, eval_dummy)}
        assert rst == expected

    def test_replace(self) -> None:
        """Test replace.

        :rtype: None
        """
        rst = replace(CONTENT, PAT, eval_dummy)
        expected = "test\n5\n"
        assert rst == expected
