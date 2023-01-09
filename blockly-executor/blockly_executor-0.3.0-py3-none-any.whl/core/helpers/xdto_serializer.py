from xml.etree import ElementTree as ET
from blockly_executor.core.helpers.xml_serializer import Serializer
from blockly_executor import ExtException


class XdtoSerializer(Serializer):
    # _amp = new RegExp("&", 'g')
    xmlDoc = None
    ns_xsi = 'http://www.w3.org/2001/XMLSchema-instance'
    dp1NS = {}
    # _xmlNodes = ['ValueTable', 'Value', 'Array', 'ValueType', 'Type', '']
    _xsiTypes = {
        'Structure': 'structure',
        'ValueTable': 'table',
        'Map': 'map',
        'Array': 'array',
        'Null': 'null',
        'string': 'str',
        'decimal': 'num',
        'boolean': 'bool',
        'dateTime': 'str'
    }

    def decode(self, xml_str):
        try:
            if not xml_str:
                return
            xml = self.loads(xml_str)
            result = self.decode_node(xml, None, '', '')
            return result
        except Exception as err:
            raise ExtException(
                parent=err,
                action='XdtoSerializer.decode'
            )

    def decode_node(self, node, parent, path, name=''):
        try:
            xsi_type = node.get(f'{{{self.ns_xsi}}}type')
            if not xsi_type:
                if not path:
                    xsi_type = node.tag  # корневой тэг идент без типа
                elif node.get(f'{{{self.ns_xsi}}}nil'):
                    return None
            if xsi_type:
                xsi_type = xsi_type.split(':')
                xsi_type = xsi_type[len(xsi_type) - 1]
                xsi_type = xsi_type.split('.')
                xsi_type = xsi_type[0]
                if xsi_type not in self._xsiTypes:
                    if xsi_type[-3:] == 'Ref':
                        nodeType = 'ref'
                    else:
                        raise ExtException(
                            message='decode Exception',
                            detail=f'Not supported xsi:type {xsi_type} {path}',
                            action='XdtoSerializer.decode_node'
                        )
                else:
                    nodeType = XdtoSerializer._xsiTypes[xsi_type]
            else:
                try:
                    # .replace('{http://v8.1c.ru/8.1/data/core}', '')
                    nodeType = XdtoSerializer._xsiTypes[node.tag]
                except KeyError:
                    nodeType = 'simple_node'
            # raise Exception("Not supported node: " + node.tag + ", path:" + path + ", content:" + node.text + ",")
            decoder = 'decode_' + nodeType
            if hasattr(self, decoder):
                return getattr(self, decoder)(node, parent, f'{path}.{xsi_type if xsi_type else node.tag}', name)
            else:
                raise ExtException(
                    message='decode Exception',
                    detail=f'Not supported node type {nodeType} {path}',
                    action='XdtoSerializer.decode_node'
                )
        except Exception as err:
            raise ExtException(parent=err, detail=path) from err

    def decode_structure(self, node, parent, path, name):
        try:
            result = {}
            for i in range(len(node)):
                try:
                    prop = node[i]
                    if prop.tag == 'Property':
                        prop_name = prop.get('name')
                        result[prop_name] = self.decode_node(prop[0], result, path, prop_name)
                    else:
                        raise ExtException(message="'not support node name in structure {prop.tag} {path}")
                except Exception as err:
                    raise ExtException(parent=err)
            return result
        except Exception as err:
            raise ExtException(parent=err)

    def decode_map(self, node, parent, path, name):
        try:
            result = {}
            for i in range(len(node)):
                try:
                    pair = node[i]
                    pair_key = self.decode_node(pair[0], result, f'{path}.pairKey{i}', 'MapKey')
                    result[pair_key] = self.decode_node(pair[1], result, f'{path}.pairValue{i}', 'MapValue')
                except Exception as err:
                    raise ExtException(parent=err)
            return result
        except Exception as err:
            raise ExtException(parent=err)

    # def decode_Value(self, node, parent, path, name):
    #     try:
    #         # xsyType = node.attrib.get('xsi:type')
    #         if node.tag not in XdtoSerializer._xsiTypes:
    #             raise Exception(f"Unsupported node type {node.tag} {path}")
    #         node_type = XdtoSerializer._xsiTypes[node.tag]
    #         return getattr(self, 'decode_value_' + node_type)(node, parent, path)
    #     except Exception as err:
    #         raise ExtException(parent=err)

    def decode_table(self, node, parent, path, name):
        try:
            result = []
            index = []
            for i in range(len(node)):
                try:
                    item = node[i]
                    if item.tag == 'row':
                        result.append(self.decode_table_row(node[i], result, "{path}.{i}", index))
                    elif item.tag == 'column':
                        index.append(self.decode_simple_node(node[i], None, path, None))
                    else:
                        raise ExtException(message=f"not support node name in table {item.tag}")
                except Exception as err:
                    raise ExtException(parent=err)
            return result
        except Exception as err:
            raise ExtException(parent=err)

    def decode_simple_node(self, node, parent, path, name):
        try:
            # result = parent ? parent : {}
            _result = None
            count_child = len(node)
            if count_child:  # != Node.TEXT_NODE
                _result = {}
                for i in range(count_child):
                    tag = node[i].tag
                    value = self.decode_node(node[i], None, path, tag)
                    if tag in _result:
                        if not isinstance(_result[tag], list):
                            _result[tag] = [_result[tag]]
                        _result[tag].append(value)
                    else:
                        _result[tag] = value
            else:
                _result = node.text
            return _result
        except Exception as err:
            raise ExtException(parent=err)

    def decode_table_row(self, node, parent, path, index):
        try:
            result = {}
            for i in range(len(node)):
                try:
                    _tag = index[i]['Name']
                    result[_tag] = self.decode_node(node[i], result, "{path}.{_tag}", _tag)
                except Exception as err:
                    raise ExtException(parent=err)
            return result
        except Exception as err:
            raise ExtException(parent=err)

    def decode_ref(self, node, parent, path, name):
        try:
            # xsiType = node.attrib.get('xsi:type').split(':')[1]
            objType = node.get(f'{{{self.ns_xsi}}}type').split(':')[1].split('.')
            if name == 'uid':
                parent['uid.xsi:ИмяИС'] = objType[1]
                parent['uid.xsi:ТипИС'] = objType[0]
                return node.text
            else:
                return {
                    'ИдИС': node.text,
                    'ИмяИС': objType[1],
                    'ТипИС': objType[0]
                }
        except Exception as err:
            raise ExtException(parent=err)

    def decode_bool(self, node, *args):
        return True if node.text == 'true' else False

    def encode(self, data):
        # xml = self.loads('<?xml version="1.0" encoding="UTF-8"?>')
        self.dp1NS = {}
        try:
            root = self.encode_node(data, None, None, '', 1)
            # root.setNS('http:#www.w3.org/2000/xmlns/', 'xmlns:xsi', 'http:#www.w3.org/2001/XMLSchema-instance')
            # root.setNS('http:#www.w3.org/2000/xmlns/','xmlns:xs', 'http:#www.w3.org/2001/XMLSchema')
            # root.set('xmlns', 'http:#v8.1c.ru/8.1/data/core')
            xml_string = ET.tostring(root, encoding="utf-8", method="xml").decode()
            # xmlString = XMLSerializer().serializeToString(root)
            # 1C нужен namespace xs для контроля значений, добавить его другими способами кроме как заменой строки одинаково для всех браузеров не вышло.
            newNS = "xmlns=\"http://v8.1c.ru/8.1/data/core\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
            # for level in self.dp1NS:
            #     if level in self.dp1NS:
            #         newNS += " xmlns:d{level}p1=\"http:#v8.1c.ru/8.1/data/enterprise/current-config\""
            result = xml_string.replace("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"", newNS)
            return result
            # return xml_string
        except Exception as err:
            raise ExtException(parent=err, action='XdtoSerializer.encode', dump={data})

    def encode_node(self, node, name, parent, path, level=None):
        try:
            node_type = type(node)

            if node_type not in self._jsonNodes:
                return

            node_type = self._jsonNodes[node_type]

            handler_name = f'encode_{node_type}'
            if not getattr(self, handler_name):
                raise ExtException(
                    message='encode error',
                    detail=f'Not supported node "{node_type}", path: {path}',
                    action='XdtoSerializer.encodeNode'
                )
            return getattr(self, handler_name)(node, name, parent, path + '.' + name if name else '', level)
        except Exception as err:
            raise ExtException(parent=err, detail=path, dump={'path': path})

    def encode_object_old(self, node, name, parent, path, level):  # to stricture
        try:
            if self.is_ref(node):  # объект содержащий ссылку
                return self.encode_ref(node, name, parent, path, level)
            else:
                if parent is None:
                    elem = ET.Element('Structure')
                    elem.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
                else:
                    elem = ET.SubElement(parent, name)
                elem.set('xsi:type', 'Structure')

                for key in node:
                    prop = ET.SubElement(elem, "Property")
                    prop.set('name', key)
                    self.encode_node(node[key], 'Value', prop, path, level + 2)
            return elem
        except Exception as err:
            raise ExtException(parent=err)

    @staticmethod
    def is_ref(node):
        return 'ТипИС' in node and 'ИмяИС' in node and 'ИдИС' in node

    def encode_object(self, node, name, parent, path, level):  # to map
        try:
            if self.is_ref(node):  # объект содержащий ссылку
                return self.encode_ref(node, name, parent, path, level)
            else:
                if parent is None:
                    elem = ET.Element('Map')
                    elem.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
                else:
                    elem = ET.SubElement(parent, name)
                elem.set('xsi:type', 'Map')

                for key in node:
                    pair = ET.SubElement(elem, "pair")
                    pair_key = ET.SubElement(pair, "Key")
                    pair_key.set('xsi:type', 'string')
                    pair_key.text = key
                    self.encode_node(node[key], 'Value', pair, path, level + 2)
            return elem
        except Exception as err:
            raise ExtException(parent=err)

    def encode_array(self, node, name, parent, path, level):
        try:
            if parent is None:
                elem = ET.Element('Structure')
                elem.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
            else:
                elem = ET.SubElement(parent, name)
            elem.set('xsi:type', 'Array')
            for i in range(len(node)):
                self.encode_node(node[i], 'Value', elem, path, level + 2)
            return elem
        except Exception as err:
            raise ExtException(parent=err)

    def encode_ref(self, node, name, parent, path, level):
        try:
            # level -= 1
            elem = ET.SubElement(parent, name)
            xsiLevel = f"d{level}p1"
            xsiType = f"{xsiLevel}:{node['ТипИС']}.{node['ИмяИС']}"
            self.dp1NS[level] = True
            elem.set('xsi:type', xsiType)
            elem.set(f'xmlns:{xsiLevel}', "http://v8.1c.ru/8.1/data/enterprise/current-config")
            elem.text = node['ИдИС']
            return elem
        except Exception as err:
            raise ExtException(parent=err)

    def encode_str(self, node, name, parent, *args):
        try:
            elem = ET.SubElement(parent, name)
            elem.set('xsi:type', 'xs:string')
            elem.text = node
            return elem
        except Exception as err:
            raise ExtException(parent=err)

    def encode_num(self, node, name, parent, *args):
        try:
            elem = ET.SubElement(parent, name)
            elem.set('xsi:type', 'xs:decimal')
            elem.text = str(node)
            return elem
        except Exception as err:
            raise ExtException(parent=err)

    def encode_bool(self, node, name, parent, *args):
        try:
            elem = ET.SubElement(parent, name)
            elem.set('xsi:type', 'xs:boolean')
            elem.text = 'true' if node else 'false'
            return elem
        except Exception as err:
            raise ExtException(parent=err)

    def encode_null(self, node, name, parent, *args):
        try:
            elem = ET.SubElement(parent, name)
            elem.set('xsi:type', 'Null')
            return elem
        except Exception as err:
            raise ExtException(parent=err)

    def loads(self, xml_str):
        xml_str = xml_str.replace('xmlns="http://v8.1c.ru/8.1/data/core"', '', 1)
        result = ET.fromstring(xml_str)
        return result

    @classmethod
    def convert_params(cls, method_params) -> list:
        """
        Форматирование параметров полученных после выполнения decode для вызова метода БЛ
        :param method_params: Параметры метода, полученные при разборе xml
        :type method_params: dict, list
        :return: Массив аргументов для вызова метода БЛ
        :rtype: list
        """
        return method_params if isinstance(method_params, list) else [method_params]
