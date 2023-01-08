import websocket, base64
from websocket import create_connection
from random import randbytes


def Websocket(headers: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-WebSocket-Version": "13",
    "Origin": "https://www.piesocket.com",
    "Sec-WebSocket-Extensions": "permessage-deflate",
    "Sec-WebSocket-Key": str(base64.b64encode(randbytes(16)).decode('utf-8')),
    "Connection": "keep-alive, Upgrade",
    "Sec-Fetch-Dest": "websocket",
    "Sec-Fetch-Mode": "websocket",
    "Sec-Fetch-Site": "cross-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade": "websocket"
}) -> websocket.WebSocket:
    """Connects to websocket and returns websocket object

    Parameters:
    headers (dict): Headers to be used to connect to websocket (Optional)

    Returns:
    websocket.WebSocket: A websocket connection connected and already logged in
    """

    return create_connection(
        "wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket",
        suppress_origin=True,
        header=headers
    )
