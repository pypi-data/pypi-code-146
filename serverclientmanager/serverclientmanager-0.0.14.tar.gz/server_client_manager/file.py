from socket import socket
from pathlib import Path

from .data import Data


data = Data()


def close_connection(socket: socket) -> None:
    socket.send(data.CLOSE_CONNECTION)
    socket.recv(data.SYNC_LENGTH)
    socket.close()


def send_authentication(socket: socket, password=str, send_request_type=True) -> None:
    if send_request_type:
        socket.send(data.SEND_AUTHENTICATION.encode())
        socket.recv(data.SYNC_LENGTH)
    socket.send(len(password.encode()).to_bytes(data.SEND_INT, "little", signed=False))
    socket.recv(data.SYNC_LENGTH)
    socket.send(password.encode())
    socket.recv(data.SYNC_LENGTH)


def recv_authentication(socket: socket) -> str:
    password_lenght = int.from_bytes(socket.recv(data.SEND_INT), "little", signed=False)
    socket.send(data.SYNC)
    password = socket.recv(password_lenght).decode()
    socket.send(data.SYNC)
    return password


def send_file(
    socket: socket, path: Path, send_path=True, send_request_type=True
) -> None:
    # type of request
    if send_request_type:
        socket.send(data.SEND_FILE)
        socket.recv(data.SYNC_LENGTH)
    # path
    if send_path:
        socket.send(len(str(path).encode()).to_bytes(2, "little", signed=False))
        socket.recv(data.SYNC_LENGTH)
        socket.send(str(path).encode())
        socket.recv(data.SYNC_LENGTH)
    # file size
    socket.send(
        path.stat().st_size.to_bytes(data.SEND_INT_LONG, "little", signed=False)
    )
    socket.recv(data.SYNC_LENGTH)
    # file
    with open(path, "rb") as f:
        for _ in range(0, path.stat().st_size, data.BUFFER_SIZE):
            socket.send(f.read(data.BUFFER_SIZE))
            socket.recv(data.SYNC_LENGTH)
    socket.recv(data.SYNC_LENGTH)


def recv_file(socket: socket, path: str = None) -> None:
    if path is not None:
        path_lenght = int.from_bytes(socket.recv(data.SEND_INT), "little", signed=False)
        socket.send(data.SYNC)
        path = socket.recv(path_lenght).decode()
        socket.send(data.SYNC)
    size = int.from_bytes(socket.recv(data.SEND_INT_LONG), "little", signed=False)
    socket.send(data.SYNC)
    with open(path, "wb") as f:
        for _ in range(0, size, data.BUFFER_SIZE):
            f.write(socket.recv(data.BUFFER_SIZE))
            socket.send(data.SYNC)


# def handle_request(
#     socket: socket,
#     need_authorization: bool = True,
#     pre_handle: function = empty,
#     post_handle: function = empty,
# ):
#     authorized = False
#     while True:
#         request = socket.recv().encode()
#         socket.send(data.SYNC_LENGTH)
#         pre_handle(request)
#         if request == data.CLOSE_CONNECTION:
#             socket.close()
#         elif request == data.SEND_AUTHENTICATION:
#             recv_authentication(socket)
#         elif request == data.SEND_FILE:
#             recv_file(socket)
#         post_handle(request)
