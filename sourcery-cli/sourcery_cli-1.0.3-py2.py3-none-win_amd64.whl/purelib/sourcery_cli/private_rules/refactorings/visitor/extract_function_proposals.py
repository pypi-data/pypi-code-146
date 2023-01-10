import typing
from typing import Any, List, Optional, Set, Type

from sourcery.analysis.clone_detection import Clones
from sourcery.analysis.control_flow_next_node import ControlFlowNextNode
from sourcery.analysis.near_clone_detection import NearClones, PartialBlockNearClones
from sourcery.analysis.node_dependencies import NodeDependencies
from sourcery.analysis.node_paths import PathNodes
from sourcery.analysis.node_statements import NodeStatements
from sourcery.analysis.node_var_ranges import StatementMemoryVars
from sourcery.analysis.nodes_in_loops import NodesInLoops
from sourcery.analysis.variable_usage import VariableUsage, VariableUsageAnalyzer
from sourcery.ast import (
    AST,
    Assign,
    Attribute,
    Block,
    Call,
    ClassDef,
    Expr,
    Expression,
    Flag,
    FormattedValue,
    FunctionDef,
    JoinedStr,
    Name,
    Node,
    Param,
    Parameters,
    Return,
    Statement,
    is_contained_in,
)
from sourcery.clones.extract_checker import ExtractChecker, ends_with_return
from sourcery.clones.extract_method import (
    CallToMethod,
    ExtractedMethod,
    MethodExtraction,
    MethodExtractor,
    is_class_function,
)
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.rules.private.refactorings.descriptions import (
    EXTRACT_DUP_FUNCTION_DESC,
    EXTRACT_DUP_METHOD_DESC,
    EXTRACT_FUNC_DESC,
    EXTRACT_METHOD_DESC,
)
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionTypeChanged,
    FunctionCallsOnException,
    LocalChangeOnException,
    LocalValueMissing,
    ReturnValuesChanged,
    ReturnValuesChangedOnException,
    SemanticDifference,
)

MINIMUM_SIZE = 3
MINIMUM_SINGLE_SIZE = 5


class ExtractFunctionProposer(MultiProposer):
    """Extract functions.

     Description of algorithm:
     We need to walk each block, returning a list of names, consts.
     [Name(a), Constant("test"), Name(a), Name(q)]
     [Name(b), Constant("test"), Name(b), Name(q)]
     [Name(c), Constant("test"), Name(c)], Name(q)]

    Then move through the zipped set of lists
    Need to build up the argument list.
      have a dictionary with hash(a,b,c): arg0, etc.
    If they're all the same and its a constant - do nothing
    If they're all the same and its a name
      add that name to the method args, call args, dont change body
    If there's a difference
      add a new argument to the method args, add the arg name to the call args
      replace the instance in the new body with the arg name
    also want a  list of replacements in the method body
    [(Name(a), arg0), (Name(a), arg0) ]
    """

    clones: Clones
    near_clones: NearClones
    partial_clones: PartialBlockNearClones

    # These are clones that can be extracted together
    suitable_clones: typing.Tuple[
        typing.Tuple[Block, ...], ...
    ]  # these would also be virtual blocks.

    # These are non-duplicate large blocks that can be extracted
    suitable_single_blocks: List[
        Block
    ]  # make these into VirtualBlocks, get rid of the getstatement

    node_statements: NodeStatements
    variable_usages: VariableUsage
    next_nodes: ControlFlowNextNode
    nodes_in_loops: NodesInLoops
    node_paths: PathNodes

    statement_vars: StatementMemoryVars

    node_dependencies: NodeDependencies

    current_function_size: int
    extract_checker: ExtractChecker

    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {ExtractMethodProposal, ExtractDuplicateMethodProposal}

    def tags(self) -> set[str]:
        return super().tags() | {"default", "pro"}

    def reset(self, ast: AST):
        super().reset(ast)
        # Calculate var usages for the partial clones
        for clones in self.partial_clones:
            for clone in clones:
                usages = clone.run(VariableUsageAnalyzer())
                var_usages = usages[clone[0].parent]
                self.variable_usages[clone] = var_usages
        self.extract_checker = ExtractChecker(
            self.node_dependencies,
            self.variable_usages,
            self.nodes_in_loops,
            self.statement_vars,
            self.next_nodes,
        )

        self.suitable_clones = self.extract_checker.suitable_clones(self.partial_clones)
        self.suitable_single_blocks = []
        self.current_function_size = 0

    def enter_functiondef(self, node: FunctionDef):
        self.suitable_single_blocks = []
        self.current_function_size = self.node_statements[node]

    def leave_functiondef(self, node: FunctionDef):
        if not suitable_function(node):
            return

        clones = self.clones_in_function(node)
        if not clones:
            return

        extractor = MethodExtractor(self.extract_checker)
        if extracted_method := extractor.extract_method(node, clones):
            proposal_class = (
                ExtractMethodProposal
                if len(clones) == 1
                else ExtractDuplicateMethodProposal
            )
            self.propose(proposal_class(self.ast, node, extracted_method))

    def clones_in_function(self, node: FunctionDef) -> Optional[typing.Tuple[Any, ...]]:
        if function_clones := [
            clones
            for clones in self.suitable_clones
            if is_contained_in(clones[0][0], node)
        ]:
            return max(function_clones, key=lambda x: sum(len(y) for y in x))
        elif self.suitable_single_blocks:
            return (self.suitable_single_blocks[0],)
        else:
            return None

    def leave_block(self, node: Block):
        remaining_function_size = (
            self.current_function_size + 1 - self.node_statements[node]
        )
        if (
            not isinstance(node.parent, (ClassDef, FunctionDef))
            and len(node.statements) > MINIMUM_SINGLE_SIZE
            and remaining_function_size > MINIMUM_SINGLE_SIZE
            and not self.extract_checker.dependency_issue((node,))
        ):
            self.suitable_single_blocks.append(node)


def suitable_function(node: Node) -> bool:
    if not isinstance(node, FunctionDef):
        return False

    if (
        node.decorator_list
        or node.is_async
        or (node.name.id.startswith("__") and node.name.id.endswith("__"))
    ):
        return False
    # It's highly suspicious if 'self' is annotated.
    elif is_class_function(node) and node.params.params[0].annotation:
        return False
    else:
        return True


class BaseExtractMethodProposal(Proposal):
    def __init__(
        self, ast: AST, node: FunctionDef, extracted_method: MethodExtraction
    ) -> None:
        self.ast = ast
        self.node = node
        self.new_method = extracted_method.new_method
        self.node_index = self.node.parent.index(self.node)
        self.calls = extracted_method.calls

    def description(self):
        raise NotImplementedError

    def target_nodes(self) -> tuple[Node, ...]:
        return tuple(node for call in self.calls for node in call.code_to_replace)

    def execute(self) -> None:
        # Replace the names in the method body with the arguments
        for node, replacement in self.new_method.body_argument_replacements:
            replacement_name = Name(replacement)
            if isinstance(node.parent, JoinedStr):
                node.replace(
                    FormattedValue(replacement_name, conversion=None, format_spec=None)
                )
            else:
                node.replace(replacement_name)

        for call in self.calls:
            self.replace_code_with_call(call)

        new_method = self.new_method._replace(body=self.new_method.body)
        new_function = self.create_new_function(new_method)

        self.node.parent.insert(self.node_index + 1, new_function)

    def replace_code_with_call(self, call: CallToMethod) -> None:
        new_call = self.create_call(
            attr=call.attribute,
            call_arguments=call.arguments,
            new_func=self.new_method.name,
            returns=ends_with_return(self.new_method.body),
            assigned_variable=call.assigned_var,
        )
        statements = call.code_to_replace.statements
        parent = statements[0].parent
        beginning = parent.statements.index(statements[0])
        end = parent.statements.index(statements[-1])
        new_call.lineno = statements[0].lineno
        parent[beginning : end + 1] = (new_call,)
        new_call.parent = parent

    def create_new_function(self, new_method: ExtractedMethod) -> FunctionDef:
        args = Parameters(
            tuple(Param(Name(name), None, None) for name in new_method.arguments),
        )

        function_method_body = new_method.body
        if new_method.add_result_return:
            function_return = Return(Name("result"))
            function_method_body = function_method_body + (function_return,)

        return FunctionDef(
            (),
            Name(new_method.name),
            args,
            None,
            None,
            Block(function_method_body),
            is_async=Flag(False),
        )

    def create_call(
        self,
        attr: str,
        call_arguments: List[Expression],
        new_func: str,
        returns: bool,
        assigned_variable: Optional[Expression],
    ) -> Statement:
        call_args = tuple(call_arguments) if call_arguments else ()
        function_name = (
            Attribute(Name(attr), Name(new_func)) if attr else Name(new_func)
        )
        new_call = Call(function_name, call_args)

        if returns:
            return Return(new_call)
        elif assigned_variable:
            return Assign((assigned_variable,), new_call)
        else:
            return Expr(new_call)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        # TODO Need to handle self appropriately to sort some of these out
        return {
            LocalChangeOnException,
            LocalValueMissing,
            ReturnValuesChanged,
            ExceptionArgsChanged,
            ReturnValuesChangedOnException,
            ExceptionTypeChanged,
            FunctionCallsOnException,
        }


class ExtractDuplicateMethodProposal(BaseExtractMethodProposal):
    def description(self):
        is_function = not is_class_function(self.node)
        return EXTRACT_DUP_FUNCTION_DESC if is_function else EXTRACT_DUP_METHOD_DESC


class ExtractMethodProposal(BaseExtractMethodProposal):
    def description(self):
        is_function = not is_class_function(self.node)
        return EXTRACT_FUNC_DESC if is_function else EXTRACT_METHOD_DESC
