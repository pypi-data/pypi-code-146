#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database overlay for any client code parameters.

Primary members
---------------
auto_args_db

args_db_csv

Give me a search string and database,
and I'll magically create a Python style arguments-compatible
tuple and dictionary (args, kwargs).


Created on Mon Aug  6 09:51:54 2018

@author: chris
"""

import csv
import numpy as np
import functools
import logging

from . import kwargs_scan as kws

LOG = logging.getLogger(__name__)


def auto_args_db(func):
    """Decorator.
    Wrap any function with args_db_csv.

    Handles pass-through.

    E.g.

    @auto_args_db
    def myFunc(param1, param2, ...):
        ...
    or
    class myClass():
        database='filename.csv'
        @auto_args_db
        def __init__(self, param1, param2, ...):
            ...

    E.g.
    instance = myClass(search='name')
    instance = myClass(database='db', search='name')
    myFunc(database='db', search='name')

    Meanwhile your function is coded like:
        def myFunc(param1, param2, ...):
            ...
        or
        def __init__(param1, param2, ...):
            ...

    auto_args_db will only apply the database if search='' is given,
        and if database is defined.

    See test_auto_args_db(), which is pre-wrapped to test your usage.
    """
    @functools.wraps(func)
    def wrapper_init_w_args_db(*args, **kwargs):
        # I doubt the search activation switch can be 100% foolproof
        db = None
        if 'search' in kwargs:
            if 'database' in kwargs:
                # take database='' first if it's there
                db = kwargs['database']
                kwargs.pop('database')
            elif len(args) > 0 and hasattr(args[0], 'database'):
                # else if args[0] is an object and .database is there
                db = args[0].database
            # little detail; search='' will passthrough if database is undefined
        if db is None:
            # if we don't have both search and database, then
            # just passthrough and do nothing
            LOG.debug('passthrough %d args %d kwargs to %s wo database query',
                      len(args), len(kwargs), func.__name__)
            return func(*args, **kwargs)
        else:
            search = kwargs['search']
            kwargs.pop('search')
            dbargs, dbkwargs = args_db_csv(search, db)
            LOG.debug('db added %dargs %dkwargs onto passthrough %dargs %dkwargs for %s',
                      len(dbargs), len(dbkwargs), len(args), len(kwargs), func.__name__)
            args = args + dbargs
            kwargs = {**dbkwargs, **kwargs}
            return func(*args, **kwargs)
    return wrapper_init_w_args_db


def args_db_csv(search, database, verbose=0, by_inspection=False):
    """kwargs database lookup from CSV file.
    Returns args compatible dictionary.

    API::

        args, kwargs = args_db_csv(search, database)
            # where the kwargs and matrices are determined by the CSV format
            # -OR- MORE TO THE POINT:
        args, kwargs = args_db_csv(search, database)
        obj = SomeClass(*args, **kwargs)
            # where it's basically your job to ensure that CSV file format
            # satisfies the input parameters for SomeMaterialClass.__init__()
            # ... test_auto_args_db or this func to view what is returned
            # ... and cross-reference help(SomeClass.__init__)

    Examples::

        args, kwargs = kwargs_db_csv('quartz', 'sellmeier.csv')
        brf = Sellmeier(*args, **kwargs)
            # or
        brf = Sellmeier(search='quartz')
    """
    with open(database) as file:
        d_list = list(csv.reader(file))
        data = np.array(d_list)
        header = data[0, :]
        # print(data[1:,0])
        key_index = kws._find_in_list(search, data[1:, 0], force=True)
        for key_end in range(key_index + 2, len(d_list)):
            if data[key_end, 0] != '':
                break
        LOG.debug('Found key "%s" at %d in file "%s"',
                  search, key_index, database)
        head = (header[1:])
        dat = (data[key_index+1:key_end, 1:])
        args, kwargs = kws.arrays_2_args(head, dat)
        return args, kwargs


@auto_args_db
def test_auto_args_db(*args, **kwargs):
    """After you write a .csv file for args, test it here."""
    print('Test of auto_args_db wrapper.')
    print('Result for *args:')
    print(args)
    print('Results for **kwargs:')
    print(kwargs)
