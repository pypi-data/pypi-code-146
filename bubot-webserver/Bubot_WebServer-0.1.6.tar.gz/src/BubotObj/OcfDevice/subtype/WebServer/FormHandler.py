import json
import os.path
import re
from sys import path as syspath

from aiohttp import web


class FormHandler(web.View):
    clear = re.compile('[^a-zA-Z0-9]')
    forms = dict()

    def __init__(self, request):
        web.View.__init__(self, request)
        if not self.forms:
            self.find_forms()

    async def get(self):
        def read_form(path):
            with open(path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    # await asyncio.sleep(1)
                    return web.json_response(data)
                except Exception as e:
                    return web.Response(status=500, text=str(e))

        device = self.request.match_info.get('device')
        obj_name = self.request.match_info.get('obj_name')
        form_name = self.request.match_info.get('form_name')
        subtype = self.request.match_info.get('subtype')

        # берем сначала формы приложения
        if subtype:
            try:
                file_name = self.forms[device][obj_name]['subtype'][subtype][f'{form_name}.form.json']
                return read_form(file_name)
            except KeyError:
                pass

        try:
            file_name = self.forms[device][obj_name][f'{form_name}.form.json']
            return read_form(file_name)
        except KeyError:
            pass

        # если таких нет берем глобальные объектов
        if subtype:
            try:
                file_name = self.forms['root'][obj_name]['subtype'][subtype][f'{form_name}.form.json']
                return read_form(file_name)
            except KeyError:
                pass

        try:
            file_name = self.forms['root'][obj_name][f'{form_name}.form.json']
            return read_form(file_name)
        except KeyError as key:
            return web.HTTPInternalServerError(text=f"Form not found ({key})")

    @classmethod
    def find_forms(cls, **kwargs):
        '''
        Ищем формы для каждого из предустановленных типов, в общем каталог и каталоге устройства
        :param kwargs:
        :return:
        '''

        for path1 in syspath:
            bubot_dir = f'{path1}/BubotObj'
            if not os.path.isdir(bubot_dir):
                continue
            cls._find_in_form_obj_dir(bubot_dir, 'root')
            # device_dir = f'{path1}/bubot/OcfDevice'
            # if not os.path.isdir(device_dir):
            #     continue
            # device_list = os.listdir(device_dir)
            # for device in device_list:
            #     find_in_form_obj_dir(os.path.normpath(f'{device_dir}/{device}'), device)
        a = 1
        pass

    @classmethod
    def _find_in_form_obj_dir(cls, _path, _device=None):
        obj_list = os.listdir(_path)
        for obj_name in obj_list:
            device = (obj_name == 'OcfDevice')

            form_dir = os.path.normpath(f'{_path}/{obj_name}/form')
            if not os.path.isdir(form_dir):
                continue
            cls._find_in_form_dir(obj_name, None, form_dir, 'root')

            form_dir = os.path.normpath(f'{_path}/{obj_name}/subtype')
            if os.path.isdir(form_dir):
                subtypes = os.listdir(form_dir)
                for subtype in subtypes:
                    subtype_form_dir = os.path.normpath(f'{form_dir}/{subtype}/form')
                    if not os.path.isdir(subtype_form_dir):
                        continue
                    cls._find_in_form_dir(obj_name, subtype, subtype_form_dir, subtype if device else _device)

    @classmethod
    def _find_in_form_dir(cls, obj_name, subtype, form_dir, _device=None):
        form_list = os.listdir(form_dir)
        for form_name in form_list:
            if form_name[-5:] != ".json":
                continue

            if _device not in cls.forms:
                cls.forms[_device] = {}
            if obj_name not in cls.forms[_device]:
                cls.forms[_device][obj_name] = {}
            if subtype:
                if 'subtype' not in cls.forms[_device][obj_name]:
                    cls.forms[_device][obj_name]['subtype'] = {}
                if subtype not in cls.forms[_device][obj_name]['subtype']:
                    cls.forms[_device][obj_name]['subtype'][subtype] = {}
                cls.forms[_device][obj_name]['subtype'][subtype][form_name] = os.path.normpath(
                    f'{form_dir}/{form_name}')

            cls.forms[_device][obj_name][form_name] = os.path.normpath(f'{form_dir}/{form_name}')
