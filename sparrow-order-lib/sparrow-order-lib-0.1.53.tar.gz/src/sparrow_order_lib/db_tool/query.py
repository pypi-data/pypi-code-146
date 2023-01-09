from collections import namedtuple
from django.db import connection
import logging

logger = logging.getLogger(__name__)


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def query_data_by_sql(sql_str, params):
    db_return = []
    err_msg = ""
    try:
        with connection.cursor() as c:
            if not params:
                c.execute(sql_str)
            else:
                c.execute(sql_str, params)
            db_return = namedtuplefetchall(c.cursor)
    except BaseException as be:
        db_return = []
        err_msg = "查询失败,原因: {be_str}".format(be_str=str(be))
        logger.error(err_msg)
    return db_return, err_msg
