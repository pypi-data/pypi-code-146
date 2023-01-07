"""
aznt - From A to Z Number Theory
Author: Adrian Zapała, MSc, adrian.zapala@outlook.com, All rights reserved
Licence: MIT
"""

import random
from sys import set_int_max_str_digits, get_int_max_str_digits
from math import log, log2, e, pi, sin, gamma
from mpmath import li
from decimal import Decimal, getcontext

set_int_max_str_digits(500_000)
max_digits = get_int_max_str_digits()


def factorization(n):
    """Shows the prime factors of a number"""
    factors = []
    i = 2
    while True:
        if n % i == 0:
            factors += [i]
            div = n / i
            n = div
            if div == 1:
                break
        else:
            i += 1

    return factors


def dividers_naive(n):
    """Shows all factors of a number - slow implementation"""
    dividers = []
    for i in range(1, n + 1):
        if n % i == 0:
            dividers += [i]

    return dividers


def dividers_opt(n, pairs=False):
    """Shows all factors of a number - fast implementation"""
    dividers = []
    t = [0, 0]
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            j = n // i
            if i != j:
                if pairs:
                    t[0], t[1] = i, j
                else:
                    dividers += [i]
            elif pairs:
                t[0], t[1] = i, j
            if pairs:
                dividers.append((t[0], t[1]))
            else:
                dividers += [j]

    if not pairs:  # If pairs param is equal to False
        dividers.sort()

    return dividers


def tau(n):
    """Returns the number of divisors of an integer (including 1 and the number itself)"""

    return len(dividers_opt(n))


def sigma(n):
    """Returns the sum of divisors of an integer (including 1 and the number itself)"""

    return sum(dividers_opt(n))


def s(n):
    """Returns the sum of proper divisors of an integer (excluding n itself)"""

    return sigma(n) - n


def gcd_mod(a, b):
    """Returns Greatest Common Divisor (GCD) of two positive integers
    using Euclidean algorithm with division"""

    while b:
        last_non_zero_remainder = b
        mod = a % b
        a = b
        b = mod

    return last_non_zero_remainder


def gcd_subtract(a, b):
    """Returns Greatest Common Divisor (GCD) of two positive integers
    using Euclidean algorithm with subtraction"""

    if a == b:
        return a
    while True:
        if a < b:
            c = b - a
        else:
            c = a - b

        if b < c:
            a = c
        else:
            a = b
            b = c

        if c:
            last_non_zero_remainder = c
        else:
            break

    return last_non_zero_remainder


def lcm(a, b):
    """Returns Lowest Common Multiple (LCM) of two positive integers"""

    return a * b // gcd_mod(a, b)


def is_gcd_eq_1(n, floor, ceil):
    """Returns a quantity of pairs of numbers which are relatively prime to themselves,
    with a density of them and a list of nested lists of them"""

    c = 0
    lst_pairs = []
    # Get n cases
    for i in range(0, n):
        r1 = random.randint(floor, ceil)
        r2 = random.randint(floor, ceil)
        if gcd_mod(r1, r2) == 1:
            lst_pairs.append([r1, r2])
            c += 1
    return c, c / n, lst_pairs


def totient(n):
    """Returns Euler's totient function"""

    counter = 1

    for k in range(2, n):
        if gcd_mod(n, k) == 1:
            counter += 1

    return counter


def pnt(n):
    """Returns the asymptotic distribution of the prime numbers
    among the positive integers"""

    return n / log(n, e)


def prime_probability(n):
    """Returns probability if a random number
    is prime to a specific ceil given"""
    return 1 / log(n, e)


def basel_problem(max, n=2):
    """Returns precise summation of the reciprocals of the squares
    of the natural numbers, i.e. the precise sum of the infinite series"""

    s = 0
    for i in range(1, max + 1):
        s += 1 / i ** n
    return s


def is_mersenne(m):
    """Check if a number is Mersenne number"""
    if m < 1:
        return f"Argument: {m}. Mersenne numbers starts from 1."
    n = int(log2(m + 1))

    if m == 2 ** n - 1:
        return True, "M" + str(n), f"{m:{len(str(m))}.2e}".strip(), m

    return False


def is_fermat(f):
    """Check if a number is Fermat number"""
    if f < 3:
        return f"Argument: {f}. Fermat numbers starts from 3."
    lg = int(log2(f - 1))
    n = int(log2(lg))

    if f == 2 ** 2 ** n + 1:
        try:
            return True, "F" + str(n), f"{Decimal(f):{len(str(f))}.2e}".strip(), f
        except ValueError:
            return f"Number too large"

    return False


def is_perfect(n):
    """Returns True if n is a perfect number"""
    if n > 0 and sum(dividers_opt(n)[:-1]) == n:
        return True

    return False


def zeta_trivial_value(s, n=10000):
    """Return value of Riemann zeta function for given argument"""
    s_greater_than_1 = False
    if s == 0:
        return .5
    if s == 1:
        return float("inf")
    if s < 0 and s % 2 == 0:
        return 0
    if s > 1:
        s_greater_than_1 = True
    if s < 1:
        s = 1 - s
    eta_s = 0
    for i in range(1, n + 1):
        if i % 2 == 0:
            eta_s -= 1 / i ** s
        else:
            eta_s += 1 / i ** s

    zeta_s = eta_s / (1 - 1 / 2 ** (s - 1))
    if s_greater_than_1:
        return zeta_s
    zeta_s = 2 ** (1 - s) * pi ** (-1 * s) * sin(pi * (1 - s) / 2) * gamma(s) * zeta_s

    return zeta_s


def nontrivial_zeros_dist(t):
    """Returns average distance between zeros
    on a critical line in Riemann zeta function"""
    return 2 * pi / log(t / (2 * pi), e)


def xs(data_rows):
    return [10 ** i for i in range(1, data_rows + 1)]


pi_x = [4, 25, 168, 1229, 9592, 78498, 664579, 5761455, 50847534, 455052511,
        4118054813, 37607912018, 346065536839, 3204941750802, 29844570422669,
        279238341033925, 2623557157654233, 24739954287740860, 234057667276344607,
        2220819602560918840, 21127269486018731928, 201467286689315906290,
        1925320391606803968923, 18435599767349200867866, 176846309399143769411680,
        1699246750872437141327603, 16352460426841680446427399, 157589269275973410412739598,
        1520698109714272166094258063]


def pnt1(data_rows):
    return list(map(pnt, xs(data_rows)))


def pstats1(data_rows=29):
    """Returns statistics of prime numbers up to 10e29"""
    if data_rows <= 0 or data_rows > 29:
        print("Incorrect argument")
        return None

    _xs = xs(data_rows)

    x_pi_x = [_xs[i] / pi_x[i] for i in range(data_rows)]
    log_x = list(map(log, _xs))
    approx_error = [(abs(x_pi_x[i] - log_x[i])) / x_pi_x[i] * 100 for i in range(data_rows)]
    headers = ["x", "\u03C0(x)", "x/\u03C0(x)", "logx", "(x/\u03C0(x) - logx) / x/\u03C0(x) [%]"]

    print(f"{headers[0]:^10}{headers[1]:^30}{headers[2]:^25}{headers[3]:^25}{headers[4]:^30}")
    for i in range(data_rows):
        print(f"{_xs[i]:<10.0e}{pi_x[i]:<30}{x_pi_x[i]:<25}{log_x[i]:<25}{approx_error[i]:<30}")


def pnt2(data_rows):
    return list(map(li, xs(data_rows)))


def pstats2(data_rows=29):
    """Returns correlation between Li(x), Pi(x) and x/logx"""
    if data_rows <= 0 or data_rows > 29:
        print("Incorrect argument")
        return None

    _xs = xs(data_rows)
    _pnt1 = pnt1(data_rows)
    _pnt2 = pnt2(data_rows)
    headers = ["x", "PNT: Li(x)", "\u03C0(x)", "PNT: x/logx"]

    print(f"{headers[0]:^10}{headers[1]:^30}{headers[2]:^30}{headers[3]:^25}")
    for i in range(data_rows):
        print(f"{_xs[i]:<10.0e}{float(_pnt2[i]):<30}{pi_x[i]:<30}{_pnt1[i]:<25}")


def pstats3(data_rows=29):
    """Returns statistics of Li(x) - Pi(x) prime numbers rests up to 10e29"""
    if data_rows <= 0 or data_rows > 29:
        print("Incorrect argument")
        return None

    _xs = xs(data_rows)
    _pnt2 = pnt2(data_rows)

    approx_error_absolute = [float(_pnt2[i]) - pi_x[i] for i in range(data_rows)]
    approx_error_relative = [approx_error_absolute[i] / pi_x[i] * 100 for i in range(data_rows)]
    headers = ["x", "\u03C0(x)", "PNT: Li(x)", "Li(x) - \u03C0(x)", "(Li(x) - \u03C0(x)) / \u03C0(x) [%]"]

    print(f"{headers[0]:^10}{headers[1]:^30}{headers[2]:^30}{headers[3]:^25}{headers[4]:^30}")
    for i in range(data_rows):
        print(f"{_xs[i]:<10.0e}{pi_x[i]:<30}{float(_pnt2[i]):<30}{approx_error_absolute[i]:<25f}{approx_error_relative[i]:<30f}")
