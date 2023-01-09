MSGLINK_VERSION = 2

AUTH_REQUEST = 0x00
AUTH_FAIL = 0x01
AUTH_OK = 0x02
PEER_ONLINE = 0x03
PEER_OFFLINE = 0x04
WATCH_ROLE = 0x05
MESSAGE_FULL = 0x06
MESSAGE_PART = 0x07
MESSAGE_END = 0x08
# PUBLISH_FULL = 0x09
# PUBLISH_PART = 0x0A
# PUBLISH_END = 0x0B
SUBSCRIBE = 0x0C
POST_FULL = 0x0D
POST_PART = 0x0E
POST_END = 0x0F
WINDOW_UPDATE = 0x10
HEARTBEAT = 0x11
DROP_BUFFERED = 0x12


MAX_MESSAGE_SIZE = 2**16 - 1
MESSAGE_FULL_MAX_PAYLOAD = MAX_MESSAGE_SIZE - 4 - 2
MESSAGE_PART_MAX_PAYLOAD = MAX_MESSAGE_SIZE - 4 - 2
POST_FULL_MAX_PAYLOAD = MAX_MESSAGE_SIZE - 4 - 32
POST_PART_MAX_PAYLOAD = MAX_MESSAGE_SIZE - 4 - 32


def _enc_str(s: str):
    if len(s) < 128:
        return len(s).to_bytes(1, 'big') + s.encode('utf-8')
    else:
        value = len(s) | (1 << 15)
        return value.to_bytes(2, 'big') + s.encode('utf-8')


def _dec_str(data: bytes, pos: int):
    # if first bit is set, length has 16 bit, else 8 bit
    if data[pos] & (1 << 7):
        str_length = int.from_bytes(data[pos:pos+2], 'big')
        str_length &= ~(1 << 15)  # unset leftmost bit
        pos += 2
    else:
        str_length = int.from_bytes(data[pos:pos+1], 'big')
        pos += 1

    return data[pos:pos+str_length].decode('utf-8'), pos + str_length


def _enc_uint8(i: int):
    return i.to_bytes(1, 'big')


def _dec_uint8(data: bytes, pos: int):
    return int.from_bytes(data[pos:pos+1], 'big'), pos + 1


def _enc_uint16(i: int):
    return i.to_bytes(2, 'big')


def _dec_uint16(data: bytes, pos: int):
    return int.from_bytes(data[pos:pos+2], 'big'), pos + 2


def _enc_uint32(i: int):
    return i.to_bytes(4, 'big')


def _dec_uint32(data, pos):
    return int.from_bytes(data[pos:pos+4], 'big'), pos + 4


def _make_packet(type: int, data: bytes):
    return _enc_uint8(type) + _enc_uint16(len(data)) + data


def encode_auth_request(role: str, password: str, peer_info: str):
    data = _enc_str(role) + _enc_str(password) + _enc_uint16(MSGLINK_VERSION)
    if peer_info is not None and len(peer_info) > 0:
        data += _enc_str(peer_info)
    return _make_packet(AUTH_REQUEST, data)


def encode_watch_role(role: str):
    return _make_packet(WATCH_ROLE, _enc_str(role))


def encode_message_full(receiver: int, channel: int, data: bytes):
    return _make_packet(MESSAGE_FULL, _enc_uint32(receiver) + _enc_uint16(channel) + data)


def encode_message_part(receiver: int, channel: int, data: bytes):
    return _make_packet(MESSAGE_PART, _enc_uint32(receiver) + _enc_uint16(channel) + data)


def encode_message_end(receiver: int, channel: int):
    return _make_packet(MESSAGE_END, _enc_uint32(receiver) + _enc_uint16(channel))


def encode_post_full(topic: bytes, data: bytes):
    return _make_packet(POST_FULL, _enc_uint32(0) + topic + data)


def encode_post_part(topic: bytes, data: bytes):
    return _make_packet(POST_PART, _enc_uint32(0) + topic + data)


def encode_post_end(topic: bytes):
    return _make_packet(POST_END, _enc_uint32(0) + topic)


def encode_subscribe(topic: bytes):
    return _make_packet(SUBSCRIBE, topic)


def encode_window_update(window_update_size: int):
    return _make_packet(WINDOW_UPDATE, _enc_uint32(window_update_size))


def encode_heartbeat():
    return _make_packet(HEARTBEAT, bytes())


def encode_drop_buffered(receiver: int, channel: int):
    return _make_packet(DROP_BUFFERED, _enc_uint32(receiver) + _enc_uint16(channel))


def decode_peer_online(data: bytes):
    peer, pos = _dec_uint32(data, 0)
    role, pos = _dec_str(data, pos)
    info = None
    if pos < len(data):
        info, pos = _dec_str(data, pos)
    return peer, role, info


def decode_peer_offline(data: bytes):
    peer, _ = _dec_uint32(data, 0)
    return peer


def decode_message_full(data: bytes):
    sender, pos = _dec_uint32(data, 0)
    channel, pos = _dec_uint16(data, pos)
    return sender, channel, data[pos:]


def decode_message_part(data: bytes):
    sender, pos = _dec_uint32(data, 0)
    channel, pos = _dec_uint16(data, pos)
    return sender, channel, data[pos:]


def decode_message_end(data: bytes):
    sender, pos = _dec_uint32(data, 0)
    channel, pos = _dec_uint16(data, pos)
    return sender, channel


def decode_post_full(data: bytes):
    sender, pos = _dec_uint32(data, 0)
    topic_id = data[pos:pos+32]
    return sender, bytes(topic_id), data[pos+32:]


def decode_post_part(data: bytes):
    sender, pos = _dec_uint32(data, 0)
    topic_id = data[pos:pos+32]
    return sender, bytes(topic_id), data[pos+32:]


def decode_post_end(data: bytes):
    sender, pos = _dec_uint32(data, 0)
    topic_id = data[pos:pos+32]
    return sender, bytes(topic_id)


def decode_window_update(data: bytes):
    window_update, _ = _dec_uint32(data, 0)
    return window_update


def decode_drop_buffered(data: bytes):
    peer, pos = _dec_uint32(data, 0)
    channel, pos = _dec_uint16(data, pos)
    return peer, channel
