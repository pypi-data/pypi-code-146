from aiohttp.web import json_response


class Device:
    @staticmethod
    async def action_get_list(request):
        result = dict(
            items=[]
        )
        if not request.query.get('items_only'):
            result['headers'] = [
                dict(
                    label='Name',
                    field='name',
                    align='left'
                ),
                dict(
                    label='OcfDevice',
                    field='device',
                    align='left'
                ),
                dict(
                    label='Status',
                    field='state',
                    align='left'
                ),
            ]
        self = request.app['device']
        if not self.resources:
            self.resources = await self.discovery_resource()
        for di in self.resources:
            device = self.resources[di]
            await device.retrieve_all(self)
            name = device.name
            device_name = device.get('/oic/d.n', '')
            state = device.get('/oic/mnt.currentMachineState', '')
            result['items'].append(dict(
                id=device.di,
                name=name,
                device=device_name,
                state=state
            ))
        return json_response(result)

    @staticmethod
    async def action_get(request):
        self = request.app['device']
        di = request.query.get('id')
        if not self.resources:
            self.resources = await self.discovery_resource()
        if di not in self.resources:
            raise Exception('device not found')
        result = dict(
            di=di,
            links=self.resources[di].data
        )
        return json_response(result)
