"""
Purpose: To ensure all the playstore reviews are present in the redshfift table. There are two
source of reviews.
1. CSV file: It has both, star ratings and reviews
2. API: It has ONLY reviews
This script will run daily and fetch the data using API and will put it the table. And At the
beginning of the month, this same script, will fetch the CSV data and append the reviewer name
(using scarper lib of python) and will put them in the same table.

Author : neha.karekar@zeno.health
"""

import argparse
import sys
import os
import datetime
from io import StringIO
import dateutil
import numpy as np
from pandas.io.json import json_normalize
import pandas as pd

sys.path.append('../../../..')
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from zeno_etl_libs.helper.google.playstore.playstore import Reviews

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument(
    '-sd', '--start_datetime', default="NA", type=str, required=False,
    help="If start date is 'NA' then latest review for the day and month will be added, for full"
         " run make the start date old")

parser.add_argument(
    '-et', '--email_to',
    default="hardik.amal@zeno.health,neha.karekar@zeno.health,kuldeep.singh@zeno.health", type=str,
    required=False)

args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to
start_datetime = args.start_datetime
os.environ['env'] = env

logger = get_logger()
logger.info(f"start_date: {start_datetime}")

# Read using google API
r = Reviews()
rs_db = DB(read_only=False)
rs_db.open_connection()
s3 = S3()

schema = 'prod2-generico'
table_name = 'playstore-reviews'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
logger.info(f"Table:{table_name} exists")


def insert_reviews(df):
    """
    Function helps in insert daily and monthly reviews in table, columns which are absent will be
    filled with default values
    """

    must_present = "RaiseException"

    # Insert data
    table_columns = {
        "review-created-at": must_present,
        "review-id": np.nan,
        "star-rating": must_present,
        "author-name": np.nan,
        "user-image": np.nan,
        "review": np.nan,
        "reviewer-lang": "en",
        "thumbsup-count": np.nan,
        "review-link": np.nan,
        "replied-at": np.nan,
        "reply-content": np.nan,
        "year": must_present,
        "month": must_present,
        "created-at": datetime.datetime.now(tz=dateutil.tz.gettz('Asia/Kolkata')).strftime(
            '%Y-%m-%d %H:%M:%S'),
        "created-by": "etl-automation",
        "updated-by": "etl-automation",
        "updated-at": datetime.datetime.now(tz=dateutil.tz.gettz('Asia/Kolkata')).strftime(
            '%Y-%m-%d %H:%M:%S')
    }

    for column in table_columns:
        if column not in df.columns:
            if table_columns[column] == must_present:
                raise Exception(f"{column} column must be present.")
            df[column] = table_columns[column]
    s3.write_df_to_db(df=df[table_columns.keys()], table_name=table_name, db=rs_db, schema=schema)


def get_month_reviews(year, month):
    """
    return the review of given month and year from s3 CSV file
    """
    uri = f"s3://aws-glue-temporary-921939243643-ap-south-1/playstore-reviews/" \
          f"reviews_reviews_com.zenohealth.android_{year}{str(month).zfill(2)}.csv"
    logger.info(f"uri: {uri}")
    csv_string = s3.get_file_object(uri=uri, encoding="utf-16")
    df = pd.read_csv(StringIO(csv_string))
    df['month'] = str(month).zfill(2)
    df['year'] = str(year)

    return df


def get_last_review_date():
    """
    Gets the last review date in the table

    :return: last review date
    """
    query = f""" select max("review-created-at") last_review_date from "{schema}"."{table_name}" 
    where "review-id" != '' """
    df: pd.DataFrame = rs_db.get_df(query=query)
    df['last_review_date'].fillna(np.nan, inplace=True)
    last_review_date = df['last_review_date'].to_string(index=False)
    logger.info(f"last_review_date: {last_review_date}")
    return last_review_date


def get_last_review_year_month():
    """
    Get the last review year and month for the CSV reviews without comments

    :returns: year, month
    """
    query = f""" select "year" last_year, "month" last_month from 
    "{schema}"."{table_name}" where "review-id" = '' order by year desc, month desc limit 1; """
    df = rs_db.get_df(query=query)
    if df.empty:
        return 0, 0
    df['last_year'].fillna(0, inplace=True)
    df['last_month'].fillna(0, inplace=True)
    last_year = df['last_year'].astype(int)
    last_month = df['last_month'].astype(int)
    logger.info(f"last_year, last_month: {last_year, last_month}")
    return int(last_year), int(last_month)


# set the start and end time
start_year = 2021
start_month = 1
if start_datetime == 'NA':
    # """ for daily review """
    last_review_date = get_last_review_date()
    if last_review_date == 'NaN':
        # set very old date
        start_datetime = '2017-01-01 00:00:00'
    else:
        start_datetime = last_review_date

    # """ for monthly review """
    table_year, table_month = get_last_review_year_month()
    if table_year == 0 and table_month == 0:
        # """ keeping it same 2021, 01 """
        pass
    else:
        # """ Every day it will refresh the last table month from s3 csv  """
        start_year = table_year
        start_month = table_month

end_date = datetime.date.today() + dateutil.relativedelta.relativedelta(months=-1)
end_year = end_date.year
end_month = end_date.month

start_datetime = dateutil.parser.parse(start_datetime)
logger.info(f"start_datetime: {start_datetime}")

day_diff = datetime.datetime.now() - start_datetime

# So that we do not fetch all the reviews every time
estimated_count = (day_diff.days + 1) * 3
logger.info(f"estimated_count: {estimated_count}")

reviews_list = r.get_all_review(count=estimated_count)

reviews_df = json_normalize(reviews_list)

# Column mapping
columns = {
    'reviewId': 'review-id',
    'userName': 'author-name',
    'userImage': 'user-image',
    'content': 'review',
    'score': 'star-rating',
    'thumbsUpCount': 'thumbsup-count',
    'at': 'review-created-at',
    'replyContent': 'reply-content',
    'repliedAt': 'replied-at'
}

reviews_df = reviews_df[columns.keys()].rename(columns=columns)

# Filter the existing reviews
reviews_df['review-created-at'] = reviews_df['review-created-at'].apply(
    pd.to_datetime, errors='coerce')
reviews_df = reviews_df[(reviews_df['review-created-at'] > start_datetime)]

# Review link calculation
reviews_df['review-link'] = reviews_df['review-id'].apply(
    lambda
        x: f"http://play.google.com/console/developers/7917307073215847519/app/4974372962404296517/"
           f"user-feedback/review-details?reviewId={x}&corpus=PUBLIC_REVIEWS")

reviews_df['year'] = reviews_df['review-created-at'].apply(lambda x: x.year)
reviews_df['month'] = reviews_df['review-created-at'].apply(lambda x: x.month)

# Delete the existing reviews if any
truncate_query = f''' DELETE FROM "{schema}"."{table_name}" where "review-created-at" > 
'{start_datetime}' and "review-id" is not null '''
rs_db.execute(truncate_query)

logger.info(f"reviews_df: {reviews_df.head(2)}")
# Insert
if reviews_df.empty:
    logger.info("No data to insert.")
else:
    insert_reviews(df=reviews_df)
logger.info("End of daily reviews.")

# """ Monthly Reviews """

print(f"start year, month: {start_year, start_month}")
print(f"end year, month: {end_year, end_month}")

csv_r_df = pd.DataFrame()
for year in range(start_year, end_year + 1):
    for month in range(1, 12 + 1):
        if year == start_year and month < start_month:
            # """ stopping for old month"""
            continue
        if year == end_year and month > end_month:
            # """ stopping for new months"""
            continue
        print(f"year, month: {year, month}")
        df = get_month_reviews(year=year, month=month)
        csv_r_df = pd.concat([csv_r_df, df], ignore_index=True)

        # Delete the old reviews data from table
        query = f"""delete from "{schema}"."{table_name}" where "review-id" = '' and year = {year} 
        and month = {month}; """
        rs_db.execute(query=query)

logger.info(f"csv_r_df.head(1): {csv_r_df.head(1)}")

# Filter only start rating review
csv_r_df = csv_r_df[csv_r_df['Review Link'].isna()]
columns = {
    'Star Rating': 'star-rating',
    'Review Submit Date and Time': 'review-created-at',
    'year': 'year',
    'month': 'month'
}

# # fetching review-id from review link
# csv_r_df['reviewId'] = csv_r_df['Review Link'].apply(
#     lambda x: re.search('reviewId=(.*)&', str(x)).group(1) if 'reviewId' in str(x) else x)

csv_r_df = csv_r_df[columns.keys()].rename(columns=columns)
csv_r_df['review-created-at'] = pd.to_datetime(csv_r_df['review-created-at'],
                                               format='%Y-%m-%dT%H:%M:%SZ')

# Insert
if csv_r_df.empty:
    logger.info(f"No CSV data to insert: {csv_r_df}")
else:
    logger.info(f"Update/Insert CSV data count: {len(csv_r_df)}")
    insert_reviews(df=csv_r_df)
logger.info("End of monthly reviews.")

rs_db.close_connection()


def last_day_of_month(any_day):
    """
    The day 28 exists in every month. 4 days later, it's always next month

    :param any_day: datetime object of date
    :returns: last day of the month
    """
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - datetime.timedelta(days=next_month.day)


# """ Send monthly reminder of playstore review file(CSV) """
today = datetime.date.today()
last_day_of_month = last_day_of_month(any_day=today)

if today == last_day_of_month:
    subject = '''[Reminder] Playstore reviews monthly CSV file '''
    mail_body = f'''Hey Hardik, 
    
Please send the playstore reviews csv file for the 
year: {last_day_of_month.year}, month: {last_day_of_month.month}.
    
@Neha: Please upload this file at this location: 
s3://aws-glue-temporary-921939243643-ap-south-1/playstore-reviews/
    
Please complete this activity by EOD, otherwise our glue/cron job will fail tomorrow.

Thanks,
Team Data
    '''
    email = Email()
    email.send_email_file(subject=subject, mail_body=mail_body, to_emails=email_to, file_uris=[])
