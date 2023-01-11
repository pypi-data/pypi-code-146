"""Install Greek aliases for common builtins.

In Unicode there are both modern Greek letters and mathematical symbols based
on the Greek letters. We support both wherever they are valid Python
identifiers.
"""
import math
import builtins

__version__ = '0.1.0'

builtins.Σ = Σ = sum
builtins.𝚺 = 𝚺 = sum
builtins.ℂ = ℂ = complex
builtins.ℤ = ℤ = int

math.π = π = math.pi
math.𝜋 = 𝜋 = math.pi
math.𝑒 = 𝑒 = math.e

try:
    # Support identifiers that were added through the 3 series
    #
    # This must be in ascending order of Python version as we bail on the first
    # one that isn't present.

    # Python 3.2
    math.Γ = Γ = math.gamma

    # Python 3.6
    math.τ = τ = math.tau
    math.𝜏 = 𝜏 = math.tau

    # Python 3.8
    math.Π = Π = math.prod
    # This mathematical operator is not a valid identifier
    # math.∏ = ∏ = math.prod
except AttributeError:
    pass

try:
    import statistics
except ModuleNotFoundError:
    pass
else:
    statistics.σ = σ = statistics.stdev
    statistics.𝜎 = 𝜎 = statistics.stdev
    del statistics


del math
del builtins
