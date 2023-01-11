import logging
from duckdb import DuckDBPyConnection
from time import perf_counter
from typing import Union


class CURSOR:
    cur: DuckDBPyConnection
    time: float

    def __init__(self, cur: DuckDBPyConnection) -> None:
        self.time = perf_counter()
        self.cur = cur
        self.cur.begin()
        logging.warning("-----------------transaction start!-----------------")

    def __del__(self) -> None:
        try:
            self.cur.commit()
        except Exception as e:
            self.cur.rollback()
            logging.error(str(e))
        self.cur.close()
        logging.info(f"Total elapsed time: {perf_counter() - self.time:0.4f} sec")
        logging.warning("-----------------transaction stop!-----------------")

    def get(
        self,
        sql: str,
        args: Union[dict, tuple, None] = None,
        as_dict: bool = False,
        one: bool = False,
    ) -> Union[dict, list, tuple, None]:
        self.set(sql, args, True)
        if as_dict:
            desc = self.cur.description
            cols = tuple(map(lambda d: d[0], desc)) if isinstance(desc, tuple) else ()
        if one:
            row = self.cur.fetchone()
            if isinstance(row, tuple):
                return dict(zip(cols, row)) if as_dict else row
            return None
        else:
            rows = self.cur.fetchall()
            if rows and as_dict:
                return [dict(zip(cols, row)) for row in rows]
            return rows

    def set(self, sql: str, args: Union[dict, tuple, None] = None, get: bool = False) -> None:
        time = perf_counter()
        if get:
            # logging.debug(self.cur.query.decode())
            logging.debug(f"{sql}, {args}")
        else:
            logging.warning(f"{sql}, {args}")
        self.cur.execute(sql, args)
        logging.info(f"Query elapsed time: {perf_counter() - time:0.4f} sec")
