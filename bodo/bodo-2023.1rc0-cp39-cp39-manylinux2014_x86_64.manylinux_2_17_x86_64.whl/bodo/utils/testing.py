import os
import shutil
from contextlib import contextmanager
import pandas as pd
import bodo


@bodo.jit
def get_rank():
    return bodo.libs.distributed_api.get_rank()


@bodo.jit
def barrier():
    return bodo.libs.distributed_api.barrier()


@contextmanager
def ensure_clean(filename):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(filename) and os.path.isfile(
                filename):
                os.remove(filename)
        except Exception as okgc__djdvc:
            print('Exception on removing file: {error}'.format(error=
                okgc__djdvc))


@contextmanager
def ensure_clean_dir(dirname):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(dirname) and os.path.isdir(
                dirname):
                shutil.rmtree(dirname)
        except Exception as okgc__djdvc:
            print('Exception on removing directory: {error}'.format(error=
                okgc__djdvc))


@contextmanager
def ensure_clean2(pathname):
    try:
        yield
    finally:
        barrier()
        if get_rank() == 0:
            try:
                if os.path.exists(pathname) and os.path.isfile(pathname):
                    os.remove(pathname)
            except Exception as okgc__djdvc:
                print('Exception on removing file: {error}'.format(error=
                    okgc__djdvc))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as okgc__djdvc:
                print('Exception on removing directory: {error}'.format(
                    error=okgc__djdvc))


@contextmanager
def ensure_clean_mysql_psql_table(conn, table_name_prefix='test_small_table'):
    import uuid
    from mpi4py import MPI
    from sqlalchemy import create_engine
    ikly__gas = MPI.COMM_WORLD
    try:
        qyjz__gxpz = None
        if bodo.get_rank() == 0:
            qyjz__gxpz = f'{table_name_prefix}_{uuid.uuid4().hex}'
        qyjz__gxpz = ikly__gas.bcast(qyjz__gxpz)
        yield qyjz__gxpz
    finally:
        bodo.barrier()
        hxn__eakn = None
        if bodo.get_rank() == 0:
            try:
                vnw__vid = create_engine(conn)
                qtjw__pjwuo = vnw__vid.connect()
                qtjw__pjwuo.execute(f'drop table if exists {qyjz__gxpz}')
            except Exception as okgc__djdvc:
                hxn__eakn = okgc__djdvc
        hxn__eakn = ikly__gas.bcast(hxn__eakn)
        if isinstance(hxn__eakn, Exception):
            raise hxn__eakn


@contextmanager
def ensure_clean_snowflake_table(conn, table_name_prefix='test_table',
    parallel=True):
    import uuid
    from mpi4py import MPI
    ikly__gas = MPI.COMM_WORLD
    try:
        qyjz__gxpz = None
        if bodo.get_rank() == 0 or not parallel:
            qyjz__gxpz = f'{table_name_prefix}_{uuid.uuid4().hex}'.upper()
        if parallel:
            qyjz__gxpz = ikly__gas.bcast(qyjz__gxpz)
        yield qyjz__gxpz
    finally:
        if parallel:
            bodo.barrier()
        hxn__eakn = None
        if bodo.get_rank() == 0 or not parallel:
            try:
                pd.read_sql(f'drop table if exists {qyjz__gxpz}', conn)
            except Exception as okgc__djdvc:
                hxn__eakn = okgc__djdvc
        if parallel:
            hxn__eakn = ikly__gas.bcast(hxn__eakn)
        if isinstance(hxn__eakn, Exception):
            raise hxn__eakn
