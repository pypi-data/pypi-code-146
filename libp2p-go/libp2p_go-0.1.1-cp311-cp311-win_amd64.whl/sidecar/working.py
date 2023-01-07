import json
import pprint
import struct
import asyncio
import argparse
import datetime
from libp2p import *
from libp2p.crypto import *
from libp2p.data_store import *
from libp2p.dht import *
from libp2p.mdns import *
from libp2p.peer import *
from libp2p.routed_host import *
from libp2p.pubsub import *


parser = argparse.ArgumentParser(
            description="workingNode",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
parser.add_argument("-l", type=int, default=0, help="listening port")
config = vars(parser.parse_args())
port = config.get('l')
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
addr = f"/ip4/0.0.0.0/udp/{port}/quic-v1"
sk, pk = crypto_generate_keypair_with_reader(KeyType.RSA, 2048, 0)

host = Host(
    ListenAddrStrings(addr),
    Identity(sk),
    SecurityNoise(),
    SecurityTls(),
    #PrivateNetwork(b'12345678901234567890123456789023'),
    loop=loop,
)
data_store = MapDataStore()
mutex_data_store = MutexDataStore(data_store)
dht = DHT.new(host, DataStore(mutex_data_store), Mode(DhtModeEnum.ModeAutoServer))
host = RoutedHost(host, dht)


async def new_peer(addr_info: AddrInfo):
    if addr_info.id == host.id():
        return
    print(f"mdns new peer: {addr_info}")
    try:
        await host.connect(addr_info)
        print(f"new peer {addr_info} connected")
    except Exception as e:
        print(f"new peer connect failed: {e}")

mdns = MdnsService(host, "_cluster", new_peer)
mdns.start()

# ps = PubSub.new_gossip(host)


async def sender(topic: Topic):
    peer_id = host.id()
    while True:
        await asyncio.sleep(5)
        s = f"I'm *{peer_id[-6:]} say hi at {datetime.datetime.now()}"
        await topic.publish(s.encode('utf8'))


async def pubsub(gossip: PubSub):
    topic = await gossip.join("SVC-0987")
    sub = await topic.subscription()
    sender_task = asyncio.create_task(sender(topic))
    try:
        async for msg in sub:
            msg: LibP2PMessage = msg
            if msg.from_peer == host.id():
                continue
            print(msg)
    finally:
        sender_task.cancel()
        await topic.close()
        await host.close()


class Node:
    def __init__(self, service_id: str, host: Host):
        self.service_id = service_id
        self.host = host
        self.host_id = host.id()
        self.service_ps = PubSub.new_gossip(host)
        self.leaders = list()
        self.is_leader = False
        self.leader_term = 1
        self.is_ready = False

        self.topic: Topic = None
        self.subscription: Subscription = None

        self.leader_task: asyncio.Task = None

    async def read_stream(self, stream: Stream):
        _, len_bytes = await stream.read_bytes(4)
        length: int = struct.unpack(">L", len_bytes)[0]
        _, msg_bytes = await stream.read_bytes(length)
        return json.loads(msg_bytes)

    async def write_stream(self, stream: Stream, d: dict):
        msg_bytes = json.dumps(d).encode('utf8')
        len_bytes = struct.pack(">L", len(msg_bytes))
        await stream.write(len_bytes)
        await stream.write(msg_bytes)

    async def leader_handler(self, stream: Stream):
        m = await self.read_stream(stream=stream)

    async def worker_handler(self, stream: Stream):
        pass

    async def wait_service_leader(self):
        try:
            sub = self.subscription
            async for msg in sub:
                msg: LibP2PMessage = msg
                if msg.from_peer == self.host_id:
                    continue
                msg: dict = json.loads(msg.data)
                svc_id = msg.get("serviceId")
                if svc_id != self.service_id:
                    continue
                leaders = msg.get("leaders", list())
                if not leaders:
                    continue
                self.leaders = leaders
                print("found current leaders", leaders)
                return True
        except asyncio.CancelledError:
            print("wait leader canceled")

    async def leader_publish_loop(self):
        while True:
            await asyncio.sleep(5)
            if not self.is_leader:
                continue
            msg = {
                "type": "borderPing",
                "version": "v1",
                "serviceId": self.service_id,
                "leaders": self.leaders,
                "members": 1,
                "term": self.leader_term,
            }
            await self.topic.publish(json.dumps(msg).encode('utf8'))

    async def chaoyang_masses(self):
        pass

    async def read_message(self):
        sub = self.subscription
        async for msg in sub:
            msg: LibP2PMessage = msg
            if msg.from_peer == self.host_id:
                continue
            msg: dict = json.loads(msg.data)
            pprint.pprint(msg)

    async def bootstrap(self):
        topic = await self.service_ps.join(self.service_id)
        self.topic = topic
        self.leader_task = asyncio.create_task(self.leader_publish_loop())
        sub = await topic.subscription()
        self.subscription = sub
        try:
            ok = await asyncio.wait_for(self.wait_service_leader(), timeout=10)
            if not ok:
                raise asyncio.TimeoutError
            self.is_leader = False
            self.is_ready = False
        except asyncio.TimeoutError:
            print("current node is leader")
            self.is_leader = True
            self.leader_term = 1
            self.is_ready = True
            self.leaders = [
                {
                    "peerId": self.host_id,
                    "addrs": self.host.addrs(),
                }
            ]

    async def run(self):
        await self.bootstrap()
        await self.read_message()


try:
    node = Node("SVC-0987", host)
    asyncio.get_event_loop().run_until_complete(node.run())
except KeyboardInterrupt:
    asyncio.get_event_loop().close()
