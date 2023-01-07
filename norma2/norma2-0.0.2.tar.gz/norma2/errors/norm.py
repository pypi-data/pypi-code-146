from enum import Enum
from typing import List, Type


class Severity(Enum):
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


class _TemplateNormError:
    severity = Severity.INFO
    explanation = ""
    rule = ""

    def __init__(
        self,
        filepath: str,
        line: int,
        severity: Severity,
        rule: str,
        explanation: str,
        msg: str = "",
    ):
        self.filepath = filepath
        self.line = line
        self.msg = msg
        self.rule = rule
        self.explanation = explanation
        self.severity = severity

    def __str__(self) -> str:
        return self.show(with_explanation=True, print_stdout=False)

    def show(self, with_explanation: bool = False, print_stdout: bool = True) -> str:
        ret = f"{self.filepath}:{self.line} :: {self.rule}::"
        ret += f"{self.severity.value}"
        if self.msg:
            ret += f" :: {self.msg}"
        if with_explanation:
            ret += f"\nexplanation: {self.explanation}"
        if print_stdout:
            print(ret)
        return ret

    @classmethod
    def only_explanation(cls, print_stdout: bool = True) -> str:
        ret = f"-> {cls.rule} :: {cls.severity.value}\n{cls.explanation}"
        if print_stdout:
            print(ret)
        return ret


class BadFileExtension(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "The repository must not contain compiled temporary or unnecessary files"  # noqa: E501
    rule = "C-O1"

    def __init__(self, filepath: str, msg: str = ""):
        super().__init__(
            filepath=filepath,
            line=0,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class TooManyFunctions(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "Beyond 5 functions in your file, you must subdivide your logical entity into several sub-entities"  # noqa: E501
    rule = "C-O3"

    def __init__(self, filepath: str, msg: str):
        super().__init__(
            filepath=filepath,
            line=0,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class BadFileName(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "All file names and folders must be in English, according to the snake_case convention (that is, only composed of lowercase, numbers, and underscores)"  # noqa: E501
    rule = "C-O4"

    def __init__(self, filepath: str, msg: str):
        super().__init__(
            filepath=filepath,
            line=0,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class FileHeader(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "C files (.c, .h, . . . ) and every Makefiles must always start with the standard header of the school"  # noqa: E501
    rule = "C-G1"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class SepBetweenFunction(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "Inside a source file, implementations of functions must be separated by one and only one empty line"  # noqa: E501
    rule = "C-G2"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class PreprocessorIndent(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "The preprocessor directives must be indented according to the level of indirection"  # noqa: E501
    rule = "C-G3"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class GlobalVariable(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "Global variables must be avoided as much as possible. Only global constants should be used"  # noqa: E501
    rule = "C-G4"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class IncludeFile(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "include directive must only include C header (.h) files"
    rule = "C-G5"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class LineEnding(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "Line endings must be done in UNIX style (with \\n)"
    rule = "C-G6"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class TrailingSpace(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "No trailing spaces must be present at the end of a line"
    rule = "C-G7"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class LeadingTrailingLine(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "No leading empty lines must be present. No more than 1 trailing empty line must be present"  # noqa: E501
    rule = "C-G7"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class NamingFunction(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "All function names must be in English, according to the snake_case convention (meaning that it is composed only of lowercase, numbers, and underscores)"  # noqa: E501
    rule = "C-F2"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class ColumnsNumber(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "The length of a line must not exceed 80 columns (not to be confused with 80 characters)"  # noqa: E501
    rule = "C-F3"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class FunctionLineNumber(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "The body of a function should be as short as possible, and must not exceed 20 lines"  # noqa: E501
    rule = "C-F4"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class FunctionParametersNumber(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "A function must not have more than 4 parameters"
    rule = "C-F5"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class FunctionWithoutParameter(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "A function taking no parameters must take void as a parameter in the function declaration"  # noqa: E501
    rule = "C-F6"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class StructureParameter(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "Structures must be transmitted as arguments using a pointer, not by copy"  # noqa: E501
    rule = "C-F7"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class CommentInFunction(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "There must be no comment within a function"
    rule = "C-F8"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class NestedFunction(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "Nested functions are not allowed"
    rule = "C-F9"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class ManyStatementOnLine(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "A line must correspond to only one statement"
    rule = "C-L1"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class BadIndentation(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "Each indentation level must be done by using 4 spaces. No tabulations may be used for indentation"  # noqa: E501
    rule = "C-L2"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class BadSpace(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "When using a space as a separator, one and only one space character must be used. Always place a space after a comma or a keyword (if it has arguments). there must be no spaces between the name of a function and the opening parenthesis, after a unary operator, or before a semicolon. In the precise case of a for control structure, if a semicolon inside the parentheses is not immediately followed by another semicolon, it must be followed by a space. All binary and ternary operators must be separated from their arguments by a space on both sides"  # noqa: E501
    rule = "C-L3"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class BadCurlyBracket(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "Opening curly brackets must be at the end of the line, after the content it precedes, except for functions definitions where they must be placed alone on their line. Closing curly brackets must be alone on their line, except in the case of else/else if control structures, enum declarations, or structure declarations (with or without an associated typedef)"  # noqa: E501
    rule = "C-L4"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class MissPlacedVariableDeclaration(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "Variables must be declared at the beginning of the scope of the function, Only one variable must be declared per line. The for control structures may also optionally declare variables in their initialization part"  # noqa: E501
    rule = "C-L5"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class BadLineJumps(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "A line break must separate the variable declarations from the remainder of the function. No other line breaks must be present in the scope of a function"  # noqa: E501
    rule = "C-L6"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class BadNamingIdentifiers(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "All identifier names must be in English, according to the snake_case convention (meaning it is composed exclusively of lowercase, numbers, and underscores). The type names defined with typedef must end with _t. The names of macros and global constants and the content of enums must be written in UPPER_SNAKE_CASE"  # noqa: E501
    rule = "C-V1"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class MissPlacedPointer(_TemplateNormError):
    severity = Severity.MINOR
    explanation = "The pointer symbol (*) must be attached to the associated variable, with no spaces"  # noqa: E501
    rule = "C-V3"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class TooManyConditionBranch(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "A conditionnal block (while, for, if, else, . . . ) must not contain more than 3 branches"  # noqa: E501
    rule = "C-C1"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class NoGoto(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "Using the goto keyword is forbidden"
    rule = "C-C3"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class FunctionInHeader(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "non static inline function are banned from header file"
    rule = "C-H1"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class NoIncludeGuard(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = "Headers must be protected from double inclusion"
    rule = "C-H2"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class MacroOnMultiLine(_TemplateNormError):
    severity = Severity.MAJOR
    explanation = (
        "Macros must match only one statement, and fit on a single line"  # noqa: E501
    )
    rule = "C-H3"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class BadEndLineBreak(_TemplateNormError):
    severity = Severity.INFO
    explanation = "Files must end with a line break"
    rule = "C-A3"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            severity=self.severity,
            rule=self.rule,
            explanation=self.explanation,
            msg=msg,
        )


class Info(_TemplateNormError):
    severity = Severity.INFO
    explanation = "tip of the norma2 dev"
    rule = "info"

    def __init__(self, filepath: str, line: int, msg: str):
        super().__init__(
            filepath=filepath,
            line=line,
            rule=self.rule,
            severity=self.severity,
            explanation=self.explanation,
            msg=msg,
        )


ALL_ERROR_NORM: List[Type[_TemplateNormError]] = [
    BadFileExtension,
    TooManyFunctions,
    BadFileName,
    FileHeader,
    SepBetweenFunction,
    PreprocessorIndent,
    GlobalVariable,
    IncludeFile,
    LineEnding,
    TrailingSpace,
    LeadingTrailingLine,
    NamingFunction,
    ColumnsNumber,
    FunctionLineNumber,
    FunctionParametersNumber,
    FunctionWithoutParameter,
    StructureParameter,
    CommentInFunction,
    NestedFunction,
    ManyStatementOnLine,
    BadIndentation,
    BadSpace,
    BadCurlyBracket,
    MissPlacedVariableDeclaration,
    BadLineJumps,
    BadNamingIdentifiers,
    MissPlacedPointer,
    TooManyConditionBranch,
    NoGoto,
    FunctionInHeader,
    NoIncludeGuard,
    MacroOnMultiLine,
    BadEndLineBreak,
    Info,
]
