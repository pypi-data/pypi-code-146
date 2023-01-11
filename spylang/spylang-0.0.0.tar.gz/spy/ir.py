from dataclasses import dataclass
from spy.util import MagicExtend
from spy.vm import wt, W_Type

extend = MagicExtend('spy.ir')

def irclass(cls):
    """
    This is just a shortcut: it automatically applies the following decorators
    to all IR nodes:

        @extend.register
        @dataclass
    """
    return extend.register(dataclass(cls))


# ==========================
# AST hierarchy
# ==========================

@irclass
class Node:

    def is_green(self):
        return False


@irclass
class Expr(Node):

    def get_type(self):
        raise NotImplementedError


@irclass
class Const(Expr):
    # XXX for now we assume that it's an i32 const
    value: int

    def __init__(self, value):
        self.value = value

    def get_type(self):
        return wt.i32

    def is_green(self):
        return True


@irclass
class BinOp(Expr):
    left: Expr
    right: Expr


@irclass
class Add(BinOp):

    def get_type(self):
        return wt.i32


@irclass
class Mul(BinOp):

    def get_type(self):
        return wt.i32


@irclass
class Block(Expr):
    statements: list # List[Expr]


@irclass
class GetLocal(Expr):
    name: str


@irclass
class Assign(Expr):
    name: str
    expr: Expr
    wt_type: W_Type = None


@irclass
class Call(Expr):
    func: str
    args: list  # List[Expr]


@irclass
class Lt(BinOp):
    pass

@irclass
class LtE(BinOp):
    pass

@irclass
class Gt(BinOp):
    pass

@irclass
class GtE(BinOp):
    pass

@irclass
class Eq(BinOp):
    pass

@irclass
class NotEq(BinOp):
    pass


@irclass
class Return(Node):
    expr: Expr
