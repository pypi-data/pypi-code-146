import csv

from loguru import logger
from sqlalchemy import create_engine, text

from toolkits import utils


class engine(object):

    _engine = None

    def __init__(self, *args, **kwargs):
        ''' Initiation '''

        self._engine = create_engine(*args, **kwargs)

    def execute(self, sql=None, sql_file=None, csv_file=None):

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

                logger.success('database connected')

                try:

                    logger.success('execute sql')

                    _results = connect.execute(text(_sql))

                    if csv_file == None:

                        # 返回数据
                        logger.success('return results')
                        return _results

                    else:

                        # 导出数据
                        with open(csv_file, 'w', encoding='utf-8-sig') as _file:
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
