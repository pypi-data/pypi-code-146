import click
import ast


class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value):

        if isinstance(value, str):
            try:
                return ast.literal_eval(value)
            except Exception as exception:
                raise click.BadParameter(value) from exception
        else:
            # This happen when the default value is already a typed instance (aka not a string)
            return value


class PythonLiteralArgument(click.Argument):

    def type_cast_value(self, ctx, value):

        if isinstance(value, str):
            try:
                return ast.literal_eval(value)
            except Exception as exception:
                raise click.BadParameter(value) from exception
        else:
            # This happen when the default value is already a typed instance (aka not a string)
            return value
