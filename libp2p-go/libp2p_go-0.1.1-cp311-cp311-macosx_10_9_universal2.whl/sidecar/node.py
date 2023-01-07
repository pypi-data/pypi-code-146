import asyncio
from libp2p import *
from libp2p.data_store import MapDataStore, MutexDataStore
from libp2p.dht import *
from libp2p.peer import AddrInfo
from libp2p.routed_host import RoutedHost


async def boring_protocol(s: Stream):
    print(f"收到流会话: {s.id}, {s.protocol}")
    await s.close()
    print(f"关闭会话")


asyncio.set_event_loop(asyncio.new_event_loop())
host = Host(ListenAddrStrings(f"/ip4/0.0.0.0/udp/0/quic-v1"))
data_store = MapDataStore()
mutex_data_store = MutexDataStore(data_store)
dht = DHT.new(host, Mode(DhtModeEnum.ModeAutoServer), DataStore(mutex_data_store))
host = RoutedHost(host, dht)
host.set_stream_handler("boring/1.0.0", boring_protocol)
dht.bootstrap()


async def read_line(p="") -> str:
    return await asyncio.get_event_loop().run_in_executor(None, input, p)


async def show_node_info():
    print(f"HostID: {host.id()}")
    print("addrs:")
    for addr in host.addrs():
        print(f"* {addr}")
    print("peers:", *host.peer_store.peer_with_addrs())


async def add_peer():
    peer_id = await read_line("peerId:")
    addr = await read_line("addr:")
    host.peer_store.add_addr(peer_id, addr, PeerStore.PermanentAddrTTL)


async def connect():
    peer_id = await read_line("peerId:")
    try:
        addrs = host.peer_store.addrs(peer_id)
        assert addrs
        info = AddrInfo(peer_id=peer_id, addrs=addrs)
        await host.connect(info)
        print("连接成功")
    except Exception as e:
        print(f"connect failed: {e}")


async def new_stream():
    peer_id = await read_line("peerId:")
    protocol_id = await read_line("protocolId:")
    try:
        s = await host.new_stream(peer_id, protocol_id)
        print("获取成功")
        await s.close()
        print("关闭成功")
    except Exception as e:
        print(f"new_stream failed: {e}")


async def loop():
    await show_node_info()
    while True:
        print("""
        1) 节点信息
        2) 加入节点信息 addAddr
        3) 连接节点 connect
        4) 获取流 new_stream
        0) 退出
        """)
        try:
            n = int(await read_line())
            match n:
                case 1:
                    await show_node_info()
                case 2:
                    await add_peer()
                case 3:
                    await connect()
                case 4:
                    await new_stream()
                case 0:
                    break
                case _:
                    await show_node_info()
        except Exception as e:
            pass


asyncio.get_event_loop().run_until_complete(loop())

