from __future__ import annotations

from typing import Any

try:
    import skopt
except ModuleNotFoundError:
    pass  # error message in typing.py


async def skopt_bayes_search_cv(*args: Any, **kwargs: Any) -> Any:
    return skopt.BayesSearchCV(*args, **kwargs)
