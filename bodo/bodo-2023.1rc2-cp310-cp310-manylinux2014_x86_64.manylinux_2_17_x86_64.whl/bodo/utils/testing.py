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
        except Exception as uke__eazyc:
            print('Exception on removing file: {error}'.format(error=
                uke__eazyc))


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
        except Exception as uke__eazyc:
            print('Exception on removing directory: {error}'.format(error=
                uke__eazyc))


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
            except Exception as uke__eazyc:
                print('Exception on removing file: {error}'.format(error=
                    uke__eazyc))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as uke__eazyc:
                print('Exception on removing directory: {error}'.format(
                    error=uke__eazyc))


@contextmanager
def ensure_clean_mysql_psql_table(conn, table_name_prefix='test_small_table'):
    import uuid
    from mpi4py import MPI
    from sqlalchemy import create_engine
    mmkq__ril = MPI.COMM_WORLD
    try:
        dvpb__uctxz = None
        if bodo.get_rank() == 0:
            dvpb__uctxz = f'{table_name_prefix}_{uuid.uuid4().hex}'
        dvpb__uctxz = mmkq__ril.bcast(dvpb__uctxz)
        yield dvpb__uctxz
    finally:
        bodo.barrier()
        gyvor__hwt = None
        if bodo.get_rank() == 0:
            try:
                winhc__rnnpt = create_engine(conn)
                crhk__ndafy = winhc__rnnpt.connect()
                crhk__ndafy.execute(f'drop table if exists {dvpb__uctxz}')
            except Exception as uke__eazyc:
                gyvor__hwt = uke__eazyc
        gyvor__hwt = mmkq__ril.bcast(gyvor__hwt)
        if isinstance(gyvor__hwt, Exception):
            raise gyvor__hwt


@contextmanager
def ensure_clean_snowflake_table(conn, table_name_prefix='test_table',
    parallel=True):
    import uuid
    from mpi4py import MPI
    mmkq__ril = MPI.COMM_WORLD
    try:
        dvpb__uctxz = None
        if bodo.get_rank() == 0 or not parallel:
            dvpb__uctxz = f'{table_name_prefix}_{uuid.uuid4().hex}'.upper()
        if parallel:
            dvpb__uctxz = mmkq__ril.bcast(dvpb__uctxz)
        yield dvpb__uctxz
    finally:
        if parallel:
            bodo.barrier()
        gyvor__hwt = None
        if bodo.get_rank() == 0 or not parallel:
            try:
                pd.read_sql(f'drop table if exists {dvpb__uctxz}', conn)
            except Exception as uke__eazyc:
                gyvor__hwt = uke__eazyc
        if parallel:
            gyvor__hwt = mmkq__ril.bcast(gyvor__hwt)
        if isinstance(gyvor__hwt, Exception):
            raise gyvor__hwt
