from random import randint
# from sqlalchemy import create_engine
from connectors_to_databases.PostgreSQL import PostgreSQL
import pandas as pd
import sqlalchemy as sa

pg = PostgreSQL(
    port=1,
    password='MWX5zen1htj@qvz.ahu'
)

# pg_dwh = PostgreSQL(
#     host='10.250.201.231',
#     login='i.korsakov',
#     password='MWX5zen1htj@qvz.ahu'
# )


print(pg.execute_to_df('''select * from simple_'''))
#
# df = pg_dwh.execute_to_df('''SELECT event_json FROM
# ods.appm_export_events
# LIMIT 1''')
#
# pg.into_pg_table(df=df,pg_table_name='events')

# print(pd.DataFrame(data={'d':[1,2,3]}))

# pg.into_pg_table(
#     df=pd.DataFrame(data={'id':[1]}),
#     pg_table_name='simple_'
# )

# df = pd.DataFrame(data={'id':[1,2,3]})
#
# df.to_sql(
#     con=pg.__authorization_pg__(),
#     name='simple_',
#     index=False,
#     if_exists='append'
# )

# print(pg.__dict__)

# pg.authorization_pg()
# pg.execute_script(f'insert into simple_ values ({randint(1,100)})')
# try:
#     pg.execute_script(f'insert into simple_ values ({randint(1,100)})')
# except sa.exc.OperationalError as err:
#     print('ex err')

# from psycopg2 import OperationalError
# from sqlalchemy.exc import OperationalError

# raise OperationalError
# raise OperationalError
# host: str = 'localhost'
# database: str = 'postgres'
# login: str = 'postgres'
# password: str = '1'
# port: int = 5432
#
# engine_str = f'postgresql://{login}:{password}@{host}:{port}/{database}'
# engine = create_engine(engine_str)
#
# while True:
#     engine.execute(
#         f'''
#         insert into simple_ values ({randint(1,100)})
#         '''
#     )

