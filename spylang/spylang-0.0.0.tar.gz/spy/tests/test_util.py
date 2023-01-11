import pytest
import textwrap
from spy.util import MagicExtend

def test_MagicExtend():

    extend = MagicExtend('MyModule')

    class MyModule:
        @extend.register
        class A:
            pass

    @extend
    class A:
        x = 42

    assert A is MyModule.A
    assert A.x == 42

    with pytest.raises(AttributeError, match='class B is not registered as extendable'):
        @extend
        class B:
            pass

def test_MagicExtend_dump_skeleton():

    extend = MagicExtend('spy.mymod')

    @extend.register
    class A:
        pass

    @extend.register
    class B:
        pass

    skeleton = extend.dump_skeleton()
    assert skeleton.strip() == textwrap.dedent("""
        from spy import mymod

        @mymod.extend
        class A:
            pass


        @mymod.extend
        class B:
            pass
    """).strip()
