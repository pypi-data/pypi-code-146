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
        except Exception as zbonk__yivm:
            print('Exception on removing file: {error}'.format(error=
                zbonk__yivm))


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
        except Exception as zbonk__yivm:
            print('Exception on removing directory: {error}'.format(error=
                zbonk__yivm))


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
            except Exception as zbonk__yivm:
                print('Exception on removing file: {error}'.format(error=
                    zbonk__yivm))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as zbonk__yivm:
                print('Exception on removing directory: {error}'.format(
                    error=zbonk__yivm))


@contextmanager
def ensure_clean_mysql_psql_table(conn, table_name_prefix='test_small_table'):
    import uuid
    from mpi4py import MPI
    from sqlalchemy import create_engine
    roma__lmkie = MPI.COMM_WORLD
    try:
        rhlwq__ztu = None
        if bodo.get_rank() == 0:
            rhlwq__ztu = f'{table_name_prefix}_{uuid.uuid4().hex}'
        rhlwq__ztu = roma__lmkie.bcast(rhlwq__ztu)
        yield rhlwq__ztu
    finally:
        bodo.barrier()
        tkfpl__pqxbu = None
        if bodo.get_rank() == 0:
            try:
                vancw__snxz = create_engine(conn)
                wwsae__igxsn = vancw__snxz.connect()
                wwsae__igxsn.execute(f'drop table if exists {rhlwq__ztu}')
            except Exception as zbonk__yivm:
                tkfpl__pqxbu = zbonk__yivm
        tkfpl__pqxbu = roma__lmkie.bcast(tkfpl__pqxbu)
        if isinstance(tkfpl__pqxbu, Exception):
            raise tkfpl__pqxbu


@contextmanager
def ensure_clean_snowflake_table(conn, table_name_prefix='test_table',
    parallel=True):
    import uuid
    from mpi4py import MPI
    roma__lmkie = MPI.COMM_WORLD
    try:
        rhlwq__ztu = None
        if bodo.get_rank() == 0 or not parallel:
            rhlwq__ztu = f'{table_name_prefix}_{uuid.uuid4().hex}'.upper()
        if parallel:
            rhlwq__ztu = roma__lmkie.bcast(rhlwq__ztu)
        yield rhlwq__ztu
    finally:
        if parallel:
            bodo.barrier()
        tkfpl__pqxbu = None
        if bodo.get_rank() == 0 or not parallel:
            try:
                pd.read_sql(f'drop table if exists {rhlwq__ztu}', conn)
            except Exception as zbonk__yivm:
                tkfpl__pqxbu = zbonk__yivm
        if parallel:
            tkfpl__pqxbu = roma__lmkie.bcast(tkfpl__pqxbu)
        if isinstance(tkfpl__pqxbu, Exception):
            raise tkfpl__pqxbu
