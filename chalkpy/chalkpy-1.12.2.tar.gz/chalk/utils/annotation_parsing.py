import ast
import inspect
import textwrap
from typing import Any, Callable, Dict, Optional

from chalk.df.ast_parser import convert_slice, eval_converted_expr


class ResolverAnnotationParser:
    def __init__(self, resolver: Callable, glbs: Optional[Dict[str, Any]], lcls: Optional[Dict[str, Any]]):
        self.resolver = resolver
        self.glbs = glbs
        self.lcls = lcls

        self._args = {arg.arg: arg for arg in self._get_resolver_args()}

    def _get_resolver_args(self):
        source = inspect.getsource(self.resolver)
        parsed_source = ast.parse(textwrap.dedent(source))
        assert len(parsed_source.body) == 1
        function_def = parsed_source.body[0]
        assert isinstance(function_def, ast.FunctionDef)
        args = function_def.args
        all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
        return all_args

    def parse_annotation(self, name: str):
        arg = self._args[name]
        annotation = arg.annotation
        assert annotation is not None
        if isinstance(annotation, ast.Constant):
            val = annotation.value
            assert isinstance(val, str), "if a literal annotation, it must be a string"
            # string of type annotation
            val = ast.parse(val, mode="eval")
            assert isinstance(val, ast.Module)
            annotation = val.body
        if isinstance(annotation, ast.Subscript):
            # All fancy ast parsing would appear within the subscript of a df __getitem__
            annotation = ast.Subscript(
                value=annotation.value,
                slice=convert_slice(annotation.slice),
                ctx=annotation.ctx,
            )
        return eval_converted_expr(annotation, self.glbs, self.lcls)
