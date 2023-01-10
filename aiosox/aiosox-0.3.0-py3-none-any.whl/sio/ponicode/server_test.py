import pytest

from aiosox.sio import server


class Test_Socketioserver_Register_namespace:
    @pytest.fixture()
    def socketioserver(self):
        return server.SocketIoServer()

    def test_register_namespace_1(self, socketioserver):
        socketioserver.register_namespace()
