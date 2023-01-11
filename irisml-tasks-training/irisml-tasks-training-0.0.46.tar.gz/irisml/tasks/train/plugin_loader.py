import ast
import importlib
import logging
from irisml.core.variable import replace_variables

logger = logging.getLogger(__name__)


def load_plugin(plugin_expr, context):
    plugin_name, plugin_args = _parse_plugin_expr(plugin_expr, context)

    try:
        plugin_module = importlib.import_module('irisml.tasks.train.plugins.' + plugin_name)
    except ModuleNotFoundError as e:
        raise RuntimeError(f"Plugin {plugin_name} is not found.") from e

    plugin_class = getattr(plugin_module, 'Plugin', None)
    instance = plugin_class(*plugin_args)
    logger.debug(f"Loaded a plugin: {plugin_expr}")
    return instance


def _parse_plugin_expr(plugin_expr, context):
    parsed = ast.parse(plugin_expr)
    if len(parsed.body) != 1:
        raise ValueError(f"Plugin description cannot have multiple expressions: {plugin_expr}")

    if isinstance(parsed.body[0].value, ast.Name):
        plugin_name = parsed.body[0].value.id
        plugin_args = []
    elif isinstance(parsed.body[0].value, ast.Call):
        plugin_name = parsed.body[0].value.func.id
        ast_args = parsed.body[0].value.args
        if not all(isinstance(a, ast.Constant) for a in ast_args):
            raise ValueError(f"Only constant types can be used as plugin arguments: {ast.dump(ast_args)}")
        plugin_args = [a.value for a in ast_args]
        # Resolve variables in the plugin arguments.
        plugin_args = [context.resolve(replace_variables(a)) if isinstance(a, str) else a for a in plugin_args]
    else:
        raise ValueError(f"Unexpected plugin expression: {ast.dump(parsed)}")

    return plugin_name, plugin_args
