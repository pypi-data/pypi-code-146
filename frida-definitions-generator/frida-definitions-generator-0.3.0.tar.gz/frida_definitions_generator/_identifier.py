import re

METHODS_BLACKLIST = ("<init>", "<clinit>")
LEGAL_NAME_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z\d_$]*$")
ILLEGAL_NAME_CHARACTERS_REGEX = re.compile(r"[^a-zA-Z\d_$]")
JAVASCRIPT_KEYWORDS = (
    "break",
    "case",
    "catch",
    "class",
    "const",
    "continue",
    "debugger",
    "default",
    "delete",
    "do",
    "else",
    "export",
    "extends",
    "finally",
    "for",
    "function",
    "if",
    "import",
    "in",
    "instanceof",
    "new",
    "return",
    "super",
    "switch",
    "this",
    "throw",
    "try",
    "typeof",
    "var",
    "void",
    "while",
    "with",
    "yield",
)
TYPESCRIPT_KEYWORDS = (
    "null",
    "package",
    "type",
    "static",
    "default",
    "number",
    "import",
    "with",
    "implements",
    "delete",
    "debugger",
    "enum",
    "private",
    "class",
    "public",
    "get",
    "as",
    "true",
    "let",
    "false",
    "any",
    "string",
    "interface",
    "module",
)


def is_name_valid(name: str) -> bool:
    return (
        len(name) > 0
        and LEGAL_NAME_REGEX.match(name) is not None
        and name not in JAVASCRIPT_KEYWORDS
        and name not in TYPESCRIPT_KEYWORDS
    )


def get_legal_name(name: str) -> str:
    if is_name_valid(name):
        return name

    stripped_name = ILLEGAL_NAME_CHARACTERS_REGEX.sub("", name)
    if is_name_valid(stripped_name):
        return stripped_name

    return "_" + stripped_name


def get_legal_pretty_name(name: str) -> str:
    names = name.split(".")
    return ".".join(map(get_legal_name, names))
