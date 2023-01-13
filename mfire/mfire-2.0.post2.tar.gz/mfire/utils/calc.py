"""Utilitaires divers pour les calculs"""


def round_to_closest_multiple(number, m):
    """Return the multiple of m closest to number"""
    return m * round(number / m)


def round_to_next_multiple(number, m):
    """Return the ceiling multiple of m from number"""
    return m * (number // m + int(bool(number % m)))
