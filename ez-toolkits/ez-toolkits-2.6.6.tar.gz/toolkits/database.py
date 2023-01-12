import csv

from loguru import logger
from sqlalchemy import create_engine, text

from toolkits import utils


class Engine(object):

    _engine = None

    def __init__(self, *args, **kwargs):
        ''' Initiation '''
        self._engine = create_engine(*args, **kwargs)

    def connect_test(self):
        try:
            self._engine.connect()
            return True
        except:
            return False

    def initializer(self):
        """ensure the parent proc's database connections are not touched in the new connection pool"""
        self._engine.dispose(close=False)

    def execute(self, sql=None, sql_file=None, csv_file=None, echo=None):

        _sql = None

        # 提取 SQL
        if sql != None and sql != '':

            _sql = sql

        elif sql_file != None and sql_file != '':

            if not utils.stat(sql_file, 'file'):
                logger.error(f'No such file: {sql_file}')
                return False

            with open(sql_file, 'r') as _file:
                _sql = _file.read()

        else:

            logger.error('SQL or SQL File is None')
            return False

        # ------------------------------------------------------------

        try:

            # 执行 SQL
            with self._engine.connect() as connect:

                if echo == True:
                    logger.success('database connected')

                try:

                    if echo == True:
                        logger.success('execute sql')

                    _results = connect.execute(text(_sql))

                    if csv_file == None:

                        # 返回数据
                        if echo == True:
                            logger.success('return results')
                        return _results

                    else:

                        # 导出数据
                        with open(csv_file, 'w', encoding='utf-8-sig') as _file:
                            if echo == True:
                                logger.success(f'writer results to {csv_file}')
                            outcsv = csv.writer(_file)
                            outcsv.writerow(_results.keys())
                            outcsv.writerows(_results)
                            return True

                except Exception as e:
                    logger.error(e)
                    return False

        except Exception as e:
            logger.error(e)
            return False

    def insert_one(self, table=None, field=None, data=None):
        try:
            logger.info('数据追加 ...')
            with self._engine.connect() as connection:
                if table == None:
                    logger.error('table error')
                    return False
                if field == None:
                    logger.error('field error')
                    return False
                if data == None:
                    logger.error('data error')
                    return False
                connection.execute(f"""INSERT INTO {table} ({field}) VALUES ({data})""")
                logger.success(f'数据追加成功')
                return True
        except Exception as e:
            logger.error(e)
            return False
