from spy import ir
from spy.vm import SPyVM
from spy.vm import wt, W_Primitive, W_Function, W_Module
from spy.tests.support import spy_parse

def make_vm():
    w_mod = W_Module('mod_for_tests')
    return SPyVM(w_mod)

def test_W_Primitive():
    w_a = W_Primitive(wt.i32, 10)
    assert w_a.unwrap() == (wt.i32, 10)

def test_wrap():
    vm = make_vm()
    w_a = vm.wrap(42)
    assert isinstance(w_a, W_Primitive)
    assert w_a.unwrap() == (wt.i32, 42)

def test_i32_const():
    expr = ir.Const(42)
    vm = None
    frame = None
    w_res = expr.vm_eval(vm, frame)
    assert isinstance(w_res, W_Primitive)
    assert w_res.unwrap() == (wt.i32, 42)

def test_i32_add():
    a = ir.Const(20)
    b = ir.Const(22)
    expr = ir.Add(a, b)
    vm = None
    frame = None
    w_res = expr.vm_eval(vm, frame)
    assert w_res.unwrap() == (wt.i32, 42)

def test_i32_mul():
    a = ir.Const(5)
    b = ir.Const(6)
    expr = ir.Mul(a, b)
    vm = None
    frame = None
    w_res = expr.vm_eval(vm, frame)
    assert w_res.unwrap() == (wt.i32, 30)

def test_block():
    expr = ir.Block([
        ir.Const(1),
        ir.Const(2),
        ir.Const(3),
    ])
    vm = make_vm()
    frame = vm.new_frame()
    w_res = expr.vm_eval(vm, frame)
    assert w_res.unwrap() == (wt.i32, 3)

def test_locals_and_block():
    expr = ir.Block([
        ir.Assign('x', ir.Const(123)),
        ir.GetLocal('x'),
    ])
    vm = make_vm()
    frame = vm.new_frame()
    w_res = expr.vm_eval(vm, frame)
    assert w_res.unwrap() == (wt.i32, 123)

def test_func():
    wt_func = wt.function([wt.i32, wt.i32], wt.i32)
    param_names = ['x', 'y']
    body = ir.Block([
        ir.Return(
            ir.Add(
                ir.GetLocal('x'),
                ir.GetLocal('y'))),
        ])
    w_func = W_Function('add', wt_func, ['x', 'y'], body)
    vm = make_vm()
    args_w = [vm.wrap(10), vm.wrap(20)]
    w_res = w_func.call(vm, args_w)
    assert w_res.unwrap() == (wt.i32, 30)

def test_call():
    mod = spy_parse("""
    def a(x: i32) -> i32:
        return b(x) * 2

    def b(x: i32) -> i32:
        return x + 3
    """)
    vm = SPyVM(mod)
    w_a = vm.get_w_function('a')
    args_w = [vm.wrap(5)]
    w_res = w_a.call(vm, args_w)
    assert w_res.unwrap() == (wt.i32, 16)
