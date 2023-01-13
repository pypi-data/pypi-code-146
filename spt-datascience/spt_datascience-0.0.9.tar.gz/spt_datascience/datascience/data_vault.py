from psycopg2.extensions import register_adapter, AsIs
from functools import partial
import numpy as np


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)


def _insert_batch_df(df, conn, table):
    cursor = conn.cursor()
    cols = df.columns.tolist()
    values = [cursor.mogrify("(%s)" % ','.join('%s' for _ in cols), tup).decode('utf8') for tup in
              df.itertuples(index=False)]
    query = "INSERT INTO %s(%s) VALUES " % (table, ','.join(cols)) + ",".join(values)
    cursor.execute(query)
    conn.commit()
    cursor.close()


def insert_df(df, conn, table, batch_size=1_000_000):
    size = df.shape[0]
    for ind in range(0, size, batch_size):
        _insert_batch_df(df.iloc[ind:ind + batch_size], conn, table)


class DataVault:

    @staticmethod
    def hash_cols(cols, cur):
        """
        This method returns sql injection helping to make a hash of values
        """
        hashed_cols = ','.join(map(
            lambda col: f"coalesce(nullif(upper(trim(cast(%s as varchar))), ''), '^^')" %
                        cur.mogrify("%s", (col,)).decode('utf-8'),
            cols
        ))
        return f"cast(md5(nullif(concat_ws('||',%s), '^^||^^')) as text)" % hashed_cols

    @staticmethod
    def hash_col(col, cur):
        return f"cast(md5(nullif(concat_ws('||',%s), '^^||^^')) as text)" % \
               f"coalesce(nullif(upper(trim(cast(%s as varchar))), ''), '^^')" % \
               cur.mogrify("%s", (col,)).decode('utf-8')

    @staticmethod
    def hub(data_df, config, conn):
        """
        Use it to upload data to hub of Data Vault
        :param data_df: pandas dataframe
        :param config: config file
        :param conn: connection to database
        """
        schema = config.get('schema', 'business_vault')
        src_pk = config.get('src_pk')
        src_nk = config.get('src_nk')
        destination = schema + '.' + config['table']
        record_source = config.get('record_source')

        with conn.cursor() as cur:
            hash_col = partial(DataVault.hash_col, cur=cur)
            data_df[src_pk] = data_df[src_nk].apply(hash_col)
            args_str = ','.join(
                "(%s, " % row[src_pk] + cur.mogrify(
                    "%s, %s, now())", (row[src_nk], record_source)
                ).decode('utf-8')
                for i, row in data_df.iterrows()
            )
            query = "insert into %s (%s) VALUES " % (
                destination, ','.join([src_pk, src_nk, 'record_source', 'load_date'])) + args_str
            cur.execute(query)

    @staticmethod
    def satellite(data_df, config, conn):
        """
        Use it to upload data to satellite of Data Vault
        :param data_df: pandas dataframe
        :param config: config file
        :param conn: connection to database
        """
        schema = config.get('schema', 'business_vault')
        src_pk = config.get('src_pk')
        src_pk_computable = config.get('src_pk_computable')
        src_nk = config.get('src_nk')
        src_hashdiff = config.get('src_hashdiff')
        destination = schema + '.' + config['table']
        src_payload = config.get('src_payload')
        record_source = config.get('record_source')

        with conn.cursor() as cur:
            hash_col = partial(DataVault.hash_col, cur=cur)
            hash_cols = partial(DataVault.hash_cols, cur=cur)
            if src_nk is not None:
                if isinstance(src_nk, list):
                    data_df[src_pk] = data_df[src_nk].apply(hash_cols)
                else:
                    data_df[src_pk] = data_df[src_nk].apply(hash_col)
            elif src_pk_computable is not None:
                data_df[src_pk] = data_df[src_pk_computable]
            else:
                data_df[src_pk] = data_df[src_pk].apply(
                    lambda pk: cur.mogrify('%s', (pk,)).decode('utf-8')
                )
            data_df['hashdiff'] = data_df[src_payload].apply(hash_cols, axis=1)
            args_str = ','.join(
                "(%s, " % row[src_pk] + cur.mogrify(
                    "%s, now(), now()," + "%s," * len(src_payload), [record_source] + row[src_payload].tolist()
                ).decode('utf-8') + row['hashdiff'] + ")"
                for i, row in data_df.iterrows()
            )
            query = "insert into %s (%s) VALUES " % (
                destination, ','.join([src_pk, 'record_source', 'effective_from', 'load_date'] + src_payload + [src_hashdiff])) \
                    + args_str
            cur.execute(query)

    @staticmethod
    def link(data_df, config, conn):
        """
        Use it to upload data to link of Data Vault
        :param data_df: pandas dataframe
        :param config: config file
        :param conn: connection to database
        """
        schema = config.get('schema', 'business_vault')
        src_pk = config.get('src_pk')
        src_fk = config.get('src_fk')
        l_link, r_link = src_fk[0], src_fk[1]
        destination = schema + '.' + config['table']
        data_df['record_source'] = config.get('record_source')

        with conn.cursor() as cur:
            hash_cols = partial(DataVault.hash_cols, cur=cur)
            data_df['link_pk'] = data_df[src_fk].apply(hash_cols, axis=1)
            args_str = ','.join("(%s, " % row['link_pk'] + cur.mogrify(
                "%s, %s, %s, now())", (row[l_link], row[r_link], row['record_source'])
            ).decode('utf-8')
                                for i, row in data_df.iterrows())
            query = "insert into %s (%s) VALUES " % (
                destination, ','.join([src_pk, l_link, r_link, 'record_source', 'load_date'])) + args_str
            cur.execute(query)



    @staticmethod
    def multi_link(data_df, config, conn):
        """
        Use it to upload data to link of Data Vault
        :param data_df: pandas dataframe
        :param config: config file
        :param conn: connection to database
        """
        schema = config.get('schema', 'business_vault')
        src_pk = config.get('src_pk')
        src_fk = config.get('src_fk')
        nk_fk_map = config.get('nk_fk_map')
        destination = schema + '.' + config['table']
        data_df['record_source'] = config.get('record_source')

        with conn.cursor() as cur:
            hash_col = partial(DataVault.hash_col, cur=cur)
            hash_cols = partial(DataVault.hash_cols, cur=cur)

            for fk in src_fk:
                if fk not in nk_fk_map.values():
                    data_df[fk] = data_df[fk].apply(
                        lambda fk: cur.mogrify('%s', (fk,)).decode('utf-8')
                    )

            for nk, fk in nk_fk_map.items():
                data_df[fk] = data_df[nk].apply(hash_col)
            data_df[src_pk] = data_df[src_fk].apply(hash_cols, axis=1)

            def build_value(row):
                return "(%s, " % row[src_pk] + \
                    ', '.join(row[fk] for fk in src_fk) + \
                    cur.mogrify(", %s, now())", (row['record_source'],)).decode('utf-8')

            args_str = ','.join(
                    build_value(row)
            for i, row in data_df.iterrows())

            query = "insert into %s (%s) VALUES %s" % (
                destination, ','.join([
                    src_pk,
                    *(fk for fk in src_fk),
                    'record_source', 'load_date']),
                args_str
            )
            cur.execute(query)
