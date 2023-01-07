import inspect


def track_step_code(run, func):
    run.fields.source_code = inspect.getsource(func)
