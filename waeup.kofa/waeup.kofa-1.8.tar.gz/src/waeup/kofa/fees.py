## $Id: fees.py 12110 2014-12-02 06:43:10Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Components for fee management.

Fees here are considered as a pair <PARAMS, VALUES> with both being a
nested tuple. This is a way to describe a table with nested columns
and its values.

For example let's have a look at the following table:

  +------+------------------+----------------------+
  |      | locals           | non-locals           |
  +------+--------+---------+------------+---------+
  |      | art    | science | art        | science |
  +------+--------+---------+------------+---------+
  |fac1  |    1.1 |     1.2 |        1.3 |     1.4 |
  +------+--------+---------+------------+---------+
  |fac2  |    2.1 |     2.2 |        2.3 |     2.4 |
  +------+--------+---------+------------+---------+

This table contains parameters (all the headings) and numbers. The
numbers are our VALUES while the headings are our PARAMS.

Now the parameters are organized in a specific way: each value
represents exactly one heading out of the following sets: {fac1,
fac2}, {locals, non-locals}, {art, science}.

The value 1.2, for instance, stands for 'fac1' and 'locals' and
'science' (and it is the only value for this combination of
parameters).

We can therefore write the set of parameters as a tuple of tuples like
this::

  (('locals', 'non-locals'), ('art', 'science'), ('fac1', 'fac2'))

This way we define how parameters must be used with an instance of the
:class:`FeeTable` class below and its methods. Please note that order
of elements matters in tuples!

We can set whatever headers we like and the order is not important,
until we want to set/get the single values.

The values then must be set accordingly. If the above tuple defines
the parameters, then the following nested tuple represents respective
values that can be assigned to a fixed set of parameters::

  (
   ((1.1, 2.1),   # locals, art, fac1/fac2
    (1.2, 2.2)),  # locals, science, fac1/fac2
   ((1.3, 2.3),   # non-locals, art, fac1/fac2
    (1.4, 2.4)),  # non-locals, science, fac1/fac2
  )

This is complicated. Let's have a closer look. If we have N param
tuples, then the values must be delivered with a nesting level of N as
well:

  params := (A, B, C)  ->  N=3 -> (((...)))  [tuples with N levels]

Each inner tuple must contain as much elements as the last param. So,
if C contains three headings, then all inner tuples must be triples:

  params := (A, B, C), C:= ('f1', 'f2', 'f3') -> (((v1, v2, v3), ...))

For practical purposes you can imagine the above values as a table as
well:

  +-----------+---------+-------+--------+
  |           |         |  fac1 |   fac2 |
  +-----------+---------+-------+--------+
  |locals     | art     |   1.1 |    2.1 |
  |           | science |   1.2 |    2.2 |
  |non-locals | art     |   1.3 |    2.3 |
  |           | science |   1.4 |    2.4 |
  +-----------+---------+-------+--------+

Now, if you look closely and read the table from left to right
column-wise and from top to bottom, you will notice that the order of
appearances of headings is exactly like in the `params` tuple defined
above:

  ('locals', 'non-locals'), ('art', 'science'), ('fac1', 'fac2')

The only condition is, that column headings are not nested. If they
are, but row headings are not, then simply 'turn' the table by 90
degrees and you have a table that can be used as a pattern for input.

This should help to create fee tables out of tuples.

We'll try to provide more convenient input methods in future.

"""
import grok
import itertools
from zope import schema
from zope.interface import Interface, implementer, Attribute
from waeup.kofa.utils.helpers import product

class IFees(Interface):
    """A utility storing fee tables for different academic sessions.
    """
    tables = Attribute("""A dict of fee tables with session as key.""")

class IFeeTable(Interface):

    values = Attribute("""Nested tuples containing cell values.""")
    params = Attribute("""Parameter names required to get"""
                            """or set the fee table values.""")

    def as_table():
        """Return fees as a tuple of tuples (of tuples).
        """

    def as_dict():
        """Return fees as dict.
        """

    def import_values(params, values):
        """Set fees with parameter names and value dictionary.
        """

    def set_fee(params_tuple, value):
        """Set a single entry in fee table.
        """

    def get_fee(params_tuple):
        """Get single value in fee table denoted by `params_tuple`.
        """

def nested_list(nested_tuple):
    """Turn nested tuples in nested lists: ((A,B),(C,)) -> [[A,B],[C,]]
    """
    if isinstance(nested_tuple, tuple):
        return [nested_list(x) for x in nested_tuple]
    return nested_tuple

def nested_tuple(nested_list):
    """Turn nested lists in nested tuples: [[A,B],[C,]] -> ((A,B),(C,))
    """
    if isinstance(nested_list, list):
        return tuple([nested_tuple(x) for x in nested_list])
    return nested_list

@implementer(IFeeTable)
class FeeTable(grok.Model):

    params = ()
    values = ()

    def __init__(self, params=(), values=None):
        if params and values is not None:
            self.import_values(params=params, values=values)
        return

    def as_table(self, row_index=None):
        pass

    def as_dict(self):
        """Get all fees as dict with param tuples as keys.

        Example:

          {
            ('locals', 'art'): 1,
            ('locals', 'science'): 2,
            ('non-locals', 'art'): 3,
            ('non-locals', 'science'): 4,
          }
        """
        result = dict()
        combinations = list(itertools.product(*self.params))
        for item in combinations:
            result[item] = self.get_fee(item)
        return result

    def import_values(self, params=(), values=()):
        if params and values:
            self._check(params, values)
        self.values = values
        self.params = params
        return

    def set_fee(self, params_tuple, value):
        """Set a single entry in fee table.

        The `params_tuple` is described more thoroughly in
        :meth:`get_fee()`.
        """
        values_list = nested_list(self.values)
        sublist = values_list
        for num, param in enumerate(params_tuple):
            col_name_tuple = self.params[num]
            if param not in col_name_tuple:
                raise KeyError("%s not in %s" % (param, col_name_tuple))
            if num == len(self.params) - 1:
                sublist[col_name_tuple.index(param)] = value
            else:
                sublist = sublist[col_name_tuple.index(param)]
        self.values = nested_tuple(values_list)
        pass

    def get_fee(self, params_tuple):
        """Get value in fee table denoted by `param_tuple`.

        The `params_tuple` must contain exactly one value for each
        tuple in instance `params`. For instance, if we have instance
        tuples (row and col names)

          (('locals', 'non-locals'), ('art', 'science')),

        then `params_tuple` must be a 2-length tuple with
        exactly one of `locals`/`non-locals` and exactly one of
        `art`/`science` in exactly that order (locals/non-locals
        before art/science).
        """
        result = self.values
        for num, param in enumerate(params_tuple):
            col_name_tuple = self.params[num]
            if param not in col_name_tuple:
                raise KeyError("%s not in %s" % (param, col_name_tuple))
            result = result[col_name_tuple.index(param)]
        return result

    def _check(self, params, values):
        # XXX: something useful here, please
        return

DEFAULT_FEE_TABLE = FeeTable(
    params = (('locals', 'non-locals'), ('art', 'science'),
              ('fac1', 'fac2')),
    values = (((1.1, 2.1), (1.2, 2.2)), ((1.3, 2.3), (1.4, 2.4)))
    )


@implementer(IFees)
class Fees(grok.GlobalUtility):

    grok.name('default')

    def __init__(self):
        self.tables = {
            '2012': DEFAULT_FEE_TABLE,
            }
