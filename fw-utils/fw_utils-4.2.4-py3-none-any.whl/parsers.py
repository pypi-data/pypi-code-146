"""String parsers for various formats."""
import re
import typing as t
from datetime import datetime
from functools import partial
from urllib.parse import unquote_plus

from .datetime import get_datetime
from .dicts import AttrDict

__all__ = [
    "parse_hrtime",
    "parse_hrsize",
    "parse_url",
    "parse_field_name",
    "parse_pattern",
    "Pattern",
]


def parse_hrtime(value: str) -> float:
    """Return number of seconds for given human-readable time duration."""
    parts = value.split()
    units = {"y": 31536000, "w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
    seconds = 0.0
    regex = re.compile(r"(?P<num>\d+(\.\d*)?)(?P<unit>[ywdhms])", flags=re.I)
    for part in parts:
        match = regex.match(part)
        if match is None:
            raise ValueError(f"Cannot parse human-readable time: {part}")
        num, unit = float(match.group("num")), match.group("unit").lower()
        seconds += num * units[unit]
    return seconds


def parse_hrsize(value: str) -> int:
    """Return number of bytes for given human-readable file size."""
    pattern = r"(?P<num>\d+(\.\d*)?)\s*(?P<unit>([KMGTPEZY]i?)?B?)"
    match = re.match(pattern, value, flags=re.I)
    if not match:
        raise ValueError(f"Cannot parse human-readable size: {value!r}")
    num = float(match.groupdict()["num"])
    unit = match.groupdict()["unit"].upper().rstrip("BI") or "B"
    units = {u: 1024**i for i, u in enumerate("BKMGTPEZY")}
    return int(num * units[unit])


URL_RE = re.compile(
    r"^"
    r"(?P<scheme>[^+:@/?#]+)(\+(?P<driver>[^:@/?#]+))?://"
    r"((?P<username>[^:@]+)(:(?P<password>[^@]+))?@)?"
    r"(?P<host>[^:@/?#]*)"
    r"(:(?P<port>\d+))?"
    r"((?P<path>/[^?#]*))?"
    r"(\?(?P<query>[^#]+))?"
    r"(#(?P<fragment>.*))?"
    r"$"
)


def parse_url(url: str, split_params: bool = False) -> AttrDict:
    """Return dictionary of fields parsed from a URL."""
    match = URL_RE.match(url)
    if not match:
        raise ValueError(f"Invalid URL: {url}")
    parsed = {k: v for k, v in match.groupdict().items() if v is not None}
    # store query params directly on the result dict
    if params := parsed.pop("query", ""):
        for param in params.split("&"):
            if "=" not in param:  # handle params w/ missing =value
                param = f"{param}="
            field, value = param.split("=", maxsplit=1)
            value = unquote_plus(value)
            if split_params and "," in value:  # split values on commas
                value = value.split(",")
            if field not in parsed:  # 1st occurrence - store as-is
                parsed[field] = value
            else:  # Nth occurrence - store as list and append
                v1, v2 = parsed[field], value
                v1 = [v1] if isinstance(v1, str) else v1
                v2 = [v2] if isinstance(v2, str) else v2
                parsed[field] = v1 + v2
    return AttrDict(parsed)


def parse_field_name(
    field: str,
    *,
    aliases: t.Dict[str, str] = None,
    allowed: t.List[str] = None,
) -> str:
    """Return canonic field from a partial/abbreviated one using hints/aliases.

    Args:
        aliases Optional {pattern: replacement} mapping to enable shorthands.
        allowed: Optional list of allowed fields (eg. ["project.label"]).

    Returns:
        The validated, canonic (potentially expanded) field.
    """
    # pylint: disable=too-many-branches
    # replace aliases (while True allows prj -> project -> project.label)
    aliases = aliases or {}
    for _ in range(len(aliases)):
        field_ = replace(field, aliases)
        if field_ == field:
            break
        field = field_
    allowed = allowed or []
    # return field unchanged if no allow-list was passed
    if not allowed:
        return field  # pragma: no cover
    # return exact matches immediately
    if field in allowed and not field.endswith("*"):
        return field
    # start gathering a list of candidates based on the allow-list
    candidates = []
    parts = field.split(".")
    # 1st: dot-splitted parts are prefixes (subj.first -> subject.firstname)
    for candidate in allowed:
        cparts = candidate.split(".")
        if len(cparts) <= len(parts) and cparts[-1] == "*":
            cparts.pop()
        elif len(cparts) != len(parts):
            continue
        if all(cp.startswith(p) for cp, p in zip(cparts, parts)):
            candidates.append(candidate)
    if len(parts) == 1:
        # 2nd: unique prefix-of root (external -> external_routing_id)
        candidates = candidates or [c for c in allowed if c.startswith(field)]
        # 3rd: unique prefix of leaf (weight -> session.weight)
        candidates = candidates or [c for c in allowed if c.split(".")[-1] == field]
        # 4th: unique infix (routing -> external_routing_id)
        candidates = candidates or [c for c in allowed if field in c]
    # if the above rules yielded a single candidate, return
    if len(candidates) == 1:
        candidate = candidates[0]
        if candidate.endswith("*"):
            subkey = field.split(".", maxsplit=candidate.count("."))[-1]
            candidate = candidate.replace("*", subkey)
        return candidate
    # raise otherwise
    if candidates:
        raise ValueError(f"ambiguous field: {field!r} ({'|'.join(candidates)})")
    raise ValueError(f"invalid field: {field!r} (allowed: {'|'.join(allowed)})")


def parse_pattern(pattern: str, string: str) -> AttrDict:
    """Return values extracted from a string based on the given pattern."""
    return Pattern(pattern).match(string)  # pragma: no cover


class Pattern:
    """Pattern for parsing strings and extracting metadata from them.

    Patterns are intended to provide an intuitive, python f-string-like syntax
    for capturing parts of an input string - simpler compared to raw regexes.

    Simplified pattern syntax elements:
      `{field}` - Curly braces for capturing (dot-notated/nested) fields
      `[opt]`   - Brackets for making parts of the match optional
      `*`       - Star to match any string of characters (like glob)
      `.`       - Dot to match a literal dot (like glob)

    Captured group formats can be specified by suffixing the group name with a
    colon followed by the desired pattern: `{group:format}`
    The format can be a regex or an strptime pattern for timestamp fields.

    Except for the capture groups, the simplified syntax can be disabled to
    allow using raw regexes instead by suffixing the full pattern with `!r`.
    Similarly, case-insensitive matching can be enabled via `!i`.

    Examples:
      `[fw://]{group._id}[/{project.label}[/{subject.label}]]`
      `SCANPHYSLOG_{acquisition.timestamp:%Y%m%d%H%M%S}.log`
    """

    def __init__(
        self,
        pattern: str,
        validate: t.Callable[[str], str] = None,
        loaders: t.Dict[str, t.Callable] = None,
    ) -> None:
        """Parse and validate pattern."""
        self.pattern = pattern
        self.validate = validate
        self.loaders = loaders or {}
        self.fields: t.Set[str] = set()
        try:
            self.regex = self._parse()
        except AssertionError as exc:
            raise ValueError(exc.args[0]) from None

    def __str__(self) -> str:
        """Return the parsed regex pattern."""
        return self.canonic

    def __repr__(self) -> str:
        """Return the string representation of the pattern object."""
        return f"{self.__class__.__name__}('{self}')"

    def match(self, string: str) -> AttrDict:
        """Return metadata dictionary extracted from the string."""
        match = self.regex.match(string)
        if not match:
            return AttrDict()
        data = {}
        for field, value in match.groupdict().items():
            if not value:
                continue
            field = id_to_str(field)
            parser = self.loaders.get(field)
            if parser:
                value = parser(value)
            data[field] = value
        return AttrDict.from_flat(data)

    def _parse(self) -> t.Pattern:  # pylint: disable=too-many-branches
        """Parse and return the compiled regex for the pattern."""
        pattern, pos, curly = self.pattern, 0, False
        self.canonic, self.fields, regex, opts, flags, raw = "", set(), "", "", 0, False
        assert pattern, "empty pattern"
        assert "{}" not in pattern, "empty capture group"
        # parse and strip pattern!options (r=raw-regex, i=case-insensitive)
        match = re.match(r".*?(?<!\\)!(?P<opts>[a-z]+)$", pattern)
        if match:
            opts = match.group("opts")
            assert all(opt in "ri" for opt in opts), f"invalid opts: {opts}"
            pattern = pattern[: -len(f"!{opts}")]
            if "r" in opts:
                raw = True
            if "i" in opts:
                flags = re.IGNORECASE
        # assume {pattern} is a capture group if no curlies present
        if not re.search(r"(?<!\\)([{}])", pattern):
            pattern = f"{{{pattern}}}"  # implicit capture group
        # transpile the pattern into a regex
        parts = [part for part in re.split(r"(?<!\\)([{}])", pattern) if part]
        for part in parts:
            canon_part = part
            # capture group start
            if part == "{":
                assert not curly, f"unexpected {{ at char {pos} in {pattern!r}"
                curly = True
            # capture group end
            elif part == "}":
                assert curly, f"unexpected }} at char {pos} in {pattern!r}"
                curly = False
            # repetition pattern (faux group)
            elif curly and re.match(r"\d+(,\d+)?", part):
                regex += f"{{{part}}}"
            # capture group body
            elif curly:
                # parse group
                match = re.match(r"(?P<field>[^:]+)(:(?P<fmt>.+))?", part)
                assert match, f"invalid capture group {part!r}"
                field, fmt = match.group("field"), match.group("fmt")
                # validate field
                field = self.validate(field) if self.validate else field
                # collect field names
                self.fields.add(field)
                canon_part = f"{field}{':' + fmt if fmt else ''}"
                # strptime format support for timestamps
                dt_re = r"date|time(stamp)?"
                if re.search(rf"^{dt_re}|{dt_re}$", field):
                    self.loaders.setdefault(field, self.load_timestamp)
                if self.loaders.get(field) is self.load_timestamp and fmt:
                    self.loaders[field] = partial(self.load_timestamp, fmt=fmt)
                    fmt = strptime_to_regex(fmt)
                fmt = fmt or (r".+" if raw else r"\.+")
                fmt = fmt if raw else simple_regex(fmt)
                regex += rf"(?P<{str_to_id(field)}>{fmt})"
            # non-captured parts
            elif part:
                regex += part if raw else simple_regex(part)
            self.canonic += canon_part
            pos += len(part)
        assert not curly, f"unterminated {{ in {pattern!r}"
        if opts:
            self.canonic += f"!{opts}"
        return re.compile(rf"^{lazy_regex(regex)}$", flags=flags)

    @staticmethod
    def load_timestamp(
        value: str,
        fmt: t.Optional[str] = None,
    ) -> t.Optional[datetime]:
        """Return parsed datetime object (or None)."""
        try:
            return get_datetime(value, fmt=fmt)
        except ValueError:  # pragma: no cover
            return None


def str_to_id(raw_string: str) -> str:
    """Convert any string to a valid python identifier in a reversible way."""

    def char_to_hex(match: t.Match) -> str:
        return f"__{ord(match.group(0)):02x}__"

    raw_string = re.sub(r"^[^a-z_]", char_to_hex, raw_string, flags=re.I)
    return re.sub(r"[^a-z_0-9]{1}", char_to_hex, raw_string, flags=re.I)


def id_to_str(python_id: str) -> str:
    """Convert a python identifier back to the original/normal string."""

    def hex_to_char(match: t.Match) -> str:
        return chr(int(match.group(1), 16))

    return re.sub(r"__([a-f0-9]{2})__", hex_to_char, python_id)


def replace(string: str, table: t.Dict[str, str]) -> str:
    """Simultaneously replace multiple patterns using re.sub in a string."""

    def repl(match: re.Match):
        return next(v for k, v in table.items() if re.match(k, match.group()))

    return re.sub("|".join(table), repl, string)


def simple_regex(pattern: str) -> str:
    """Translate simplified glob-like notation to full regex."""
    return replace(pattern, SIMPLE_RE_MAP)


def lazy_regex(pattern: str) -> str:
    """Translate eager repeat patterns to lazy ones."""
    return replace(pattern, LAZY_RE_MAP)


def strptime_to_regex(strptime: str) -> str:
    """Convert strptime pattern to a matching regex string."""
    regex, lastpos = "", 0
    for match in re.finditer(r"%.", strptime):
        # track non-capture prefix and postfix around match group
        start, end = match.span()
        pre, post = match.string[lastpos:start], match.string[end:]
        lastpos = end
        # translate strptime format code to regex
        code = match.group()
        code_re = STRPTIME_CODE_RE.get(code)
        if not code_re:
            raise ValueError(f"invalid strptime code {code!r} in {strptime!r}")
        regex = f"{regex}{pre}{code_re}"
    return f"{regex}{post}"


SIMPLE_RE_MAP = {
    # simplified [optional] notation
    r"(?<!\\)\[": r"(",
    r"(?<!\\)\]": r")?",
    # glob-like "^" - escaped to match literal caret
    r"(?<!\\)\^": r"\^",
    # glob-like "." - escaped to match literal dot
    r"(?<!\\)\.": r"\.",
    # glob-like "*" - turned into .* to match
    r"(?<!\\)\*": r".*",
    # allow escaping all of the above
    r"\\\[": "[",
    r"\\\]": "]",
    r"\\\^": "^",
    r"\\\.": ".",
    r"\\\*": "*",
}

LAZY_RE_MAP = {
    # lazify stars and pluses to allow less verbose patterns
    r"(?<!\\)\*(?![?{])": r"*?",
    r"(?<!\\)\+(?![?{])": r"+?",
}

# map of strptime codes to regex strings
STRPTIME_CODE_RE: t.Dict[str, str] = {
    "%a": r"[A-Za-z]+?",
    "%A": r"[A-Za-z]+?",
    "%w": r"\d",
    "%d": r"\d\d",
    "%b": r"[A-Za-z]+?",
    "%B": r"[A-Za-z]+?",
    "%m": r"\d\d",
    "%y": r"\d\d",
    "%Y": r"\d\d\d\d",
    "%H": r"\d\d",
    "%I": r"\d\d",
    "%p": r"[A-Za-z]+?",
    "%M": r"\d\d",
    "%S": r"\d\d",
    "%f": r"\d+?",
    "%z": r"[+-]\d\d\d\d(\d\d(\.\d+?)?)?",
    "%Z": r"[A-Z]*?",
    "%j": r"\d\d\d",
    "%U": r"\d\d",
    "%W": r"\d\d",
    "%c": r".*?",
    "%x": r".*?",
    "%X": r".*?",
    "%%": r"%",
    "%G": r"\d\d\d\d",
    "%u": r"\d",
    "%V": r"\d\d",
}
