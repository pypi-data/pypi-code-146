from dataclasses import dataclass

class W_Root:
    """
    Base class for all SPy VM objects.
    """

class W_Module(W_Root):
    """
    A module is the basic unit of compilation.

    A module represents a namespace which contains functions and other
    objects. It is compiled into a WASM module.
    """

    def __init__(self, name):
        self._name = name
        self._functions_w = {}

    def add(self, w_func):
        # XXX we need to think and decide what happens in this case
        assert w_func.name not in self._functions_w
        self._functions_w[w_func.name] = w_func

    def lookup(self, func_name):
        # XXX which kind of exception do we want to raise here? An
        # interp-level or app-level exception?
        return self._functions_w[func_name]


class FunctionReturn(Exception):
    """
    Not a real exception. Used to implement the 'return' statement.
    """

    def __init__(self, w_result):
        self.w_result = w_result


@dataclass
class W_Function(W_Root):

    name: str
    wt_func: "W_Type"
    param_names: list  # List[str]
    ir_body: "ir.expr"

    def post_init(self):
        assert len(wt_func.args_wt) == len(self.param_names)

    def get_params(self):
        """
        Return a list of [(param_name, wt_type), ...]
        """
        return zip(self.param_names, self.wt_func.args_wt)

    def __str__(self):
        return '<W_Function %s>' % (self.name)

    def call(self, vm, args_w):
        """
        Create a new frame, set the arguments, eval the body
        """
        # XXX: we need better typecheck and error reporting
        assert len(args_w) == self.wt_func.n_args
        frame = vm.new_frame()
        for w_arg, wt_arg, name in zip(args_w, self.wt_func.args_wt, self.param_names):
            assert w_arg.wt_value == wt_arg # poor's man typecheck
            frame.set(name, w_arg)
        try:
            w_result = self.ir_body.vm_eval(vm, frame)
            # a function body should never return a value. If it does, it's
            # probably a bug in the parser
            assert w_result is None
        except FunctionReturn as exc:
            return exc.w_result

    def is_green(self):
        # XXX: for now the green functions are the ones in UPPERCASE. We might
        # want to switch to a dedicated syntax at some point.
        return self.name.isupper()

    def vm_meta_eval(self, vm):
        ir_body = self.ir_body.vm_meta_eval(vm)
        return W_Function(self.name, self.wt_func, self.param_names, ir_body)
