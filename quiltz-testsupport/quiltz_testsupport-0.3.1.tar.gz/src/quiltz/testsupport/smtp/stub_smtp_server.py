import ssl
from os.path import join, dirname
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP


class TLSController(Controller):
    def __init__(self, handler, hostname, port, tls_context):
        super().__init__(handler=handler, hostname=hostname, port=port)
        self.tls_context = tls_context
        
    def factory(self):
        return SMTP(self.handler, enable_SMTPUTF8=True, tls_context=self.tls_context)


class StubSmtpServer:
    def __init__(self, hostname='localhost', port=9925):
        self.messages = []
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(pem_path('cert'), pem_path('key'))
        self.controller = TLSController(self, hostname=hostname, port=port, tls_context=context)
        self.default_return_value = '250 Message accepted for delivery'
        self.return_values = []

    def send_message_returns(self, *return_values):
        self.return_values = list(return_values)

    async def handle_DATA(self, server, session, envelope):
        data = envelope.content.decode('utf8', errors='replace')
        self.messages.append(data)
        return len(self.return_values) and self.return_values.pop(0) or self.default_return_value

    def start(self):
        self.controller.start()

    def stop(self):
        self.controller.stop()


def pem_path(pem_file):
    return join(dirname(__file__), 'pems', '{}.pem'.format(pem_file))
