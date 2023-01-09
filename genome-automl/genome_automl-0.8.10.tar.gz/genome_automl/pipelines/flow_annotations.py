import functools
import time
import logging


"""
attach a "decorator" property to @flow annotated classes
to then be able to initialize the annotated classes generically
"""
def RegisteringDecoratorFactory(foreignDecoratorFactory):
    def newDecoratorFactory(*args, **kw):
        oldGeneratedDecorator = foreignDecoratorFactory(*args, **kw)
        def newGeneratedDecorator(cls):
            modifiedDeco = oldGeneratedDecorator(cls)
            modifiedDeco.decorator = newDecoratorFactory # keep track of decorator
            return modifiedDeco

        # when no parameters are given invoke with cls
        if len(args):
            return newGeneratedDecorator(args[0])

        return newGeneratedDecorator

    newDecoratorFactory.__name__ = foreignDecoratorFactory.__name__
    newDecoratorFactory.__doc__ = foreignDecoratorFactory.__doc__
    return newDecoratorFactory



# flow decorator
def flow(
  application="search",
  versionName="0.0.1",
  canonicalName=None,
  schedule=None
  ):
    def deco_flow(func):
        @functools.wraps(func)
        def wrapper_flow(*args, **kwargs):
            func.application = application
            func.versionName = versionName
            func.canonicalName = canonicalName
            func.schedule = schedule
            v = func(*args, **kwargs)
            logging.info(f"setting flow properties: - {v.versionName} - {v.application} for: {func.__name__}")

            return v

        return wrapper_flow
    return deco_flow


flow = RegisteringDecoratorFactory(flow)
