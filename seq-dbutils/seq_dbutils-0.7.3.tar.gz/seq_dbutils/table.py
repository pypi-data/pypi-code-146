import logging
import sys

import pandas as pd

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Table:

    def __init__(self, df_table, session_instance, table_subclass):
        assert isinstance(df_table, pd.DataFrame)
        assert hasattr(session_instance, 'execute')
        assert hasattr(table_subclass, '__tablename__')

        self.df_table = df_table
        self.session_instance = session_instance
        self.table_subclass = table_subclass

    def bulk_insert_df_table(self):
        if not self.df_table.empty:
            try:
                logging.info(f"Bulk inserting into table '{self.table_subclass.__tablename__}'")
                self.session_instance.bulk_insert_mappings(self.table_subclass, self.df_table.to_dict(orient='records'))
            except Exception as ex:
                logging.error('Failed to load data into database. Rolling back...')
                self.session_instance.rollback()
                logging.error(str(ex))
                sys.exit(1)
        else:
            logging.info(f"Skipping bulk insert for table '{self.table_subclass.__tablename__}' and empty dataframe")

    def bulk_update_df_table(self):
        if not self.df_table.empty:
            try:
                logging.info(f"Bulk updating table '{self.table_subclass.__tablename__}'")
                self.session_instance.bulk_update_mappings(self.table_subclass, self.df_table.to_dict(orient='records'))
            except Exception as ex:
                logging.error('Failed to update data in database. Rolling back...')
                self.session_instance.rollback()
                logging.error(str(ex))
                sys.exit(1)
        else:
            logging.info(f"Skipping bulk update for table '{self.table_subclass.__tablename__}' and empty dataframe")
