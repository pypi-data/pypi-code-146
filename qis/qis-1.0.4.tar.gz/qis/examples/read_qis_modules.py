import qis.plots.derived.prices
this = dir(qis.plots.derived.prices)
print(this)
for x in this:
    if not any(y in x for y in ['__', 'Dict']):
        print(f"{x},")


print('##############################')
import inspect

all_functions = inspect.getmembers(qis.plots.derived.prices, inspect.isfunction)
for x in all_functions:
    if not any(y in x for y in ['run_unit_test', 'njit', 'NamedTuple', 'dataclass', 'skew', 'kurtosis', 'abstractmethod']):
        print(f"{x[0]},")