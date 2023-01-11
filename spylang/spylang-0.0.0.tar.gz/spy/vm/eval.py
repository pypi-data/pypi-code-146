import operator
from spy import ir
from spy.vm import wt, W_Primitive, W_Function
from spy.vm.objects import FunctionReturn

@ir.extend
class Node:
    def vm_meta_eval(self, vm):
        """
        Perform meta evaluation and return an AST tree where some of the nodes has
        already been evaluated.

        The default implementation is to return a copy of itself after having
        recursively applied vm_meta_eval() to all children node.
        """
        def apply_vm_meta_eval_maybe(x):
            if hasattr(x, 'vm_meta_eval'):
                return x.vm_meta_eval(vm)
            return x

        new_fields = {}
        for name in self.__dataclass_fields__:
            value = getattr(self, name)
            if isinstance(value, ir.Node):
                # recursively apply vm_meta_eval
                value = value.vm_meta_eval(vm)
            elif isinstance(value, list):
                value = [apply_vm_meta_eval_maybe(x) for x in value]
            #
            new_fields[name] = value
        return self.__class__(**new_fields)


@ir.extend
class Expr:
    def vm_eval(self, vm, frame):
        raise NotImplementedError


@ir.extend
class Const:
    def vm_eval(self, vm, frame):
        return W_Primitive(wt.i32, self.value)


@ir.extend
class BinOp:

    def _binop_eval(self, vm, frame, op):
        w_left = self.left.vm_eval(vm, frame)
        w_right = self.right.vm_eval(vm, frame)
        # XXX we need proper typecheck and better error reporting
        assert isinstance(w_left, W_Primitive)
        assert isinstance(w_right, W_Primitive)
        res = op(w_left.value, w_right.value)
        return W_Primitive(wt.i32, res)


@ir.extend
class Add:
    def vm_eval(self, vm, frame):
        return self._binop_eval(vm, frame, operator.add)

@ir.extend
class Mul:
    def vm_eval(self, vm, frame):
        return self._binop_eval(vm, frame, operator.mul)

@ir.extend
class Lt:
    def vm_eval(self, vm, frame):
        return self._binop_eval(vm, frame, operator.lt)

@ir.extend
class LtE:
    def vm_eval(self, vm, frame):
        return self._binop_eval(vm, frame, operator.le)

@ir.extend
class Gt:
    def vm_eval(self, vm, frame):
        return self._binop_eval(vm, frame, operator.gt)

@ir.extend
class GtE:
    def vm_eval(self, vm, frame):
        return self._binop_eval(vm, frame, operator.ge)

@ir.extend
class Eq:
    def vm_eval(self, vm, frame):
        return self._binop_eval(vm, frame, operator.eq)

@ir.extend
class NotEq:
    def vm_eval(self, vm, frame):
        return self._binop_eval(vm, frame, operator.ne)


@ir.extend
class Block:

    def vm_eval(self, vm, frame):
        val = None
        for s in self.statements:
            val = s.vm_eval(vm, frame)
        return val


@ir.extend
class GetLocal:

    def vm_eval(self, vm, frame):
        return frame.get(self.name)


@ir.extend
class Assign:

    def vm_eval(self, vm, frame):
        val = self.expr.vm_eval(vm, frame)
        frame.set(self.name, val)


@ir.extend
class Return:

    def vm_eval(self, vm, frame):
        w_result = self.expr.vm_eval(vm, frame)
        raise FunctionReturn(w_result)


@ir.extend
class Call:

    def vm_eval(self, vm, frame):
        # XXX better error reporting in case self.func doesn't exist
        w_func = vm.get_w_function(self.func)
        assert isinstance(w_func, W_Function)
        args_w = [arg.vm_eval(vm, frame) for arg in self.args]
        return w_func.call(vm, args_w)

    def vm_meta_eval(self, vm):
        w_func = vm.get_w_function(self.func)
        if w_func.is_green():
            args_w = []
            assert w_func.wt_func.n_args == len(self.args) # XXX better error reporting
            for arg in self.args:
                assert arg.is_green()
                # XXX this is wrong, we should pass a frame and/or have
                # another way to go from i32_const to W_Primitive
                w_arg = arg.vm_eval(vm, None)
                args_w.append(w_arg)

            w_result = w_func.call(vm, args_w)
            # XXX for now we support only i32 prebuilt constants
            assert isinstance(w_result, W_Primitive)
            assert w_result.wt_value == wt.i32
            return ir.Const(w_result.value)
        else:
            args = [arg.vm_meta_eval(vm) for arg in self.args]
            return ir.Call(self.func, args)
