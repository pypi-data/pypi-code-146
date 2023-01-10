from functools import partial
from front.crude import Crudifier

mall = dict(
    a=dict(one=1, two=2), b=dict(three=3, four=4), foo_output=dict(), bar_output=dict(),
)
crudifier = partial(Crudifier, mall=mall, include_stores_attribute=True)


@crudifier(param_to_mall_map=['a', 'b'], output_store='foo_output')
def foo(a, b: float):
    """This is foo. It computes something"""
    return a + b


@crudifier(param_to_mall_map=['foo_output'], output_store='bar_output')
def bar(foo_output: float):
    return foo_output * 10


funcs = [foo, bar]
