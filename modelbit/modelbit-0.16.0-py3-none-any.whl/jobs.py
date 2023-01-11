from typing import Callable, Any, cast, Optional
import functools, re


class ModelbitJobResult:

  def __init__(self, func: Callable[..., Any], redeploy_on_success: bool, schedule: Optional[str] = None):
    if not callable(func):
      raise Exception("Only functions can be decorated as jobs.")
    try:
      self.mb_func = func
      self.mb_obj = self.mb_func()
    except Exception as err:
      if "required positional argument" in str(err):
        raise Exception(
            "Job function arguments require default values. Example: change train(foo) into train(foo = 1).")
      raise err
    if func.__name__ == "source":  # avoid collisions with source.py
      raise Exception("The job function cannot be named 'source'")
    self.mb_redeployOnSuccess = redeploy_on_success
    self.mb_schedule = schedule

  def __getattr__(self, attr: str):
    return getattr(self.mb_obj, attr)

  def __getitem__(self, item: Any):
    return self.mb_obj.__getitem__(item)

  def __str__(self):
    return str(self.mb_obj)

  def __repr__(self):
    return self.__str__()

  def __dir__(self):
    return self.mb_obj.__dir__()


def jobDecorator(f: Any = None, *, redeploy_on_success: bool = True, schedule: Optional[str] = None):
  if f is None:
    # decorator with parentheses and arguments
    return cast(Callable[..., ModelbitJobResult],
                functools.partial(jobDecorator, redeploy_on_success=redeploy_on_success, schedule=schedule))

  else:
    # bare decorator, no parentheses or arguments
    @functools.wraps(f)
    def wrapper():
      return ModelbitJobResult(f, redeploy_on_success=redeploy_on_success, schedule=schedule)

    return wrapper


def stripJobDecorators(source: str) -> str:
  for decorator in ["@modelbit.job", "@jobDecorator", "@job"]:
    source = re.sub("(?sm)" + decorator + r".*def", "def", source, re.M)
  return source
