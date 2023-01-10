from aiohttp.web import json_response


class Driver:
    @staticmethod
    async def action_get_list(request):
        if not request.query.get('items_only'):
            result = dict(
                items=[],
                headers=[
                    dict(
                        label='Id',
                        field='id'
                    ),
                    dict(
                        label='Name',
                        field='name'
                    ),
                    dict(
                        label='',
                        field='_actions',
                        align='right',
                        sortable=False
                    )
                ],
            )
        else:
            result = dict(
                items=[]
            )
        self = request.app['device']

        for name in self.drivers:
            try:
                # if self.drivers[name].get('data') is None:
                driver = self.init_from_config(class_name=name)
                    # self.drivers[name]['handler'] = _device
                result['items'].append(dict(
                    id=name,
                    name=name,
                    links=driver.data,
                    _actions=driver.get_install_actions()
                ))
            except Exception as e:
                pass

        return json_response(result)

    @staticmethod
    async def action_get(request):
        self = request.app['device']
        name = request.query.get('id')
        driver = self.init_from_config(class_name=name)
        return json_response(dict(
            id=name,
            links=driver.data,
            _actions=driver.get_install_actions()
        ))

    @staticmethod
    async def action_post_add_device(request):
        self = request.app['device']
        data = await request.json()
        class_name = data.pop('id')
        new_device = self.init_from_config(data['links'], class_name=class_name)
        new_device.save_config()
        di = new_device.get_device_id()
        await self.action_add_device(dict(di=di, dmno=class_name))
        return json_response({})
