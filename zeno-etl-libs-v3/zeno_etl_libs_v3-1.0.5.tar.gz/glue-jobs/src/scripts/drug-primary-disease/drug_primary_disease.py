import argparse
import sys
import os
sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB


def main(db):
    table_name = "drug-primary-disease"

    db.execute(query="begin ;")
    db.execute(query=f""" delete from "prod2-generico"."{table_name}"; """)
    query = f"""
    insert into
        "prod2-generico"."{table_name}" (
            "created-by",
            "created-at",
            "updated-by",
            "updated-at",
            "drug-id",
            "drug-primary-disease"
            )
        select
        'etl-automation' as "created-by",
        convert_timezone('Asia/Calcutta',
        GETDATE()) as "created-at",
        'etl-automation' as "updated-by",
        convert_timezone('Asia/Calcutta',
        GETDATE()) as "updated-at",
        "drug-id",
        "subgroup" as "drug-primary-disease"
    from
        (
        select
            ab."drug-id", ab."subgroup", ab."molecules_count", row_number() over (partition by ab."drug-id"
        order by
            ab."molecules_count" desc,
            ab."subgroup" asc) as "rank"
        from
            (
            select
                a."id" as "drug-id", c."subgroup", count(c."id") as molecules_count
            from
                "prod2-generico".drugs a
            inner join "prod2-generico"."composition-master-molecules-master-mapping" b on
                a."composition-master-id" = b."composition-master-id"
            inner join "prod2-generico"."molecule-master" c on
                b."molecule-master-id" = c."id"
            where
                c.subgroup != 'others'
            group by
                a."id", c."subgroup") ab ) sub
    where
        "rank" = 1
    """
    db.execute(query=query)

    """ committing the transaction """
    db.execute(query=" end; ")


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
