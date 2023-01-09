import logging
import time
from mines_data_engineering.container import MongoDB, TimescaleDB, dbdir

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

_mongo_instance = None
_pg_instance = None

def start_mongo(image_file: str =  "/sw/apps/singularity-images/mines_data_engineering/mongo.sif"):
    """
    Starts MongoDB and returns the connection string
    """
    global _mongo_instance
    if _mongo_instance is not None:
        logging.info("MongoDB is already running!")
        return "mongodb://" + f"{dbdir.name}/mongodb-27017.sock".replace('/', '%2F')

    logging.info("Starting MongoDB")
    _mongo_instance = MongoDB.run(image_file)
    logging.info("Sleeping for 2 seconds to let MongoDB start")
    time.sleep(2)
    return "mongodb://" + f"{dbdir.name}/mongodb-27017.sock".replace('/', '%2F')


def stop_mongo():
    global _mongo_instance
    _mongo_instance.stop()
    _mongo_instance = None


def start_postgres(image_file: str =  "/sw/apps/singularity-images/mines_data_engineering/timescaledb-pg14.sif"):
    """
    Starts Postgres w/ TimescaleDB extension and returns the connection string
    """
    global _pg_instance
    if _pg_instance is not None:
        logging.info("Postgres is already running!")
        return f"user=postgres password=password host={dbdir.name}"
    logging.info("Starting Postgres")
    _pg_instance = TimescaleDB.run(image_file)
    logging.info("Sleeping for 20 seconds to let Postgres start")
    time.sleep(20)
    return f"user=postgres password=password host={dbdir.name}"


def stop_postgres():
    global _pg_instance
    _pg_instance.stop()
    _pg_instance = None
