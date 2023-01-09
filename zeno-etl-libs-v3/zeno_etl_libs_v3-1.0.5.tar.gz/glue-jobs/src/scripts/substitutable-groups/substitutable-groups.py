#owner : aashish.mishra
#objective : Track the groups where generic substitution is available
import argparse
import sys
import os
sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB


def main(db):
    table_name = "substitutable-groups"

    db.execute(query="begin ;")
    db.execute(query=f""" delete from "prod2-generico"."{table_name}"; """)
    query = f"""
    insert
        into
        "prod2-generico"."{table_name}" (
                "id", 
                "created-by", 
                "created-at", 
                "updated-by", 
                "updated-at", 
                "group", 
                "generic-flag"
                )    
        select
            d."group" as "id",
            'etl-automation' as "created-by",
            convert_timezone('Asia/Calcutta',
            GETDATE()) as "created-at",
            'etl-automation' as "updated-by",
            convert_timezone('Asia/Calcutta',
            GETDATE()) as "updated-at",
            d."group" as "group",
            count(distinct(case when (d1."type" = 'generic') then c."drug-id" end)) as "generic-flag"
        from
            "prod2-generico"."drug-unique-composition-mapping" d
        inner join "prod2-generico"."drugs" d1 on
            d1.id = d."drug-id"
        inner join "prod2-generico"."inventory-1" c on
            c."drug-id" = d."drug-id"
        inner join "prod2-generico"."bill-items-1" a on
            c."id" = a."inventory-id"
        where
            d."group" is not null
            and d1."type" = 'generic'
        group by
            d."group"
            ;
    """
    db.execute(query=query)

    """ committing the transaction """
    db.execute(query=" end; ")

    # ##Vacuum Clean
    #
    # clean = f"""
    #               VACUUM full "prod2-generico"."substitutable-compositions";
    #                   """
    # db.execute(query=clean)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                        help="This is env(dev, stag, prod)")
    args, unknown = parser.parse_known_args()
    env = args.env
    os.environ['env'] = env
    logger = get_logger()
    logger.info(f"env: {env}")

    rs_db = DB()
    rs_db.open_connection()

    """ For single transaction  """
    rs_db.connection.autocommit = False

    """ calling the main function """
    main(db=rs_db)

    # Closing the DB Connection
    rs_db.close_connection()
