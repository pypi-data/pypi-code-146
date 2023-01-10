from functools import partial

# from typing import Callable
from collections.abc import Callable
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from front import Crudifier

mall = dict(
    func=dict(StandardScaler=StandardScaler, KMeans=KMeans, linreg=LinearRegression),
    parametrized_funcs=dict(),
)

crudify = partial(Crudifier, mall=mall)


def str_to_dict(string):
    import json

    return json.loads(string)


def dict_maker(**kwargs):
    return dict(**kwargs)


@crudify('func', output_store='parametrized_funcs')
def factory(func, kwargs='()'):
    kwargs = str_to_dict(kwargs)
    return partial(func, **kwargs)


def foo(x):
    return x + 1


if __name__ == '__main__':
    from streamlitfront import mk_app
    from front.util import deep_merge
    from streamlitfront import dispatch_funcs

    # app = dispatch_funcs([factory])

    import front as f
    import streamlitfront.elements as sf

    # my_convention = {
    #     # f.APP_KEY: {'title': 'apply_func_to_wf'},
    #     f.RENDERING_KEY: {
    #         Callable: {
    #             'execution': {
    #                 'inputs': {
    #                     'func': {
    #                         f.ELEMENT_KEY: sf.SelectBox,
    #                         'options': list(mall['func'])
    #                     },
    #                 },
    #             }
    #         },
    #     }
    # }

    my_config = {
        # f.APP_KEY: {'title': 'apply_func_to_wf'},
        f.RENDERING_KEY: {
            'factory': {
                'execution': {
                    'inputs': {
                        'func': {
                            f.ELEMENT_KEY: sf.SelectBox,
                            'options': list(mall['func']),
                        },
                    },
                }
            },
        }
    }

    from i2 import Sig

    @Sig(KMeans)
    def kmeans(*args, **kwargs):
        return KMeans(*args, **kwargs)

    def change_types_to_callable(x):
        if isinstance(x, type):
            x = partial(x)
        return x

    app = mk_app([factory, kmeans], config=my_config,)
    app()

    import streamlit as st

    st.write(mall)
