import os
import logging
import threading
import tempfile
from typing import Tuple
try:
    from spython.main import get_client
    from spython.utils import check_install
    USE_DOCKER = False
    client = get_client(quiet=True)
    if not check_install():
        raise ImportError("Singularity not available")
except ImportError:
    from docker import from_env
    import docker
    USE_DOCKER = True
    client = from_env()

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# Create a temporary directory to hold all the writable parts of the configuration + any
# data stored in the databases. We put this in a special user directory so that all the files
# are self-conained
tmpdir = os.makedirs(os.getcwd() + "/scratch/tmp/", exist_ok=True)
# make sure this exists in the 'scratch' directory
if USE_DOCKER:
    dbdir = "/tmp/"
else:
    dbdir = tempfile.TemporaryDirectory(prefix=os.getcwd() + "/scratch/tmp/")

class Service:
    singularity_container: str
    docker_container: Tuple[str, str]

    @classmethod
    def pull(cls, singularity_filename: str):
        if USE_DOCKER:
            logging.info(f"Pulling contaner: {cls.docker_container}")
            client.images.pull(cls.docker_container[0], tag=cls.docker_container[1])
        elif not os.path.exists(singularity_filename):
            logging.info(f"Pulling contaner: {cls.singularity_container}")
            client.pull(image=cls.singularity_container)
        else:
            logging.info(f"Using existing image: {singularity_filename}")

    @classmethod
    def run(cls):
        raise NotImplementedError

    @classmethod
    def stop(cls, instance):
        client.instance.Instance.stop(f"instance://{instance.name}")


class MongoDB(Service):
    singularity_container = "docker://mongo:latest"
    docker_container = ("mongo", "latest")

    @classmethod
    def run(cls, image_file: str = "/sw/apps/singularity-images/mines_data_engineering/mongo.sif"):
        cls.pull(image_file)
        if USE_DOCKER:
            try:
                return client.containers.get("data-engineering-mongodb")
            except docker.errors.NotFound:
                return client.containers.run(cls.docker_container[0], detach=True, volumes=['tmp:/tmp'], auto_remove=False, name="data-engineering-mongodb")
        else:
            inst = client.instance.instance(image=image_file, options=[f"-B {dbdir.name}:/data/db", f"-B {dbdir.name}:/tmp"], name='data-engineering-mongodb')
            def _run_mongo():
                client.execute(image=f"instance://{inst.name}", command=["mongod"])
            t = threading.Thread(target=_run_mongo)
            t.start()
            return inst


class TimescaleDB(Service):
    singularity_container = "docker://timescale/timescaledb:latest-pg14"
    docker_container = ("timescale/timescaledb", "latest-pg14")

    @classmethod
    def run(cls, image_file: str = "/sw/apps/singularity-images/mines_data_engineering/timescaledb-pg14.sif"):
        cls.pull(image_file)
        if USE_DOCKER:
            try:
                return client.containers.get("data-engineering-timescaledb")
            except docker.errors.NotFound:
                return client.containers.run(cls.docker_container[0], detach=True, auto_remove=False, name="data-engineering-timescaledb")
        else:
            os.environ["POSTGRES_PASSWORD"] = "password"
            inst = client.instance.instance(image=image_file, options=[f"-B {dbdir.name}:/var/lib/postgresql/data", f"-B {dbdir.name}:/var/run/postgresql", f"--env=POSTGRES_PASSWORD"], name='data-engineering-timescaledb')
            def _run_timescale():
                client.execute(image=f"instance://{inst.name}", command=["/usr/local/bin/docker-entrypoint.sh", "postgres"])
            t = threading.Thread(target=_run_timescale)
            t.start()
            return inst
