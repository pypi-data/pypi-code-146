from xml.etree import ElementTree as ET
from blockly_executor.core.helpers.xml_serializer import Serializer, ExtException
from blockly_executor import helper


class SapXmlSerializer(Serializer):
    _xmlNodes = ['array', 'object', 'str', 'num', 'bool', 'null']

    def __init__(self, *, name_to_camel_case=False):
        self.name_to_camel_case = name_to_camel_case

    def decode(self, xml):
        try:
            if not xml:
                return
            xml = self.loads(xml)
            result = self.decode_node(xml, None, '')
            return result
        except Exception as err:
            raise ExtException(
                parent=err,
                action='SapXmlSerializer.decode'
            )

    def decode_node(self, node, parent, path, *args):
        try:
            if node.tag not in SapXmlSerializer._xmlNodes:
                raise ExtException(
                    message='decode error',
                    detail=f'Unsupported node type {node.tag} {path}',
                    action='SapXmlSerializer.decode_node'
                )

            name = node.attrib.get('name')
            if self.name_to_camel_case:
                name = helper.to_camel_case(name)
            result = getattr(self, f'decode_{node.tag}')(node, parent, path + '.' + (name if name else node.tag))
            if name:
                parent[name] = result
                return
            return result
        except Exception as err:
            raise ExtException(parent=err, detail=path)

    def decode_object(self, node, parent, path, level=None):
        result = {}
        for elem in node:
            try:
                self.decode_node(elem, result, path)
            except Exception as err:
                raise ExtException(parent=err)
        return result

    def encode(self, data):
        root = self.encode_node(data, None, None, '')
        return ET.tostring(root, encoding="utf-8", method="xml").decode()

    def encode_array(self, node, name, parent, path, level=None):
        if not node:
            return

        for i in range(len(node)):
            self.encode_node(node[i], None, parent, path)

    def encode_object(self, node, name, parent, path, level=None):
        if not node:
            return

        for key in node:
            self.encode_node(node[key], key, parent, path, level)

    def encode_str(self, node, name, parent, path, level=None):
        parent.text = node

    def encode_num(self, node, name, parent, path, level=None):
        parent.text = str(node)

    def encode_bool(self, node, name, parent, path, level=None):
        parent.text = str(1 if node else 0)

    def encode_null(self, node, name, parent, path, level=None):
        pass

    @classmethod
    def convert_params(cls, method_params) -> list:
        """
        Форматирование параметров полученных после выполнения decode для вызова метода БЛ
        Для САП порядок аргументов указывается в имени узла (см. описание метода proxy_xml_1c)
        :param method_params: Параметры метода, полученные при разборе xml
        :type method_params: dict
        :return: Массив аргументов для вызова метода БЛ
        :rtype: list
        """
        if not isinstance(method_params, dict):
            raise TypeError(f'Unexpected type {method_params.__class__.__name__} of method parameters')
        _pre_args = [{'Порядок': int(param_name.split('_')[1]), 'Значение': method_params[param_name]} for param_name in
                     method_params]
        return [_pre_args['Значение'] for _pre_args in sorted(_pre_args, key=lambda x: x['Порядок'])]
