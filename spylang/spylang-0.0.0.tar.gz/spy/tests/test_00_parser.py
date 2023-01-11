import pytest
from spy import ir
from spy.vm import wt
from spy.tests.support import SPyTest

class TestParser(SPyTest):

    @pytest.fixture
    def spy_eval_strategy(self, request):
        return 'this-is-only-for-parsing'

    def test_minimal(self):
        w_mod = self.parse("""
        def foo() -> i32:
            return 42
        """)
        w_func = w_mod.lookup('foo')
        assert w_func.name == 'foo'
        assert w_func.wt_func == wt.function([], wt.i32)
        assert w_func.param_names == []
        #
        ir_expected = ir.Block([
            ir.Return(
                ir.Const(42)
            ),
        ])
        assert w_func.ir_body == ir_expected

    def test_add(self):
        w_mod = self.parse("""
        def add(x: i32, y: i32) -> i32:
            return x+y
        """)
        w_func = w_mod.lookup('add')
        assert w_func.name == 'add'
        assert w_func.wt_func == wt.function([wt.i32, wt.i32], wt.i32)
        assert w_func.param_names == ['x', 'y']
        ir_expected = ir.Block([
            ir.Return(
                ir.Add(
                    left=ir.GetLocal('x'),
                    right=ir.GetLocal('y')
                )
            )
        ])
        assert w_func.ir_body == ir_expected
