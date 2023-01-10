import types
from html import escape


# http://192.168.0.8:18003/unit_test
def all_test():
    result_txt = ""
    result_txt += check_intercept()
    return result_txt


def check_intercept():
    import sys

    result = ""

    must_be = [
        ('jennifer.hooks.app_flask', check_flask),
        ('jennifer.hooks.db_sqlite3', None),
        # not installed ('jennifer.hooks.app_django', None),
        ('jennifer.hooks.db_mysqlclient', None),
        ('jennifer.hooks.db_pymysql', None),
        ('jennifer.hooks.external_requests', None),
        ('jennifer.hooks.external_urllib', None),
        ('jennifer.hooks.external_urllib2', None),
        ('jennifer.hooks.external_urllib3', None),
        ('jennifer.api.proxy', None),
        ('jennifer.hooks.db_pymongo', None),
        ('jennifer.hooks.db_redis', None),
        ('jennifer.hooks.db_cx_oracle', None),
        ('jennifer.hooks.db_psycopg2', check_psycopg2),
        ('jennifer.hooks.app_fastapi', None),
        ('jennifer.hooks.mod_asyncio', None),
        ('jennifer.hooks', None),
        ('jennifer.startup', None),
        ('jennifer', None),
    ]

    for module in must_be:
        if module[0] not in sys.modules.keys():
            result += "EXCEPTION: NO JENNIFER MODULE: " + module[0] + "<br />"
        else:
            target_module = __import__(module[0])
            result += "info: " + module[0] + " imported: " + target_module.__package__ + "<br />"

            func = module[1]
            if func is not None:
                result += module[1](target_module)

    for key in sys.modules.keys():
        # result += "info: " + key + ", " + "<br />"
        pass

    return result


def check_flask(module):
    import flask

    check_funcs = [
        (flask.Flask.wsgi_app, "_wrap_wsgi_handler.<locals>.handler"),
        (flask.Flask.dispatch_request, "wrap_dispatch_request.<locals>.handler"),
    ]

    result = ""
    for func_item in check_funcs:
        result += func_name_check(func_item[0], func_item[1]) + "<br />"

    return result


def check_psycopg2(module):
    import psycopg2

    check_funcs = [
        (psycopg2.connect, "register_database.<locals>._wrap_connect.<locals>.handler"),
        (psycopg2.extensions.register_type, "_wrap_register_type.<locals>.handler"),
        (psycopg2._psycopg.register_type, "_wrap_register_type.<locals>.handler"),
        (psycopg2._json.register_type, "_wrap_register_type.<locals>.handler"),
    ]

    result = ""
    for func_item in check_funcs:
        result += func_name_check(func_item[0], func_item[1]) + "<br />"

    return result


def func_name_check(func, func_name):
    import dis
    if func.__qualname__ == func_name:
        return "info: Intercepted: " + escape(func_name, "<")

    return "exception: NOT INTERCEPTED: " + escape(func_name, "<") + ", " + escape(func.__qualname__, "<")

