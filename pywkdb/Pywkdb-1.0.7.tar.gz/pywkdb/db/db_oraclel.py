#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pywkdb.utils.db_base import DbBase
from pywkdb.utils.url_parse import UrlParse
logger = logging.getLogger('OracleDb')


class OracleDb(DbBase):

    def __init__(self, url, with_tran=False):
        """
        构造函数,初始化数据库连接
        :param url: example oracle://user:passwd@127.0.0.1:1521/orcl
                oracle://user:passwd@127.0.0.1:1521/orcl?NLS_LANG=SIMPLIFIED CHINESE_CHINA.UTF8
        :param with_tran:
        """
        super(OracleDb, self).__init__(url, with_tran)

    def connect(self, url_parse=None):
        """
        生成连接串
        :return:
        """
        if url_parse is None:
            url_parse = UrlParse(self._url)

        import cx_Oracle
        import os
        if len(url_parse.query) > 0:
            for query in url_parse.query:
                os.environ[query] = url_parse.query[query]
        return self._cxoracle().connect(
            url_parse.username,
            url_parse.password,
            cx_Oracle.makedsn(url_parse.hostname, url_parse.port, url_parse.path)
        )


if __name__ == '__main__':
    pass
