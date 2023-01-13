"""String formatting helpers for various inputs."""
import re
import time
import typing as t
from functools import partial
from urllib.parse import quote_plus

from .dicts import get_field

__all__ = [
    "pluralize",
    "quantify",
    "hrsize",
    "hrtime",
    "format_url",
    "format_query_string",
    "Template",
    "Timer",
]

PLURALS = {
    "study": "studies",
    "series": "series",
    "analysis": "analyses",
}


def pluralize(singular: str, plural: str = "") -> str:
    """Return plural for given singular noun."""
    if plural:
        PLURALS[singular.lower()] = plural.lower()
    return PLURALS.get(singular, f"{singular}s")


def quantify(num: int, singular: str, plural: str = "") -> str:
    """Return "counted str" for given num and word: (3,'file') => '3 files'."""
    if num == 1:
        return f"1 {singular}"
    plural = pluralize(singular, plural)
    return f"{num} {plural}"


def hrsize(size: float) -> str:
    """Return human-readable file size for given number of bytes."""
    unit, decimals = "B", 0
    for unit in "BKMGTPEZY":
        decimals = 0 if unit == "B" or round(size) > 9 else 1
        if round(size) < 1000 or unit == "Y":
            break
        size /= 1024.0
    return f"{size:.{decimals}f}{unit}".replace(".0", "")


def hrtime(seconds: float) -> str:
    """Return human-readable time duration for given number of seconds."""
    remainder = seconds
    parts: t.List[str] = []
    units = {"y": 31536000, "w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
    for unit, seconds_in_unit in units.items():
        quotient, remainder = divmod(remainder, seconds_in_unit)
        if len(parts) > 1 or (parts and not quotient):
            break
        if unit == "s" and not parts:
            decimals = 0 if round(quotient) >= 10 or not round(remainder, 1) else 1
            parts.append(f"{quotient + remainder:.{decimals}f}{unit}")
        elif quotient >= 1:
            parts.append(f"{int(quotient)}{unit}")
    return " ".join(parts)


def format_url(  # pylint: disable=too-many-arguments
    *,
    scheme: str = "https",
    driver: str = None,
    username: str = None,
    password: str = None,
    host: str = "",
    port: int = None,
    path: str = None,
    fragment: str = None,
    **query: str,
) -> str:
    """Return URL string built from the arguments."""
    url = scheme
    if driver:
        url += f"+{driver}"
    url += "://"
    if username:
        auth = username if not password else f"{username}:{password}"
        url += f"{auth}@"
    url += host
    if port:
        url += f":{port}"
    if path:
        url += f"/{path.lstrip('/')}"
    if query:
        url += format_query_string(**query)
    if fragment:
        url += f"#{fragment}"
    return url


def format_query_string(**params) -> str:
    """Return URL query string with params from kwargs."""
    query_string = ""
    for key, value in params.items():
        if not isinstance(value, list):
            value = [value]
        for item in value:
            if item is None:
                continue  # pragma: no cover
            if item in (True, False):
                item = str(item).lower()  # pragma: no cover
            query_string += "?" if not query_string else "&"
            query_string += key if not item else f"{key}={quote_plus(item)}"
    return query_string


def format_template(template: str, data: dict) -> str:
    """Return data formatted as a string based on the given template."""
    return Template(template).format(data)  # pragma: no cover


class Template:
    """Template for formatting metadata as a single string like a path.

    Templates are intended to provide an intuitive, python f-string-like syntax
    to format strings from nested or dot-notated flywheel metadata dicts.

    Formatting syntax elements:
      `{field}`         - Curly braces for dumping (dot-notated/nested) fields
      `{field/pat/sub}` - re.sub pattern and replacement string
      `{field:format}`  - f-string format specifier (strftime pattern for timestamps)
      `{field|default}` - Default to use if the value is None/"" instead of "UNKNOWN"

    Combining the modifier syntaxes when dumping a field is allowed in the order:
      /pat/sub >> :format >> |default

    Examples:
      `{project.label:.5}/{subject.firstname|John}/{file.name/.dicom.zip/}`
    """

    def __init__(
        self,
        template: str,
        validate: t.Callable[[str], str] = None,
    ) -> None:
        """Parse and validate the template."""
        self.template = template
        self.validate = validate
        self.fields: t.List[str] = []
        self.specs: t.List[str] = []
        self.dumpers: t.List[t.Callable] = []
        try:
            self.fstring = self._parse()
        except AssertionError as exc:
            raise ValueError(exc.args[0]) from None

    def __str__(self) -> str:
        """Return the parsed/canonized f-string like template string."""
        args = [f"{{{f}{s}}}" for f, s in zip(self.fields, self.specs)]
        return self.fstring.format(*args)

    def __repr__(self) -> str:
        """Return the string representation of the template object."""
        return f"{self.__class__.__name__}('{self}')"

    def format(self, data: dict) -> str:
        """Return the template formatted with the given value mapping."""
        raw_values = [get_field(data, field) for field in self.fields]
        fmt_values = [dump(raw) for dump, raw in zip(self.dumpers, raw_values)]
        return self.fstring.format(*fmt_values)

    def _parse(self) -> str:
        """Parse and return the f-string for the template."""
        template, pos, curly = self.template, 0, False
        fstring = ""
        regex = re.compile(
            r"(?P<field>[^/:|]+)"
            r"(?P<spec>"
            r"(/(?P<pat>[^/]+)(/(?P<sub>[^:|]*))?)?"
            r"(:(?P<fmt>[^|]+))?"
            r"(\|(?P<default>.+))?"
            r")"
        )
        assert template, "empty template"
        assert "{}" not in template, "empty format block"
        # assume {template} is a format block if no curlies present
        if not re.search(r"(?<!\\)([{}])", template):
            template = f"{{{template}}}"  # implicit format block
        parts = [part for part in re.split(r"(?<!\\)([{}])", template) if part]
        for part in parts:
            # format block start
            if part == "{":
                assert not curly, f"unexpected {{ at char {pos} in {template!r}"
                curly = True
            # format block end
            elif part == "}":
                assert curly, f"unexpected }} at char {pos} in {template!r}"
                curly = False
            # format block body
            elif curly:
                # parse format
                match = regex.match(part)
                assert match, f"invalid format block {part!r}"
                kwargs = match.groupdict()
                field = kwargs.pop("field")
                # validate field
                field = self.validate(field) if self.validate else field
                # validate substitution pattern
                re.compile(kwargs["pat"] or "")
                # store field, spec and dumper func for later
                self.fields.append(field)
                self.specs.append(kwargs.pop("spec") or "")
                self.dumpers.append(partial(self._dump_value, **kwargs))
                fstring += "{}"
            # literal part
            else:
                fstring += part
            pos += len(part)
        assert not curly, f"unterminated {{ in {template!r}"
        # translate backslash-escaped curlies to f-string-style double notation
        fstring = re.sub(r"\\(\{|\})", r"\\\1\1", fstring)
        return fstring

    @staticmethod
    def _dump_value(
        value,
        pat: str = "",
        sub: str = "",
        fmt: str = "",
        default: str = "",
    ) -> str:
        """Return value formatted as a string."""
        if value in (None, ""):
            return default or "UNKNOWN"
        if pat:
            value = re.sub(pat, sub, str(value))
        if fmt:
            value = f"{{:{fmt}}}".format(value)
        return value


def report_progress(
    iterable: t.Iterable,
    callback: t.Callable[[str], t.Any] = print,
    template: str = "{count}/{total} ({percent:.1%}) [{elapsed}, {speed:.1f}/s]",
    seconds: int = 1,
    total: int = 0,
) -> t.Iterable:
    """Report progress via a callback/message when processing an iterable."""
    start = now = last_report = time.perf_counter()
    count = 0
    if not total and hasattr(iterable, "__len__"):
        total = len(t.cast(t.Sized, iterable))
    if not total and "total" in template:
        template = "{count} [{elapsed}, {speed:.1f}/s]"

    def report():
        elapsed = now - start
        progress = dict(
            count=count,
            total=total,
            percent=count / total if total else 0,
            elapsed=hrtime(elapsed),
            speed=count / elapsed if elapsed else 0,
        )
        callback(template.format_map(progress))

    for count, item in enumerate(iterable):
        now = time.perf_counter()
        if now - last_report >= seconds:
            last_report = now
            report()
        yield item

    if count:
        count += 1
        now = time.perf_counter()
        report()


class Timer:  # pylint: disable=too-few-public-methods
    """Timer for logging size/speed reports on file processing/transfers."""

    # pylint: disable=redefined-builtin
    def __init__(self, files: int = 0, bytes: int = 0) -> None:
        """Init timer w/ current timestamp and the no. of files/bytes."""
        self.start = time.perf_counter()
        self.files = files
        self.bytes = bytes

    def report(self) -> str:
        """Return message with size and speed info based on the elapsed time."""
        elapsed = time.perf_counter() - self.start
        size, speed = [], []
        if self.files or not self.bytes:
            size.append(quantify(self.files, "file"))
            speed.append(f"{self.files / elapsed:.1f}/s")
        if self.bytes:
            size.append(hrsize(self.bytes))
            speed.append(hrsize(self.bytes / elapsed) + "/s")
        return f"{'|'.join(size)} in {hrtime(elapsed)} [{'|'.join(speed)}]"
