from aiohttp.web import json_response


class Store:
    @staticmethod
    async def api_store_get(request):
        return json_response(
            {
                'menu': [
                    dict(
                        path='/resources',
                        name='Resources',
                        icon='build',
                        component='Browser',
                        props=dict(name='resource')
                    ),
                    dict(
                        path='/OcfDriver',
                        name='Devices',
                        icon='build',
                        component='Browser',
                        props=dict(name='device')
                    ),
                    dict(
                        path='/drivers',
                        name='Drivers',
                        icon='build',
                        component='Browser',
                        props=dict(name='driver')
                    )
                ]
            }
        )

    @staticmethod
    async def action_get(request):
        self = request.app['device']
        return json_response(self.get_schema_by_rt(request.query.get('id').split('+')))
