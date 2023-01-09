from xml.etree import ElementTree as ET
from blockly_executor import ExtException


class Serializer:
    _jsonNodes = {
        list: 'array',
        dict: 'object',
        type(None): 'null',
        int: 'num',
        float: 'num',
        bool: 'bool',
        str: 'str'
    }

    def decode_node(self, node, parent, path, name=''):
        raise NotImplemented()

    def decode_array(self, node, parent, path, *args):
        result = []
        for i in range(len(node)):
            try:
                result.append(self.decode_node(node[i], None, f'{path}.{i}'))
            except Exception as err:
                raise ExtException(parent=err)
        return result

    def decode_str(self, node, *args):
        return node.text

    def decode_num(self, node, *args):
        try:
            return int(node.text)
        except ValueError:
            return float(node.text)

    def decode_bool(self, node, *args):
        try:
            return bool(int(node.text))
        except ValueError:
            return False

    def decode_null(self, *args):
        return None

    def loads(self, xml_str):
        xml_str = xml_str.replace('xmlns="http://www.w3.org/1999/xhtml"', '', 1)
        result = ET.fromstring(xml_str)
        return result

    def encode_node(self, node, name, parent, path, level=None):
        node_type = type(node)

        if node_type not in self._jsonNodes:
            return

        node_type = self._jsonNodes[node_type]
        if parent is None:
            elem = ET.Element(node_type)
        else:
            elem = ET.SubElement(parent, node_type)

        if name:
            elem.set('name', name)
        handler_name = f'encode_{node_type}'
        if not getattr(self, handler_name):
            raise ExtException(
                'encode error',
                detail=f'Not supported node "{node_type}", path: {path}',
                action='XdtoSerializer.encodeNode'
            )
        getattr(self, handler_name)(node, name, elem, path + '.' + name if name else node_type[0], level)
        return elem

