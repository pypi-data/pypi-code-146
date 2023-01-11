from sqlalchemize.create import create_table
from sqlalchemize.insert import insert_records


def create_test_table(engine):
    return create_table(table_name='xy',
                        column_names=['id', 'x', 'y'],
                        column_types=[int, int, int],
                        primary_key='id',
                        engine=engine,
                        if_exists='replace')


def insert_test_records(table):
    insert_records(table, [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}])
    
    