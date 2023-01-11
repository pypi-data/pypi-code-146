"""
SPy parser.

The goal is to turn the source code into the SPy IR. For the sake of
simplicity, for now we are reusing the Python parser, so the job of this
module is to translate the Python AST into the SPy IR.  Eventually, we will
probably want to write our own SPy-specific parser, to be able to tweak the
syntax.

Note that for now the SPy IR is just an Abstract Syntax Tree. To avoid
confusion, we adopt the following naming convention:

  - When we talk about the AST, we talk about the Python AST, i.e. the ast.*
    module.  There should be no references to the Python AST outside this
    module.

  - When we talk SPy Abstract Syntax Tree, we call it IR, and it's
    implemented by spy.ir.*.
"""

import ast
from astpretty import pprint as pp
from spy.util import MagicExtend
from spy import ir
from spy.vm import wt, W_Module, W_Function


def parse(src):
    tree = ast.parse(src)
    return tree.to_spy_ir()


def parse_and_meta_eval(src):
    from spy.vm import SPyVM
    w_mod = parse(src)
    vm = SPyVM(w_mod)
    w_mod2 = vm.meta_eval_module(w_mod)
    return w_mod2

def parse_type(name: ast.Name):
    assert type(name) is ast.Name


# ===================
# AST magic
# ===================

def make_ast_extend():
    """
    some magic to let us @extend ast.* classes
    """
    ast_extend = MagicExtend('ast')
    for obj in ast.__dict__.values():
        if type(obj) is type and issubclass(obj, ast.AST):
            ast_extend.register(obj)
    return ast_extend

ast_extend = make_ast_extend()


@ast_extend
class Module:
    def to_spy_ir(self):
        for child in self.body:
            if not isinstance(child, ast.FunctionDef):
                raise Exception('Invalid child of module: %s' % child)

        funcs_w = [f.to_spy_ir() for f in self.body]
        name = 'mymodule' # XXX
        w_mod = W_Module(name)
        for w_func in funcs_w:
            w_mod.add(w_func)
        return w_mod


@ast_extend
class FunctionDef:
    def to_spy_ir(self):
        name = self.name
        param_names, args_wt = self.args.as_spy_params()
        wt_return = self.returns.as_spy_type()
        #
        ir_stmts = []
        for py_stmt in self.body:
            ir_stmts.append(py_stmt.to_spy_ir())
        ir_body = ir.Block(ir_stmts)
        wt_func = wt.function(args_wt, wt_return)
        return W_Function(name, wt_func, param_names, ir_body)


@ast_extend
class Return:
    def to_spy_ir(self):
        return ir.Return(self.value.to_spy_ir())

@ast_extend
class Name:
    def as_spy_type(self):
        try:
            return getattr(wt, self.id)
        except AttributeError:
            raise Exception(f'Unknown SPY type: {name.id}')

    def to_spy_ir(self):
        return ir.GetLocal(self.id)


@ast_extend
class arguments:
    def as_spy_params(self):
        param_names = []
        args_wt = []
        for arg in self.args:
            if arg.annotation is None:
                raise Exception('function arguments must have a type')
            args_wt.append(arg.annotation.as_spy_type())
            param_names.append(arg.arg)
        return param_names, args_wt


@ast_extend
class Expr:
    def to_spy_ir(self):
        return self.value.to_spy_ir()


@ast_extend
class BinOp:
    def to_spy_ir(self):
        op = self.op.__class__.__name__
        if op == 'Add':
            # XXX: here we assume it's i32 but we need a proper typechecking phase
            return ir.Add(self.left.to_spy_ir(),
                          self.right.to_spy_ir())
        elif op == 'Mult':
            return ir.Mul(self.left.to_spy_ir(),
                          self.right.to_spy_ir())
        else:
            raise Exception(f'Unknown op: {op}')


@ast_extend
class Constant:
    def to_spy_ir(self):
        assert type(self.value) is int
        return ir.Const(self.value)


@ast_extend
class Call:
    def to_spy_ir(self):
        # this is very fragile: it assumes that the callee exists in the
        # module that we are compiling. We should check this at compile time
        # and report errors properly. Also, we assume that we are calling a
        # Name.
        assert isinstance(self.func, ast.Name)
        callee = self.func.id
        args = [arg.to_spy_ir() for arg in self.args]
        return ir.Call(callee, args)


@ast_extend
class Compare:
    def to_spy_ir(self):
        assert len(self.ops) == 1
        assert len(self.comparators) == 1
        opname = self.ops[0].__class__.__name__ # Gt, Lt, etc.
        ir_op = getattr(ir, opname)
        ir_left = self.left.to_spy_ir()
        ir_right = self.comparators[0].to_spy_ir()
        return ir_op(ir_left, ir_right)


@ast_extend
class AnnAssign:
    def to_spy_ir(self):
        assert isinstance(self.target, ast.Name)
        name = self.target.id
        wt_type = self.annotation.as_spy_type()
        ir_expr = self.value.to_spy_ir()
        return ir.Assign(name, ir_expr, wt_type=wt_type)


@ast_extend
class Assign:
    def to_spy_ir(self):
        assert len(self.targets) == 1
        target = self.targets[0]
        assert isinstance(target, ast.Name)
        name = target.id
        ir_expr = self.value.to_spy_ir()
        return ir.Assign(name, ir_expr)
