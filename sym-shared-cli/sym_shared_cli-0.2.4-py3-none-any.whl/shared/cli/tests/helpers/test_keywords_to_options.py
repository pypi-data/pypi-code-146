import shlex

from sym.shared.cli.helpers.keywords_to_options import Argument, keywords_to_options


def _assert_cmdline(expected: str, *args: Argument) -> None:
    assert keywords_to_options(args) == shlex.split(expected)


def test_no_args_pass_through() -> None:
    _assert_cmdline("")


def test_str_args_pass_through() -> None:
    _assert_cmdline("foo bar", "foo", "bar")


def test_mapping_args_with_str_values() -> None:
    _assert_cmdline("--foo bar --baz qux", {"foo": "bar", "baz": "qux"})


def test_mapping_args_with_bool_values() -> None:
    _assert_cmdline("--bar", {"foo": False, "bar": True})


def test_mix_and_match() -> None:
    _assert_cmdline(
        "saml2aws --verbose --idp-account sym exec aws ssm start-session --target i-0123456789abcdef",
        "saml2aws",
        {"verbose": True, "idp_account": "sym"},
        "exec",
        "aws",
        "ssm",
        "start-session",
        {"target": "i-0123456789abcdef"},
    )
