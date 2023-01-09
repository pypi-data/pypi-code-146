"""
Owner: neha.karekar@zeno.health
Purpose: to get patients nearest store
"""

import argparse
import os
import sys

import dateutil
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
table_name = "patient-nearest-store"
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)


def geo_distance(lat1, long1, lat2, long2):
    geo_dist = geopy.distance.geodesic((lat1, long1), (lat2, long2)).km
    return geo_dist


max_q = f""" select max("created-at") max_exp from "{schema}"."{table_name}" """
max_date = rs_db.get_df(max_q)
max_date = max_date['max_exp'][0]
logger.info(f'max date: {max_date}')

# params
if max_date is None:
    start_date = '2017-05-13 00:00:00'
    start_date = dateutil.parser.parse(start_date)
else:
    start_date = max_date
logger.info(f'start_date: {start_date}')


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


def patient_nearest_store():
    global patient_df
    for ix, patient in patient_df.iterrows():
        nearest_store_id = store_df['id'][0]
        nearest_store_distance = 1000000
        for iy, store in store_df.iterrows():
            distance = geo_distance(patient['latitude'], patient['longitude'], store['latitude'],
                                    store['longitude'])
            if distance < nearest_store_distance:
                nearest_store_distance = distance
                nearest_store_id = store['id']
                # logger.info(
                #     f"i: {ix}, patient id: {patient['id']}, nearest_store_id: {nearest_store_id}, "
                #     f"nearest_store_distance: {nearest_store_distance}")
        patient_df.loc[ix, 'nearest-store-id'] = int(nearest_store_id)
    # return patient_df


def get_patients_data(batch=1):
    patient_query = f"""
        select
            pm.id
            , pm."last-bill-date"
            -- , pm."primary-store-id"
            , zpa.latitude
            , zpa.longitude
            -- , "previous-store-id"
        from
            "{schema}"."patients-metadata-2" pm
        inner join (
                select 
                    "patient-id",
                    latitude,
                    longitude,
                    rank() over (partition by "patient-id" order by "created-at" desc ) r
                from 
                    "{schema}"."zeno-patient-address"
        ) zpa on
            zpa."patient-id" = pm.id
        where
            r = 1
            and zpa.latitude is not null 
            and zpa.latitude != ''
            and zpa.longitude is not null 
            and zpa.longitude != ''
            and pm."last-bill-date" >= '{start_date}'
            -- and pm.id is not null
            -- and pm.id = 5
            -- and pm."primary-store-id" in (16,2)
            -- and pm."last-bill-date" >= CURRENT_DATE - 90 
        group by
            1,2,3,4
        order by 
            pm."last-bill-date" asc
        LIMIT {batch_size} OFFSET {(batch - 1) * batch_size} 
    """

    _patient_df = rs_db.get_df(patient_query)
    logger.info(f'patient batch count: {_patient_df.shape}')
    return _patient_df

    # pat['i'] = 1
    # store['i'] = 1
    # hash_join = pat.merge(store, how='left', on='i')
    # hash_join['geo_dist'] = hash_join.apply(
    #     lambda x: geo_distance(x.latitude_x, x.longitude_x, x.latitude_y, x.longitude_y), axis=1)
    # hash_join['rank'] = hash_join.sort_values(by=['geo_dist']).groupby(['patient-id']).cumcount() + 1
    # hash_join = hash_join[hash_join['rank'] == 1].copy()
    # hash_join.columns = [c.replace('_', '-').lower() for c in hash_join.columns]
    # hash_join = hash_join[['patient-id', 'nearest-store-id']]
    # hash_join['created-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    # return hash_join


try:
    truncate_query = f''' DELETE FROM "{schema}"."{table_name}" where date("created-at") > '{start_date}' '''
    logger.info(f'truncate query: {truncate_query}')
    rs_db.execute(truncate_query)
    logger.info(f'batch size type:{type(batch_size)}')
    store_df = get_store_data()
    batch = 1
    patient_df = get_patients_data(batch=batch)
    while not patient_df.empty:
        logger.info(f'Starting batch number:{batch}')
        patient_nearest_store()
        """ rename the columns """
        patient_df.rename(columns={"id": "patient-id", "last-bill-date": "created-at"},
                          inplace=True)
        patient_df[['nearest-store-id']] = patient_df[['nearest-store-id']].astype(int)
        s3.write_df_to_db(df=patient_df[table_info['column_name']],
                          table_name=table_name, db=rs_db,
                          schema=schema)
        logger.info(f'End of batch number:{batch}')

        if not full_run:
            break

        batch += 1
        patient_df = get_patients_data(batch=batch)

except Exception as e:
    logger.exception(e)
finally:
    rs_db.close_connection()
