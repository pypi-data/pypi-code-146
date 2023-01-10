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
        except Exception as iatuk__nbf:
            print('Exception on removing file: {error}'.format(error=
                iatuk__nbf))


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
        except Exception as iatuk__nbf:
            print('Exception on removing directory: {error}'.format(error=
                iatuk__nbf))


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
            except Exception as iatuk__nbf:
                print('Exception on removing file: {error}'.format(error=
                    iatuk__nbf))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as iatuk__nbf:
                print('Exception on removing directory: {error}'.format(
                    error=iatuk__nbf))


@contextmanager
def ensure_clean_mysql_psql_table(conn, table_name_prefix='test_small_table'):
    import uuid
    from mpi4py import MPI
    from sqlalchemy import create_engine
    ethl__sbey = MPI.COMM_WORLD
    try:
        jukal__jjh = None
        if bodo.get_rank() == 0:
            jukal__jjh = f'{table_name_prefix}_{uuid.uuid4().hex}'
        jukal__jjh = ethl__sbey.bcast(jukal__jjh)
        yield jukal__jjh
    finally:
        bodo.barrier()
        ewajh__dsde = None
        if bodo.get_rank() == 0:
            try:
                wdjw__jorik = create_engine(conn)
                qhu__iiz = wdjw__jorik.connect()
                qhu__iiz.execute(f'drop table if exists {jukal__jjh}')
            except Exception as iatuk__nbf:
                ewajh__dsde = iatuk__nbf
        ewajh__dsde = ethl__sbey.bcast(ewajh__dsde)
        if isinstance(ewajh__dsde, Exception):
            raise ewajh__dsde


@contextmanager
def ensure_clean_snowflake_table(conn, table_name_prefix='test_table',
    parallel=True):
    import uuid
    from mpi4py import MPI
    ethl__sbey = MPI.COMM_WORLD
    try:
        jukal__jjh = None
        if bodo.get_rank() == 0 or not parallel:
            jukal__jjh = f'{table_name_prefix}_{uuid.uuid4().hex}'.upper()
        if parallel:
            jukal__jjh = ethl__sbey.bcast(jukal__jjh)
        yield jukal__jjh
    finally:
        if parallel:
            bodo.barrier()
        ewajh__dsde = None
        if bodo.get_rank() == 0 or not parallel:
            try:
                pd.read_sql(f'drop table if exists {jukal__jjh}', conn)
            except Exception as iatuk__nbf:
                ewajh__dsde = iatuk__nbf
        if parallel:
            ewajh__dsde = ethl__sbey.bcast(ewajh__dsde)
        if isinstance(ewajh__dsde, Exception):
            raise ewajh__dsde
