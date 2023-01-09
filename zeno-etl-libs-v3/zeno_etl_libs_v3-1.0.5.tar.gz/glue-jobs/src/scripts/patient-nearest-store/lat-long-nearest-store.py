"""
Owner: neha.karekar@zeno.health
Purpose: to get patients nearest store
"""

import argparse
import os
import sys

import geopy as geopy
import geopy.distance

sys.path.append('../../../..')

sys.path.append('../../../..')
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from zeno_etl_libs.logger import get_logger

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-bs', '--batch_size', default=10, type=int, required=False)
parser.add_argument('-fr', '--full_run', default=0, type=int, required=False)

args, unknown = parser.parse_known_args()
env = args.env
full_run = args.full_run
batch_size = args.batch_size

os.environ['env'] = env
logger = get_logger()

rs_db = DB()
rs_db.open_connection()
s3 = S3()

schema = 'prod2-generico'
table_name = "lat-long-nearest-store"
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)


def geo_distance(lat1, long1, lat2, long2):
    geo_dist = geopy.distance.geodesic((lat1, long1), (lat2, long2)).km
    return geo_dist


query = f"""
    insert into "{schema}"."{table_name}" (
        "created-at",
        "latitude",
        longitude,
        "nearest-store-id" )
    select
        convert_timezone('Asia/Calcutta', GETDATE()),
        ll."latitude",
        ll.longitude,
        0
    from
        ( select
            latitude,
            longitude
        from
            "{schema}"."zeno-patient-address"
        where
            latitude != '' and latitude is not null
            and longitude != '' and longitude is not null
        group by 1, 2 ) ll
    left join "{schema}"."{table_name}" llns on
        (llns.latitude = ll.latitude
            and llns.longitude = ll.longitude)
    where
        llns.latitude is null and llns.longitude is null;
"""

""" Insert the new lat long in the table """
rs_db.execute(query=query)


def get_store_data():
    """
    function returns the stores lat, long data
    """
    store_query = f"""
        select 
            id,
            -- store as nearest_store,
            latitude,
            longitude
            -- , "store-type" 
        from 
            "{schema}"."stores-master" sm
        where
            "store-type" != 'dc'
            and sm.latitude != ''
            and sm.latitude is not null
            and sm.longitude != ''
            and sm.longitude is not null
            and sm."id" is not null 
    """
    _store_df = rs_db.get_df(store_query)
    logger.info(f'store count: {_store_df.shape}')
    return _store_df


def lat_long_nearest_store():
    global lat_long_df
    for ix, lat_long in lat_long_df.iterrows():
        nearest_store_id = store_df['id'][0]
        nearest_store_distance = 1000000
        for iy, store in store_df.iterrows():
            distance = geo_distance(lat_long['latitude'], lat_long['longitude'], store['latitude'],
                                    store['longitude'])
            if distance < nearest_store_distance:
                nearest_store_distance = distance
                nearest_store_id = store['id']

        lat_long_df.loc[ix, 'nearest-store-id'] = int(nearest_store_id)
    # return patient_df


def get_lat_long_data(batch=1):
    lat_long_query = f"""
        select
            latitude,
            longitude ,
            "nearest-store-id"
        from
            "prod2-generico"."lat-long-nearest-store"
        where
            "nearest-store-id" = 0
        LIMIT {batch_size} OFFSET {(batch - 1) * batch_size} 
    """

    _lat_long_df = rs_db.get_df(lat_long_query)
    logger.info(f'lat long batch count: {_lat_long_df.shape}')
    return _lat_long_df


def update_nearest_store():
    """ clean the temp table """
    t_query = f""" TRUNCATE TABLE {lat_long_temp_table} ;"""
    rs_db.execute(query=t_query)

    # Fixing the data type
    lat_long_df[['nearest-store-id']] = lat_long_df[['nearest-store-id']].astype(int)

    # fill the temp table
    s3.write_df_to_db(df=lat_long_df[temp_table_info['column_name']], db=rs_db,
                      table_name=lat_long_temp_table, schema=None)

    # Updating the data in table
    _query = f"""
        update
            "{schema}"."{table_name}" t
        set
            "nearest-store-id" = s."nearest-store-id"
        from
             {lat_long_temp_table} s
        where
            ( t.latitude = s.latitude and t.longitude = s.longitude)
    """
    rs_db.execute(query=_query)


try:
    store_df = get_store_data()
    batch = 1
    lat_long_df = get_lat_long_data(batch=batch)

    if not lat_long_df.empty:
        # Create temp table and update the nearest store
        lat_long_temp_table = table_name.replace("-", "_") + "_temp"
        rs_db.execute(query=f"DROP table IF EXISTS {lat_long_temp_table};")
        _query = f"""
                CREATE TEMP TABLE {lat_long_temp_table}
                (
                    latitude VARCHAR(765)   ENCODE lzo
                    ,longitude VARCHAR(765)   ENCODE lzo
                    ,"nearest-store-id" INTEGER NOT NULL  ENCODE az64
                );
            """
        rs_db.execute(query=_query)
        temp_table_info = helper.get_table_info(db=rs_db, table_name=lat_long_temp_table,
                                                schema=None)

    while not lat_long_df.empty:
        logger.info(f'Starting batch number:{batch}')

        lat_long_nearest_store()  # calculate the nearest store
        update_nearest_store()  # update the nearest store

        logger.info(f'End of batch number:{batch}')

        if not full_run:
            break

        batch += 1
        lat_long_df = get_lat_long_data(batch=batch)

except Exception as e:
    logger.exception(e)
finally:
    rs_db.close_connection()
