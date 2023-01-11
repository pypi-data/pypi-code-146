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
        except Exception as sloza__cqz:
            print('Exception on removing file: {error}'.format(error=
                sloza__cqz))


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
        except Exception as sloza__cqz:
            print('Exception on removing directory: {error}'.format(error=
                sloza__cqz))


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
            except Exception as sloza__cqz:
                print('Exception on removing file: {error}'.format(error=
                    sloza__cqz))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as sloza__cqz:
                print('Exception on removing directory: {error}'.format(
                    error=sloza__cqz))


@contextmanager
def ensure_clean_mysql_psql_table(conn, table_name_prefix='test_small_table'):
    import uuid
    from mpi4py import MPI
    from sqlalchemy import create_engine
    vuc__mfb = MPI.COMM_WORLD
    try:
        euxu__twn = None
        if bodo.get_rank() == 0:
            euxu__twn = f'{table_name_prefix}_{uuid.uuid4().hex}'
        euxu__twn = vuc__mfb.bcast(euxu__twn)
        yield euxu__twn
    finally:
        bodo.barrier()
        ufe__kulai = None
        if bodo.get_rank() == 0:
            try:
                jfx__xffm = create_engine(conn)
                qxw__svvyu = jfx__xffm.connect()
                qxw__svvyu.execute(f'drop table if exists {euxu__twn}')
            except Exception as sloza__cqz:
                ufe__kulai = sloza__cqz
        ufe__kulai = vuc__mfb.bcast(ufe__kulai)
        if isinstance(ufe__kulai, Exception):
            raise ufe__kulai


@contextmanager
def ensure_clean_snowflake_table(conn, table_name_prefix='test_table',
    parallel=True):
    import uuid
    from mpi4py import MPI
    vuc__mfb = MPI.COMM_WORLD
    try:
        euxu__twn = None
        if bodo.get_rank() == 0 or not parallel:
            euxu__twn = f'{table_name_prefix}_{uuid.uuid4().hex}'.upper()
        if parallel:
            euxu__twn = vuc__mfb.bcast(euxu__twn)
        yield euxu__twn
    finally:
        if parallel:
            bodo.barrier()
        ufe__kulai = None
        if bodo.get_rank() == 0 or not parallel:
            try:
                pd.read_sql(f'drop table if exists {euxu__twn}', conn)
            except Exception as sloza__cqz:
                ufe__kulai = sloza__cqz
        if parallel:
            ufe__kulai = vuc__mfb.bcast(ufe__kulai)
        if isinstance(ufe__kulai, Exception):
            raise ufe__kulai
