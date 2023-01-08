import logging
import sqlite3
import sqlite3 as sql
import numpy as np
from enum import IntEnum
import importlib
import os
import multiprocessing
from ..indicator_data import OHLCV_day
from ..constants import TIME_TYPE, PRICE_TYPE, VOLUME_TYPE


class CompressionType(IntEnum):
    no = 0
    gzip = 1
    bz2 = 2
    lz4 = 3

    @staticmethod
    def cast(str_type):
        return getattr(__class__, str_type)


class Sqlite3Cache:

    def __init__(self, config):

        self.database_file = config['quotation_database']
        self.compression_type = CompressionType.cast(config['compression_type'])
        self.compression_modules = dict()

        database_folder = os.path.split(self.database_file)[0]
        if not os.path.isdir(database_folder):
            os.makedirs(database_folder)

        self.sl3base = sql.connect(self.database_file, isolation_level=None)

        cursor = self.sl3base.cursor()
        check_bars_table = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quotes'")

        if check_bars_table.fetchone() is None:
            self.init_database()

    def day_to_int(self, day_date):
        return int(day_date.astype('datetime64[D]').astype(np.int64))

    def day_from_int(self, day_int):
        return np.datetime64(day_int, 'D')

    def get_compression_module(self, compression_type):

        compression_module = self.compression_modules.get(compression_type)
        if compression_module is not None:
            return compression_module

        if compression_type == CompressionType.gzip:
            return importlib.import_module('zlib')
        elif compression_type == CompressionType.bz2:
            return importlib.import_module('bz2')
        elif compression_type == CompressionType.lz4:
            return importlib.import_module('lz4')
        else:
            raise NotImplementedError(f'Unknown compression type: {compression_type}')

    def compress_numpy(self, array, compression_type):

        if compression_type == CompressionType.no:
            return array.tobytes()

        compression_module = self.get_compression_module(compression_type)
        return compression_module.compress(array.tobytes())

    def decompress_numpy(self, array_compressed_bytes, dtype, compression_type):

        if compression_type == CompressionType.no:
            array_bytes = array_compressed_bytes
        else:
            compression_module = self.get_compression_module(compression_type)
            array_bytes = compression_module.decompress(array_compressed_bytes)

        return np.frombuffer(array_bytes, dtype=dtype)

    def init_database(self):
        cursor = self.sl3base.cursor()
        cursor.execute("""
            CREATE TABLE quotes(
                source TEXT,
                symbol TEXT,
                timeframe INT,
                day INT,
                compression_type INT,
                quotation_data BLOB,
                PRIMARY KEY (source, symbol, timeframe, day)
            ) WITHOUT ROWID""")

            # CREATE TABLE quotes(
            #            "    source TEXT, "
            #            "    symbol TEXT, "
            #            "    timeframe INT, "
            #            "    day INT, "
            #            "    compression_type INT, "
            #            "    data BLOB,"
            #            "    open BLOB,"
            #            "    high BLOB,"
            #            "    low BLOB,"
            #            "    close BLOB,"
            #            "    volume BLOB,"
            #            "    PRIMARY KEY (source, symbol, timeframe, day)"
            #            ") WITHOUT ROWID")

    def save_day(self, source, symbol, timeframe, day_date, bar_data):
        assert isinstance(bar_data, OHLCV_day)

        quotation_data = []
        quotation_data.append(bar_data.time.tobytes())
        quotation_data.append(bar_data.open.tobytes())
        quotation_data.append(bar_data.high.tobytes())
        quotation_data.append(bar_data.low.tobytes())
        quotation_data.append(bar_data.close.tobytes())
        quotation_data.append(bar_data.volume.tobytes())
        # time = self.compress_numpy(bar_data.time, self.compression_type)
        # open = self.compress_numpy(bar_data.open, self.compression_type)
        # high = self.compress_numpy(bar_data.high, self.compression_type)
        # low = self.compress_numpy(bar_data.low, self.compression_type)
        # close = self.compress_numpy(bar_data.close, self.compression_type)
        # volume = self.compress_numpy(bar_data.volume, self.compression_type)

        params = {
            'source': source,
            'symbol': symbol,
            'timeframe': timeframe,
            'day': self.day_to_int(day_date),
            'compression_type': self.compression_type.value,
            'quotation_data': self.get_compression_module(self.compression_type).compress(b''.join(quotation_data))
        }
        cursor = self.sl3base.cursor()

        try:
            cursor.execute("""
                INSERT INTO quotes(source, symbol, timeframe, day, compression_type, quotation_data)
                VALUES (:source, :symbol, :timeframe, :day, :compression_type, :quotation_data)
                """, params)
        except sqlite3.IntegrityError:
            logging.warning(f're-updating quotes: {source} {symbol} {timeframe:s} {day_date}')

    @staticmethod
    def decompress_numpy_worker(args):
        data, numpy_type, decompression_func = args
        return np.frombuffer(decompression_func(data), numpy_type)

    def load_day(self, source, symbol, timeframe, day_date):

        params = {
            'source': source,
            'symbol': symbol,
            'timeframe': timeframe,
            'day': self.day_to_int(day_date)
        }

        cursor = self.sl3base.cursor()
        query_result = cursor.execute("""
            SELECT
                quotation_data, compression_type
            FROM
                quotes
            WHERE
                source = :source AND symbol = :symbol AND timeframe = :timeframe AND day = :day
        """, params)

        day_data = query_result.fetchone()
        if day_data is None:
            return None

        compression_type = CompressionType(day_data[1])

        compressoin_module = self.get_compression_module(compression_type)
        quotation_data = compressoin_module.decompress(day_data[0])
        #quotation_data = day_data[0]
        n_bars = len(quotation_data) // 6 // 8

        workers_args = []
        result = []
        blob_types = [TIME_TYPE] + [PRICE_TYPE] * 4 + [VOLUME_TYPE]
        for i_blob, blob_type in enumerate(blob_types):
            r = np.frombuffer(quotation_data, blob_type, n_bars, i_blob * 8)
            result.append(r)

        # pool = multiprocessing.Pool(6)
        # result = pool.map(self.decompress_numpy_worker, workers_args)

        time, open, high, low, close, volume = tuple(result)

        return OHLCV_day({
            'symbol': symbol,
            'timeframe': timeframe,
            'source': source,
            'is_incomplete_day': False,
            'time': time,
            'open': open,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
