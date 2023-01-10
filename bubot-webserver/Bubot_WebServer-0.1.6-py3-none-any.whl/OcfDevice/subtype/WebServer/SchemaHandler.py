from aiohttp import web
import json
import os.path
import asyncio
import re
import os.path
from sys import path as syspath


class SchemaHandler(web.View):
    clear = re.compile('[^a-zA-Z0-9]')
    schemas = dict()

    def __init__(self, request):
        web.View.__init__(self, request)
        if not self.schemas:
            self.find_schemas()

    async def get(self):
        schema_id = self.request.query.get('id')
        try:
            file_name = self.schemas[schema_id]
        except KeyError:
            return web.HTTPInternalServerError(text=f"Schema not found ({key})")

        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                # await asyncio.sleep(1)
                return web.json_response(data)
            except Exception as e:
                return web.Response(status=500, text=str(e))
        # file_name = './jay/{obj_type}/{obj_name}/form/{form_name}.params.schema.json'.format(
        #     dir=os.path.dirname(__file__),
        #     obj_type=self.obj_type,
        #     obj_name=self.obj_name,
        #     form_name=self.form_name)
        # if os.path.exists(file_name):
        #     with open(file_name, 'r', encoding='utf-8') as file:
        #         data['params'] = json.load(file)
        # file_name = f'./bubot/{obj_name}/schemas/{form_name}.schema.json'
        #
        # if os.path.exists(file_name):
        #     with open(file_name, 'r', encoding='utf-8') as file:
        #         data['schema'] = json.load(file)
        # return web.json_response(data)

    @classmethod
    def find_schemas(cls, **kwargs):
        '''
        Ищем формы для каждого из предустановленных типов, в общем каталог и каталоге устройства
        :param kwargs:
        :return:
        '''

        def find_in_form_dir(_path, _device=None):
            obj_list = os.listdir(_path)
            for obj_name in obj_list:
                schemas_dir = os.path.normpath(f'{_path}/schema')
                if not os.path.isdir(schemas_dir):
                    continue
                schema_list = os.listdir(schemas_dir)
                for schema_name in schema_list:
                    if schema_name[-5:] != ".json":
                        continue

                    cls.schemas[schema_name] = os.path.normpath(f'{schemas_dir}/{schema_name}')

        for path1 in syspath:
            bubot_dir = f'{path1}/BubotObj/ObjSchema'
            if not os.path.isdir(bubot_dir):
                continue
            find_in_form_dir(bubot_dir, 'root')
        pass
