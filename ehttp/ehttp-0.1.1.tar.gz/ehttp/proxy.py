"""класс содержит метод для быстрого проксирования трафика с помощью библиотеки requests."""
from .server import Server
from .classes import Request

try:
    import requests
except ImportError:
    pass


def proxy(address="http://localhost:80", host="0.0.0.0", port=3000, force_bind=False):
    """Метод для проксирования

    Args:
        address (str, optional): адресс удаленного сервера. Defaults to "http://localhost:80"
        host (str, optional): адресс для прослушивания. Defaults to "0.0.0.0"
        port (int, optional): порт для прослушивания. Defaults to 3000
        force_bind (bool, optional): принудительно освобождать порт. Defaults to False
    """
    address = address[:-1] if address.endswith("/") else address
    server = Server(host, port, force_bind)

    @server.bind("(.*)")
    def _(req: Request, path):
        return requests.request(
            req.method, address+path,
            headers=req.headers, data=req.raw_data,
            timeout=20
        )
    server.start()
