from collections import OrderedDict
from enum import Enum
import json
import xmltodict

class MappingFormat(Enum):
    XML = 'xml'
    JSON = 'json'

class SerializableObject:
    
    def to_dict(self, mapping_format: MappingFormat = MappingFormat.XML):
        """
        Convert object to JSON
        """
        # class_dict = {self.xml_mapping.get(k, k): v if not isinstance(v, SerializableObject) else self.xml_mapping[k].to_dict(v) for k, v in self.__dict__.items()}
        
        # ordered dict is required since xs:sequence is ordered
        class_dict = OrderedDict()
        
        if mapping_format == MappingFormat.XML:
            if self.xml_mapping is None:
                raise NotImplementedError(f'xml_mapping is not defined {self.__class__.__name__}')
        if mapping_format == MappingFormat.JSON:
            if self.json_mapping is None:
                raise NotImplementedError(f'json_mapping is not defined {self.__class__.__name__}')

        mapping_to_use = self.xml_mapping.items() if mapping_format == MappingFormat.XML else self.json_mapping.items()
        for k, v in mapping_to_use:
            if k not in self.__dict__ or self.__dict__[k] is None:
                continue

            if isinstance(v, SerializerField) and isinstance(self.__dict__[k], SerializableObject):
                class_dict[v.name] = v.to_dict(self.__dict__[k], mapping_format)
            elif isinstance(v, SerializerList):
                class_dict[v.name] = v.to_dict(self.__dict__[k], mapping_format)
            else:
                class_dict[v.name] = self.__dict__[k]
        return class_dict

        # for k, v in self.__dict__.items():
        #     if k not in self.xml_mapping:
        #         continue
        #     if isinstance(self.xml_mapping[k], SerializerField) and isinstance(v, SerializableObject):
        #         class_dict[self.xml_mapping[k].name] = self.xml_mapping[k].to_dict(v)
        #     elif isinstance(self.xml_mapping[k], SerializerList):
        #         class_dict[self.xml_mapping[k].name] = self.xml_mapping[k].to_dict(v)#v.to_dict(v)
        #     else:
        #         class_dict[self.xml_mapping[k].name] = v
        # return class_dict

    def to_xml(self):
        """
        Convert class to XML
        uses predefined xml_mapping (OrderedDict) to map class attributes to XML elements
        """
        
        if self.xml_mapping is None:
            raise NotImplementedError('xml_mapping is not defined')
        
        # ordered dict is required since xs:sequence is ordered
        json_dict = OrderedDict()
        for k, v in self.xml_mapping.items():
            if k not in self.__dict__ or self.__dict__[k] is None:
                continue

            if isinstance(v, SerializerField) and isinstance(self.__dict__[k], SerializableObject):
                json_dict[v.name] = v.to_dict(self.__dict__[k])
            elif isinstance(v, SerializerList):
                json_dict[v.name] = v.to_dict(self.__dict__[k])
            else:
                json_dict[v.name] = self.__dict__[k]
        return xmltodict.unparse(json_dict, pretty=True, full_document=False)

    def to_json(self):
        """
        Convert class to JSON
        uses predefined json_mapping (OrderedDict) to map class attributes to JSON elements
        """
        if self.json_mapping is None:
            raise NotImplementedError('json_mapping is not defined')
        
        # ordered dict is required since xs:sequence is ordered
        json_dict = OrderedDict()
        for k, v in self.json_mapping.items():
            if k not in self.__dict__ or self.__dict__[k] is None:
                continue

            if isinstance(v, SerializerField) and isinstance(self.__dict__[k], SerializableObject):
                json_dict[v.name] = v.to_dict(self.__dict__[k], mapping_format = MappingFormat.JSON)
            elif isinstance(v, SerializerList):
                json_dict[v.name] = v.to_dict(self.__dict__[k], mapping_format = MappingFormat.JSON)
            else:
                json_dict[v.name] = self.__dict__[k]
        return json_dict

class MappingType(Enum):
    """
    XML mapping type
    """
    List = 'List'
    Field = 'Field'
    Object = 'Object'


class SerializerItem:
    """
    Serializer item
    """
    def __init__(self, name: str, type: MappingType, mapping: str = None, class_type: SerializableObject = None):
        self.name = name
        self.type = type
        self.mapping = mapping
        self.class_type = class_type


class SerializerField(SerializerItem):
    """
    Serializer list
    """
    def __init__(self, name: str ):
        super().__init__(name, MappingType.Field)

    def to_dict(self, object_to_serialize: SerializableObject = None, mapping_format: MappingFormat = MappingFormat.XML):
        """
        Convert field to JSON
        """
        return object_to_serialize.to_dict(mapping_format=mapping_format)


class SerializerList(SerializerItem):
    """
    Serializer list
    """
    def __init__(self, name: str, list_item_name: str = None):
        super().__init__(name, MappingType.List)
        self.list_item_name = list_item_name

    def to_dict(self, list_to_serialize: list[SerializableObject] = None, mapping_format: MappingFormat = MappingFormat.XML):
        """
        Convert list to JSON
        """
        if mapping_format == MappingFormat.XML and self.list_item_name is not None:
            return {self.list_item_name: [item.to_dict(mapping_format=mapping_format) for item in list_to_serialize]}
        if mapping_format == MappingFormat.JSON:
            return [item.to_dict(mapping_format=mapping_format) for item in list_to_serialize]
        