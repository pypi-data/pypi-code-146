"""
SPY IR backend.

Compiles the IR into various outputs such as WAT.
"""

import sexpdata
from spy import ir

def compile_module_to_wat(w_mod):
    """
    Compile a W_Module to WASM.
    """
    funcs_w = w_mod._functions_w.values()
    funcs = [compile_func_to_sexp(w_f) for w_f in funcs_w]
    exports = [[Sym('export'), w_f.name, [Sym('func'), Name(w_f.name)]]
               for w_f in funcs_w]
    sexp = [Sym('module')] + funcs + exports
    return sexpdata.dumps(sexp)

def compile_func_to_sexp(w_func):
    sexp = [Sym('func'), Name(w_func.name)]
    for param, wt_param in w_func.get_params():
        sexp.append([Sym('param'), Name(param), Sym(wt_param.name)])
    sexp.append([Sym('result'), Sym(w_func.wt_func.wt_return.name)])
    assert isinstance(w_func.ir_body, ir.Block)

    # first, we declare all local variables. XXX: for now we simple search for
    # the appropriate ir.local_set statements, but we soon need a proper
    # symbol table and typechecking phase.
    for ir_stmt in w_func.ir_body.statements:
        if isinstance(ir_stmt, ir.Assign) and ir_stmt.wt_type is not None:
            sexp.append([Sym('local'), Name(ir_stmt.name,), Sym(ir_stmt.wt_type.name)])

    for ir_stmt in w_func.ir_body.statements:
        sexp.append(ir_stmt.to_sexp())
    return sexp

def compile_func_to_wat(w_func):
    sexp = compile_func_to_sexp(w_func)
    return sexpdata.dumps(sexp)


class Sym(sexpdata.SExpBase):
    """
    Similar to sexpdata.Symbol, but doesn't quote its value
    """

    def tosexp(self, tosexp=None):
        return self._val

class Name(sexpdata.SExpBase):
    """
    Like Sym, but automatically add a $ prefix
    """

    def tosexp(self, tosexp=None):
        return '$' + self._val


@ir.extend
class Expr:
    def to_wat(self):
        return sexpdata.dumps(self.to_sexp())

    def to_sexp(self):
        raise NotImplementedError(self.__class__.__name__)


@ir.extend
class Const:
    def to_sexp(self):
        return [Sym('i32.const'), self.value]


@ir.extend
class Add:
    def to_sexp(self):
        return [Sym('i32.add'),
                self.left.to_sexp(),
                self.right.to_sexp()]


@ir.extend
class Lt:
    def to_sexp(self):
        # XXX: this assumes that the operands are i32, but we need a better
        # typechecking
        return [Sym('i32.lt_s'),
                self.left.to_sexp(),
                self.right.to_sexp()]


@ir.extend
class LtE:
    def to_sexp(self):
        # XXX: this assumes that the operands are i32, but we need a better
        # typechecking
        return [Sym('i32.le_s'),
                self.left.to_sexp(),
                self.right.to_sexp()]


@ir.extend
class GtE:
    def to_sexp(self):
        # XXX: this assumes that the operands are i32, but we need a better
        # typechecking
        return [Sym('i32.ge_s'),
                self.left.to_sexp(),
                self.right.to_sexp()]

@ir.extend
class Gt:
    def to_sexp(self):
        # XXX: this assumes that the operands are i32, but we need a better
        # typechecking
        return [Sym('i32.gt_s'),
                self.left.to_sexp(),
                self.right.to_sexp()]


@ir.extend
class Eq:
    def to_sexp(self):
        # XXX: this assumes that the operands are i32, but we need a better
        # typechecking
        return [Sym('i32.eq'),
                self.left.to_sexp(),
                self.right.to_sexp()]


@ir.extend
class NotEq:
    def to_sexp(self):
        # XXX: this assumes that the operands are i32, but we need a better
        # typechecking
        return [Sym('i32.ne'),
                self.left.to_sexp(),
                self.right.to_sexp()]


@ir.extend
class Block:
    def to_sexp(self):
        res = [Sym('block')]
        for child in self.statements:
            res.append(child.to_sexp())
        return res


@ir.extend
class GetLocal:
    def to_sexp(self):
        return [Sym('local.get'), Name(self.name)]


@ir.extend
class Assign:
    def to_sexp(self):
        return [Sym('local.set'),
                Name(self.name),
                self.expr.to_sexp()]


@ir.extend
class Call:

    def to_sexp(self):
        res = [Sym('call'), Name(self.func)]
        for arg in self.args:
            res.append(arg.to_sexp())
        return res


@ir.extend
class Return:

    def to_sexp(self):
        return [Sym('return'), self.expr.to_sexp()]
