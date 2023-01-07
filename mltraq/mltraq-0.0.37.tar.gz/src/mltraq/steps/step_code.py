import joblib
from mltraq import Run


def track_step_code(run: Run, step):
    if "steps_code" not in run.fields:
        run.fields.steps_code = {}
        func_code, source_file, _ = joblib.func_inspect.get_func_code(step)
        run.fields.steps_code[step.__name__] = {"func_code": func_code, "source_file": source_file}
