from __future__ import annotations

from typing import Any

try:
    from imblearn import over_sampling, pipeline, under_sampling
except ModuleNotFoundError:
    pass  # error message in typing.py


async def imb_pipeline(
    *args: Any,
    **kwargs: Any,
) -> Any:
    return pipeline.Pipeline(*args, **kwargs)


async def imb_random_under_sampler(
    *args: Any,
    **kwargs: Any,
) -> Any:
    return under_sampling.RandomUnderSampler(*args, **kwargs)


async def imb_smotenc(
    *args: Any,
    **kwargs: Any,
) -> Any:
    return over_sampling.SMOTENC(*args, **kwargs)
