
import os
from mongoengine import connect
from mongoengine.document import Document
from mongoengine.fields import FloatField, ListField, LongField, StringField
import time
import requests
import random
import uuid
import pybo.util as util


mongo_ip = util.get_mysql_ip()
if mongo_ip is None:
    mongo_ip = "127.0.0.1"

# mongo_addr = os.getenv('MONGO_ADDR', 'mongodb://' + mongo_ip + ':27017/db?authSource=admin')
mongo_addr = 'mongodb://' + mongo_ip + ':27017'
# mongo_addr = 'mongodb://172.22.176.1:27017'
connect(db='test', host=mongo_addr)


def get_mongo_ip():
    return mongo_addr


class Stations(Document):
    place_id = StringField(required=True)
    lat = FloatField(required=True)
    lan = FloatField(required=True)
    bus = ListField(StringField(max_length=10))


def create_random_station():
    place_id = f'stop-{uuid.uuid4()}'
    bus = [str(random.randint(1000, 2000)) for _ in range(random.randint(5, 10))]
    station = Stations(
        place_id=place_id,
        lat=37 + random.random(),
        lan=127 + random.random(),
        bus=bus,
    )

    station.save()
    return station


def get_station(station_id: str):
    return Stations.objects.get(place_id=station_id)


def get_eta(station: Stations):
    eta = cache.get_eta(station.place_id)
    if eta is None:
        time.sleep(random.random() * 2 + 3)
        with open('/dev/random', 'rb') as f:
            for _ in range(random.randint(10, 20)):
                f.read(1)
        eta = random.randint(100, 3000)
        cache.set_eta(station.place_id, eta)

        return eta
    else:
        return int(eta.decode('utf-8'))


def geocoding(station: Stations):
    requests.get(f'https://httpbin.org/delay/{random.randint(1, 10)}')
    return 'Seoul Korea'
