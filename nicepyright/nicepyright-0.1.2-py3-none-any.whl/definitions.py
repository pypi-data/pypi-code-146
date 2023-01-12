from __future__ import annotations

from enum import Enum
from typing import NamedTuple


class DiagnosticRule(str, Enum):
    """The diagnostic rule that caused the error.

    See Also:
        https://github.com/microsoft/pyright/
        File: packages/pyright-internal/src/common/diagnosticRules.ts
    """

    StrictListInference = "strictListInference"
    StrictSetInference = "strictSetInference"
    StrictDictionaryInference = "strictDictionaryInference"
    AnalyzeUnannotatedFunctions = "analyzeUnannotatedFunctions"
    StrictParameterNoneValue = "strictParameterNoneValue"
    EnableTypeIgnoreComments = "enableTypeIgnoreComments"

    GeneralTypeIssues = "reportGeneralTypeIssues"
    PropertyTypeMismatch = "reportPropertyTypeMismatch"
    FunctionMemberAccess = "reportFunctionMemberAccess"
    MissingImports = "reportMissingImports"
    MissingModuleSource = "reportMissingModuleSource"
    MissingTypeStubs = "reportMissingTypeStubs"
    ImportCycles = "reportImportCycles"
    UnusedImport = "reportUnusedImport"
    UnusedClass = "reportUnusedClass"
    UnusedFunction = "reportUnusedFunction"
    UnusedVariable = "reportUnusedVariable"
    DuplicateImport = "reportDuplicateImport"
    WildcardImportFromLibrary = "reportWildcardImportFromLibrary"
    OptionalSubscript = "reportOptionalSubscript"
    OptionalMemberAccess = "reportOptionalMemberAccess"
    OptionalCall = "reportOptionalCall"
    OptionalIterable = "reportOptionalIterable"
    OptionalContextManager = "reportOptionalContextManager"
    OptionalOperand = "reportOptionalOperand"
    TypedDictNotRequiredAccess = "reportTypedDictNotRequiredAccess"
    UntypedFunctionDecorator = "reportUntypedFunctionDecorator"
    UntypedClassDecorator = "reportUntypedClassDecorator"
    UntypedBaseClass = "reportUntypedBaseClass"
    UntypedNamedTuple = "reportUntypedNamedTuple"
    PrivateUsage = "reportPrivateUsage"
    TypeCommentUsage = "reportTypeCommentUsage"
    PrivateImportUsage = "reportPrivateImportUsage"
    ConstantRedefinition = "reportConstantRedefinition"
    IncompatibleMethodOverride = "reportIncompatibleMethodOverride"
    IncompatibleVariableOverride = "reportIncompatibleVariableOverride"
    InconsistentConstructor = "reportInconsistentConstructor"
    OverlappingOverload = "reportOverlappingOverload"
    MissingSuperCall = "reportMissingSuperCall"
    UninitializedInstanceVariable = "reportUninitializedInstanceVariable"
    InvalidStringEscapeSequence = "reportInvalidStringEscapeSequence"
    UnknownParameterType = "reportUnknownParameterType"
    UnknownArgumentType = "reportUnknownArgumentType"
    UnknownLambdaType = "reportUnknownLambdaType"
    UnknownVariableType = "reportUnknownVariableType"
    UnknownMemberType = "reportUnknownMemberType"
    MissingParameterType = "reportMissingParameterType"
    MissingTypeArgument = "reportMissingTypeArgument"
    InvalidTypeVarUse = "reportInvalidTypeVarUse"
    CallInDefaultInitializer = "reportCallInDefaultInitializer"
    UnnecessaryIsInstance = "reportUnnecessaryIsInstance"
    UnnecessaryCast = "reportUnnecessaryCast"
    UnnecessaryComparison = "reportUnnecessaryComparison"
    UnnecessaryContains = "reportUnnecessaryContains"
    AssertAlwaysTrue = "reportAssertAlwaysTrue"
    SelfClsParameterName = "reportSelfClsParameterName"
    ImplicitStringConcatenation = "reportImplicitStringConcatenation"
    UndefinedVariable = "reportUndefinedVariable"
    UnboundVariable = "reportUnboundVariable"
    InvalidStubStatement = "reportInvalidStubStatement"
    IncompleteStub = "reportIncompleteStub"
    UnsupportedDunderAll = "reportUnsupportedDunderAll"
    UnusedCallResult = "reportUnusedCallResult"
    UnusedCoroutine = "reportUnusedCoroutine"
    UnusedExpression = "reportUnusedExpression"
    UnnecessaryTypeIgnoreComment = "reportUnnecessaryTypeIgnoreComment"
    MatchNotExhaustive = "reportMatchNotExhaustive"
    ShadowedImports = "reportShadowedImports"


class Range(NamedTuple):
    line: int
    character: int


class SeverityLevel(str, Enum):
    Error = "error"
    Warning = "warning"
    Information = "information"

    def __rich_console__(self, console, options):
        if self == SeverityLevel.Error:
            yield f"[bold red]{self.value.capitalize()}[/bold red]"
        elif self == SeverityLevel.Warning:
            yield f"[bold yellow]{self.value.capitalize()}[/bold yellow]"
        elif self == SeverityLevel.Information:
            yield f"[bold blue]{self.value.capitalize()}[/bold blue]"
        else:
            raise ValueError(f"Unknown severity level: {self}")


__all__ = ("DiagnosticRule", "Range", "SeverityLevel")
