from wedeliver_core import WeDeliverCore

service_endpoint = dict(
    local='http://localhost:5000',
    development='http://{}-service.services',
    staging='http://{}-service.services',
    sandbox='http://{}-service-sandbox.sandbox',
    production='http://{}-service.services',
)


class ServiceConfig(object):
    name = None
    url = None

    def __init__(self, name):

        self.name = name

    def initialize(self):
        app = WeDeliverCore.get_app()

        url = service_endpoint.get(app.config.get('FLASK_ENV'))

        if url:
            self.url = url.format(self.name.replace('_SERVICE', '').lower())

        return self
