def get_apifuncs(api, funcs):
    # TODO: Not robust. Api should provide a get_funcs method perhaps?
    for func in funcs:
        yield getattr(api, func.__name__)


if __name__ == '__main__':
    # import os
    # print("file: {}".format(os.path.realpath(__file__)))

    # What I want to dispatch
    from plunk.tw.py2py_front_example.simple_pycode import foo, bar, confuser

    funcs = [foo, bar, confuser]

    kind_of_dispatch = 'funcs'
    kind_of_dispatch = 'httppy_funcs'

    # My dispatching the funcs directly
    from streamlitfront.base import dispatch_funcs

    if kind_of_dispatch == 'funcs':
        app = dispatch_funcs(funcs)
    elif kind_of_dispatch == 'httppy_funcs':
        from http2py import HttpClient

        api_url = 'http://127.0.0.1:3030'  # TODO: should get this from service object
        api = HttpClient(url=f'{api_url}/openapi')  # Why openapi?
        app = dispatch_funcs(list(get_apifuncs(api, funcs)))
    else:
        raise ValueError(f'Unknown {kind_of_dispatch=}')

    # launch the app
    app()  # TODO: perhaps we can have this do the `streamlit run...` itself?
