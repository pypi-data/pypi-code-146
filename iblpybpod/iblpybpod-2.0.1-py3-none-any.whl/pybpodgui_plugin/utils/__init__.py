# !/usr/bin/python3
# -*- coding: utf-8 -*-


def make_lambda_func(func, **kwargs):
    return lambda: func(**kwargs)


def do_nothing():
    pass
