from aiohttp.web import json_response, Response
from Bubot.Core.DeviceLink import DeviceLink
from Bubot.Helpers import Helper


class Resource:
    @staticmethod
    async def action_get_list(request):
        result = dict(
            items=[]
        )
        if not request.query.get('items_only'):
            result['headers'] = [
                {
                    'label': 'Resource',
                    'field': 'title',
                    'name': 'name'
                },
                {
                    'label': 'OcfDevice',
                    'field': 'device',
                    'name': 'device'
                }
            ]
        self = request.app['device']
        if not self.resources:
            self.resources = await self.discovery_resource()
        for di in self.resources:
            device = self.resources[di]
            for href in device.links:
                if href[0:4] == '/oic':
                    continue
                link = device.links[href]
                name = device.name if device.name else device.di
                item = Helper.copy(link.data)
                item['id'] = '{0}{1}'.format(link.anchor, link.href)
                item['title'] = link.name
                item['device']: name
                result['items'].append(item)
        return json_response(result)

    @staticmethod
    async def action_get(request):
        self = request.app['device']
        if not self.resources:
            self.resources = await self.discovery_resource()
        uri = request.query.get('id')
        resource = DeviceLink.get_resource_by_uri(self.resources, uri)
        data = await resource.retrieve(self)
        data['_actions'] = [
            dict(
                id='update',
                icon='save'
            )
        ]
        return json_response(data)

    @staticmethod
    async def action_post(request):
        self = request.app['device']
        data = await request.json()
        data.pop('_actions')
        if not self.resources:
            self.resources = await self.discovery_resource()
        uri = request.query.get('id')
        resource = DeviceLink.get_resource_by_uri(self.resources, uri)
        result = await self.request('update', resource.data, data)
        return Response()

    @staticmethod
    async def action_request(ws, op, to, data):
        self = ws.device
        if not self.resources:
            self.resources = await self.discovery_resource()
        resource = DeviceLink.get_resource_by_uri(self.resources, to)
        result = await self.request(op, resource, data)
        await ws.ws.send_json(result.to_dict())

    @staticmethod
    async def action_observe(ws, to):
        self = ws.device
        if not self.resources:
            self.resources = await self.discovery_resource()
        resource = DeviceLink.get_resource_by_uri(self.resources, to)
        # if resource.observe:
        #     return
        await self.observe(resource, ws.device.on_notify_response)
        resource.observe = True
