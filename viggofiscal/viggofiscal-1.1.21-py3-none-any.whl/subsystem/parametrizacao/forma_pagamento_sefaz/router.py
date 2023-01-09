from viggocore.common.subsystem import router


class Router(router.Router):

    def __init__(self, collection, routes=[]):
        super().__init__(collection, routes)

    @property
    def routes(self):
        return [
            {
                'action': 'Listar forma_pagamento_sefaz por id',
                'method': 'GET',
                'url': self.resource_url,
                'callback': 'get',
                'bypass': True
            },
            {
                'action': 'Listar forma_pagamento_sefaz',
                'method': 'GET',
                'url': self.collection_url,
                'callback': 'list',
                'bypass': True
            }
        ]
