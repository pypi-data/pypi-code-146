class AdaptiveParameterWrapper:
    """Utility class to change hyperparameter using function call count.

        >>> from deap_misl.tools import AdaptiveParameterWrapper
        >>> def arg_logic(count): return 10 / count
        >>> def func(param, hyperparam): return param, hyperparam
        >>> adaptive_func = AdaptiveParameterWrapper(func, 'hyperparam', arg_logic)
        >>> adaptive_func(10)
        (10, 10.0)
        >>> adaptive_func(10)
        (10, 5.0)
        >>> adaptive_func(10)
        (10, 3.3333333333333335)
    """

    def __init__(self, func, arg_name, arg_logic):
        """
        :param func: An operator function that you want to be adaptive.
        :param arg_name: An argument name that you want to be adaptive.
        :param arg_logic: A function to determine argument value.
        """
        self.func = func
        self.arg_name = arg_name
        self.arg_logic = arg_logic
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        kwargs[self.arg_name] = self.arg_logic(self.call_count)
        return self.func(*args, **kwargs)
