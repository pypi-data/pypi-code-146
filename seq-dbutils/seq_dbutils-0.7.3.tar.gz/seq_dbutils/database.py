import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Database:

    @staticmethod
    def get_db_table_col_list(engine, tablename):
        df_db_table_cols = pd.read_sql(f'SHOW COLUMNS FROM {tablename};', engine)
        db_table_col_list = df_db_table_cols['Field'].tolist()
        return db_table_col_list

    @staticmethod
    def create_db_table_dataframe(df, engine, tablename):
        db_table_col_list = Database.get_db_table_col_list(engine, tablename)
        df_db_table = df.filter(db_table_col_list, axis=1)
        df_db_table = df_db_table.dropna(subset=df_db_table.columns, how='all')
        logging.info(f"'{tablename}' rows to load: {len(df_db_table)}")
        return df_db_table

    @staticmethod
    def commit_changes(session_instance, commit):
        if commit:
            session_instance.commit()
            logging.info('Changes committed')
        else:
            logging.info('Changes NOT committed')
