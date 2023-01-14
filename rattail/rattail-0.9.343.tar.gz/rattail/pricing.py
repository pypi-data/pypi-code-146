# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Pricing Utilities
"""

from __future__ import unicode_literals, absolute_import

import decimal
import warnings


def gross_margin(price, cost, percentage=False):
    """
    Calculate and return a gross margin percentage based on ``price`` and
    ``cost``.

    Please note, that for historical reasons, the default behavior is to return
    the margin as a decimal value from 0.0 through 100.0 (or beyond, perhaps).

    However the "industry standard" seems to be to use a decimal value between
    0.000 and 1.000 instead.  Specify ``percentage=True`` for this behavior.

    If ``price`` is empty (or zero), returns ``None``.

    If ``cost`` is empty (or zero), returns ``100`` (or ``1`` if
    ``percentage=True``).
    """
    if not price:
        return None

    if not cost:
        if percentage:
            return 1
        return 100

    margin = (price - cost) / price
    if percentage:
        return margin
    return 100 * margin


def calculate_markup_from_margin(margin, from_decimal=False):
    """
    Calculate the "markup" value corresponding to the given margin.

    This assumes the ``margin`` value is user-friendly, e.g. ``37.5``
    instead of ``0.375`` to represent 37.5%, unless ``from_decimal``
    is true in which case the decimal format is assumed.

    :param margin: Profit margin percentage.

    :param from_decimal: If false (the default), then ``margin``
       should (normally) be between 0 - 100.  But if true, then
       ``margin`` is assumed to be between 0.0 and 1.0 instead.

    :returns: Equivalent cost markup as decimal value (e.g. 1.4).
    """
    if margin is None:
        return
    if margin == 0:
        return 1

    if from_decimal:
        margin *= 100

    return 100 / (100 - margin)


def calculate_markup_from_margin_decimal(margin):
    warnings.warn("calculate_markup_from_margin_decimal() is deprecated; "
                  "please use calculate_markup_from_margin() instead",
                  DeprecationWarning, stacklevel=2)
    return calculate_markup_from_margin(margin, from_decimal=True)


def calculate_markup(margin):
    warnings.warn("calculate_markup() is deprecated; please use "
                  "calculate_markup_from_margin() instead",
                  DeprecationWarning, stacklevel=2)
    return calculate_markup_from_margin(margin, from_decimal=True)


def calculate_variance(oldvalue, newvalue):
    """
    Calculate and return a simple variance percentage, between the
    given old and new values.  For instance::

       calculate_variance(4.00, 6.00)
       # returns 50.0 (50% increase in value)

       calculate_variance(4.00, 3.00)
       # returns -25.0 (25% decrease in value)
    """
    if oldvalue is None or newvalue is None:
        return
    diff = (newvalue or 0) - (oldvalue or 0)
    if not diff:
        return 0
    if not oldvalue:
        return 100
    return diff / oldvalue * 100


def calculate_price_from_margin(cost, margin, places=2):
    """
    Calculate a basic retail price from the given cost amount and
    ideal margin.

    :param cost: Cost amount as decimal.

    :param margin: Ideal / target margin percentage, expressed as
       e.g. 39.0 and *not* 0.39.

    :returns: Price amount as decimal.
    """
    if cost is None or margin is None:
        return

    retail = cost * 100 / (100 - margin)

    # only modify value if caller did *not* specify places=None
    if places is not None:
        if places == 0:
            return int(retail)
        fmt = '{{:0.{}f}}'.format(places)
        return decimal.Decimal(fmt.format(retail))

    return retail
