import pytest
from spy.symtable import SymTable, SymbolAlreadyDeclaredError
from spy.vm import wt

def test_basic():
    t = SymTable('<globals>')
    sym = t.declare('a', wt.i32)
    assert sym.name == 'a'
    assert sym.wt_type == wt.i32
    assert t.lookup('a') is sym
    assert t.lookup('I-dont-exist') is None
    #
    with pytest.raises(SymbolAlreadyDeclaredError):
        t.declare('a', wt.i32)


def test_nested_table_lookup():
    glob = SymTable('<globals>')
    loc = SymTable('loc', glob)
    sym_a = glob.declare('a', wt.i32)
    sym_b = loc.declare('b', wt.i32)
    #
    assert glob.lookup('a') is sym_a
    assert glob.lookup('b') is None
    #
    assert loc.lookup('a') is sym_a
    assert loc.lookup('b') is sym_b
