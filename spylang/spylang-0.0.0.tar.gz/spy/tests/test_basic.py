from spy.tests.support import SPyTest

class TestBasic(SPyTest):

    def test_simple(self):
        mod = self.compile("""
            def foo() -> i32:
                return 42

            def bar() -> i32:
                return 43
        """)
        assert mod.foo() == 42
        assert mod.bar() == 43

    def test_args(self):
        mod = self.compile("""
            def add(x: i32, y: i32) -> i32:
                return x + y
        """)
        assert mod.add(40, 2) == 42

    def test_cmp_operators(self):
        # XXX: comparison operators should return bool, but we haven't introduced this type yet
        mod = self.compile("""
            def lt(x: i32, y: i32) -> i32: return x < y
            def le(x: i32, y: i32) -> i32: return x <= y
            def ge(x: i32, y: i32) -> i32: return x >= y
            def gt(x: i32, y: i32) -> i32: return x > y
            def eq(x: i32, y: i32) -> i32: return x == y
            def ne(x: i32, y: i32) -> i32: return x != y
        """)
        assert mod.lt(3, 4)
        assert not mod.lt(4, 3)
        assert mod.le(3, 3)
        assert not mod.le(4, 3)
        assert mod.ge(3, 3)
        assert not mod.ge(3, 4)
        assert mod.gt(4, 3)
        assert not mod.gt(3, 3)
        assert mod.eq(3, 3)
        assert not mod.eq(3, 4)
        assert mod.ne(3, 4)
        assert not mod.ne(3, 3)

    def test_local_set(self):
        mod = self.compile("""
            def foo() -> i32:
                a: i32 = 42
                return a

            def bar() -> i32:
                a: i32 = 42
                a = 100
                return a
        """)
        assert mod.foo() == 42
        assert mod.bar() == 100
