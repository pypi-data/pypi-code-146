import re
from simpleeval import simple_eval, NameNotDefined, AttributeDoesNotExist


class Expression:
    def __init__(self, expr):
        self.expr = expr

    def eval(self, context):
        raise NotImplementedError


class Bind(Expression):
    def eval(self, context):
        try:
            return simple_eval(self.expr, names=context)
        except AttributeDoesNotExist as e:
            obj = e.expression.split(e.attr)[0][:-1]  # page.valami; e.attr=valami
            if context.get(obj, None) is None:
                return None

        raise ValueError


class Condition(Bind):
    pass


class ForLoop(Expression):
    REGEX = re.compile(r'^\s*(.+)\s+in\s+(.+)\s*$')

    def __init__(self, expr):
        super().__init__(expr)
        m = self.REGEX.match(expr)
        if m:
            self.loop_variable = m.groups()[0].strip()
            if not self.loop_variable.isidentifier():
                raise SyntaxError(f'Not valid identifier name: {self.loop_variable}')
            self.iterable = m.groups()[1].strip()
        else:
            raise SyntaxError(f'For loop syntax error: {expr}')

    def eval(self, context):
        try:
            iterable = simple_eval(f'{self.iterable}', names=context)
            for counter, item in enumerate(iterable, start=1):
                yield counter, self.loop_variable, item
        except NameNotDefined as e:
            raise ValueError(f'"{self.iterable}" is not defined in context') from e
