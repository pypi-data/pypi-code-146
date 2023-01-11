from spy import ir
from spy.vm import SPyVM, wt, meta_eval
from spy.backend import compile_module_to_wat, compile_func_to_wat
from spy.tests.support import spy_parse, sexp_equal


class TestMetaEval:

    def meta_eval(self, src):
        w_mod = spy_parse(src)
        return meta_eval(w_mod)

    def test_simple(self):
        w_mod = self.meta_eval("""
        def foo() -> i32:
            return 1+2
        """)

        w_foo = w_mod.lookup('foo')
        assert w_foo.ir_body == ir.Block([
            ir.Return(
                ir.Add(left=ir.Const(1),
                       right=ir.Const(2))
            )
        ])

    def test_red_call(self):
        w_mod = self.meta_eval("""
        def foo() -> i32:
            return 42

        def bar() -> i32:
            return foo()
        """)
        w_bar = w_mod.lookup('bar')
        assert w_bar.ir_body == ir.Block([
            ir.Return(
                ir.Call('foo', []),
            )
        ])

    def test_green_call(self):
        w_mod = self.meta_eval("""
        def FOO() -> i32:
            return 42

        def bar() -> i32:
            return FOO()
        """)
        w_bar = w_mod.lookup('bar')
        assert w_bar.ir_body == ir.Block([
            ir.Return(
                ir.Const(42)
            )
        ])

    def test_green_call_with_arguments(self):
        w_mod = self.meta_eval("""
        def FOO(a: i32, b: i32) -> i32:
            return a+b

        def bar() -> i32:
            return FOO(10, 20)
        """)
        w_bar = w_mod.lookup('bar')
        assert w_bar.ir_body == ir.Block([
            ir.Return(
                ir.Const(30)
            )
        ])
