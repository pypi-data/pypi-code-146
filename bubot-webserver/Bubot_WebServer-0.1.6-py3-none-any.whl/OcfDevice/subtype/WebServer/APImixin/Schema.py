from aiohttp.web import json_response


class Schema:

    @staticmethod
    async def action_get(request):
        self = request.app['device']
        return json_response(self.get_schema_by_rt(request.query.get('id').split('+')))
