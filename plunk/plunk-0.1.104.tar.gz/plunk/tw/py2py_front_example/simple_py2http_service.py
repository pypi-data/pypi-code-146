if __name__ == '__main__':
    # What I want to dispatch
    from plunk.tw.py2py_front_example.simple_pycode import foo, bar, confuser

    funcs = [foo, bar, confuser]

    # My dispatching
    from py2http import run_app

    run_app(funcs, publish_openapi=True)
