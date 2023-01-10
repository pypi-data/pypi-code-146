from functools import partial
from typing import Any
from front.crude import Crudifier

mall = dict(tagged_wf=dict())
crudifier = partial(Crudifier, mall=mall, include_stores_attribute=True)
WaveForm = Any


@crudifier(output_store='tagged_wf', output_trans=lambda: None)
def tag_wf(wf: WaveForm, tag: str):
    return (wf, tag)


@crudifier(param_to_mall_map=dict(x='tagged_wf'))
def get_tagged_wf(x: Any):
    return x


funcs = [tag_wf, get_tagged_wf]
