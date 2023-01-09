from __future__ import annotations

from collections.abc import Iterable
from typing import Union, AnyStr

import influxdb_datalogger

from .functions import QueryFunction
from .compiler import Compiler
from .tag import Tag


class Select:
    """
    Class to build a select-clause for an InfluxDB query.
    """

    @staticmethod
    def build(*fields: Union[influxdb_datalogger.Field, str], query_function: QueryFunction = None):
        with Compiler() as c:
            c.SELECT()
            c.field(*fields, query_function=query_function)
        return c.compile()


class Delete:
    """
    Class to build a delete-clause for an InfluxDB query.
    """

    @staticmethod
    def build():
        with Compiler() as c:
            c.DELETE()
        return c.compile()


class From:
    """
    Class to build a FROM-clause for an InfluxDB query.
    """

    @staticmethod
    def build(*measurements: Union[influxdb_datalogger.Measurement, AnyStr]):
        with Compiler() as c:
            c.FROM()
            c.measurement(*measurements)
        return c.compile()


class Where:
    """
    Class to build a WHERE-clause for an InfluxDB query.
    """

    @staticmethod
    def build(*tags: Tag):
        """
        A very simple and basic way to build a WHERE-clause for InfluxDB query.

        Args:
            tags: An iterable of tags to combine into a WHERE-clause.

        Returns:

        """
        with Compiler() as c:
            c.WHERE()
            c.components.append(Where.join(tags, operator="AND"))
        return c.compile()

    @staticmethod
    def join(tags: Union[Iterable[Tag], Tag], operator: str):
        """
        Joins a set of Tag-objects together with 'AND' between them and returns a string.

        Args:
            tags: A set of Tag-objects.
            operator: An operator to join the tags with. Must be either 'AND' or 'OR'.

        Returns:
            A string where Tag-objects are joined together with 'AND' or 'OR',
             depending on what the argument 'operator' is.
        """
        if not tags:
            return None

        assert isinstance(tags, (set, list, tuple)), f"tags must be a {set}, {list} or {tuple}. {type(tags)} is not permitted."
        assert operator == "AND" or operator == "OR", f"operator = {operator} is not permitted. Must be 'AND' or 'OR'."
        operator = f" {operator} "
        # Do WHERE-clause
        for tag in tags:
            assert isinstance(tag, Tag), f"tags must be a set of Tag-objects. {type(tag)} is not permitted."
        return f"{operator.join(tags)}"


class Group:
    """
    Class to build a GROUP-clause for an InfluxDB query.
    """

    @staticmethod
    def build(*groups: Union[influxdb_datalogger.Tag, str]):

        if not groups:
            return
        with Compiler() as c:
            c.GROUP_BY()
            c.group(*groups)
        return c.compile()


class Limit:
    """
    Class to build a LIMIT-clause for an InfluxDB query.
    """

    @staticmethod
    def build(limit):
        if not limit:
            return
        with Compiler() as c:
            c.LIMIT(limit)
        return c.compile()
