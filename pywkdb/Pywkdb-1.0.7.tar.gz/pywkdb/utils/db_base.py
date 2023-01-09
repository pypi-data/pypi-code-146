#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pandas as pd
from .url_parse import UrlParse

logger = logging.getLogger('DbBase')


class DbBase(object):
    
    def __init__(self, url, with_tran=False):
        self._url = url
        self._with_tran = with_tran
        self._conn = None
        if self._with_tran:
            self._conn = self.connect()
    
    def _get_conn(self):
        if not self._with_tran:
            return self.connect()
        else:
            return self._conn

    def _close(self):
        DbBase.close(self._conn)

    def __del__(self):
        self._close()
    @staticmethod
    def _execute(conn, sql: str, params=None):
        """
        内部方法，执行sql代码
        :param sql:     sql代码
        :param params:  传递参数
        :return:        游标值Cursor
        """
        cur = conn.cursor()
        logger.info(sql)
        logger.info(params)
        if params is None:
            cur.execute(sql)
        else:
            cur.execute(sql, params)
        return cur
    
    def update(self, sql: str, params=None):
        """
        更新数据库
        :param sql:     sql代码
        :param params:  传递参数
        :return:        操作影响记录数
        """
        cur = None
        conn = None
        try:
            conn = self._get_conn()
            cur = self._execute(conn, sql, params)
            conn.commit()
            return cur.rowcount
        except Exception as e:
            logger.error("update_error:{}".format(e))
        finally:
            self.close(cur)
            if not self._with_tran:
                self.close(conn)
    
    def fetchmany(self, fetch_number, sql: str, params=None):
        """
        获取指定数据量，根据游标向下获取
        :param fetch_number:    数据条数
        :param sql:             sql代码
        :param params:          传递参数
        :return:                记录集
        """
        cur = None
        conn = None
        try:
            conn = self._get_conn()
            cur = self._execute(conn, sql, params)
            return cur.fetchmany(fetch_number)
        except Exception as e:
            logger.error("fetchmany_error:{}".format(e))
        finally:
            self.close(cur)
            if not self._with_tran:
                self.close(conn)
    
    def select(self, sql: str, params=None) -> (tuple, list):
        """
        用来查询表数据
        :return: 返回数据和表头
        """
        cur = None
        conn = None
        try:
            conn = self._get_conn()
            cur = self._execute(conn, sql, params)
            col = cur.description
            results = cur.fetchall()
            # 执行结果转化为dataframe
            headers = []
            for i in range(len(col)):
                headers.append(col[i][0])
            return results, headers
        except Exception as e:
            logger.error("fetchmany_error:{}".format(e))
        finally:
            self.close(cur)
            if not self._with_tran:
                self.close(conn)
    
    def select_frame_data(self, sql: str, params=None) -> pd.DataFrame:
        """
        查询结果返回DataFrame格式。
        example
        df = self.select_frame_data()
        for index, row in df.iterrows():
            print(index,row)
        :return: 返回DataRame格式数据
        """
        result, headers = self.select(sql, params)
        return pd.DataFrame(list(result), columns=headers)
    
    def select_data(self, sql: str, params=None) -> list:
        """
        查询结果返回List
        :param sql:
        :param params:
        :return:
        """
        results, headers = self.select(sql, params)
        items = []
        for result in results:
            item = {}
            i = 0
            for header in headers:
                item[header] = result[i]
                i += 1
            items.append(item)
        return items
    
    @staticmethod
    def close(conn):
        """
        关闭游标或数据库
        :param conn: 游标或数据库链接
        """
        if conn is not None:
            try:
                conn.close()
                del conn
            except Exception as e:
                logger.error("close:{}".format(e))
    
    def __del__(self):
        """
        删除对象时，自动释放数据库连接
        :return:
        """
        logger.debug('del sqldb')
        if self._conn is not None:
            try:
                self.close(self._conn)
            except Exception as e:
                logger.error("__del__:{}".format(e))
    
    def insert(self, sql: str, params=None):
        """
        插入一条记录
        :param sql:     sql代码
        :param params:  传递参数
        :return:        主键ID
        """
        cur = None
        conn = None
        try:
            conn = self._get_conn()
            cur = self._execute(conn, sql, params)
            try:
                insert_id = conn.insert_id()
            except:
                try:
                    insert_id = cur.lastrowid
                except:
                    print('无法获取id')
            conn.commit()
            return insert_id
        except Exception as e:
            conn.rollback()
            logger.error(e)
            return -1
        finally:
            self.close(cur)
            if not self._with_tran:
                self.close(conn)
    
    def connect(self, url_parse=None):
        """
        生成连接串
        :return:
        """
        raise RuntimeError('找不到对应的数据配置,目前支持mysql、mssql、sqlite 和 oracle')

    @staticmethod
    def _pymysql():
        try:
            import pymysql
            return pymysql
        except ImportError:
            raise RuntimeError('PyMySQL不存在，pip install PyMySQL')
    
    @staticmethod
    def _pymssql():
        try:
            import pymssql
            return pymssql
        except ImportError:
            raise RuntimeError('pymssql不存在，pip install pymssql')

    @staticmethod
    def _cxoracle():
        try:
            import cx_Oracle
            return cx_Oracle
        except ImportError:
            raise RuntimeError('cx_Oracle不存在，pip install cx_Oracle')

    @staticmethod
    def _sqlite3():
        try:
            import sqlite3
            return sqlite3
        except ImportError:
            raise RuntimeError('SqliteDb不存在')