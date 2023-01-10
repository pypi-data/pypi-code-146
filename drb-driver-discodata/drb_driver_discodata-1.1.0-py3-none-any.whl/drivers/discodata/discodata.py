import io

from drb.core import DrbNode, ParsedPath, DrbFactory
from drb.drivers.http import DrbHttpNode
from drb.exceptions.core import DrbException, \
    DrbNotImplementationException, DrbFactoryException
from drb.nodes.abstract_node import AbstractNode
from requests.auth import AuthBase
from typing import Optional, List, Union, Any, Dict, Tuple
from drb.topics.resolver import create

from drb.drivers.json import JsonBaseNode


class DrbDiscodataRowList(list):

    def __init__(self, table: DrbNode):
        super().__init__()
        self._skip = 0
        self._page_size = -1
        self._table = table
        self._page = None
        self._count_page = None
        self._page_size = None
        self._count = -1

    def __perform_query(self, num_page):
        rep_json = self._table.get_elts(num_page)
        if rep_json is None:
            return []
        rep_json = rep_json[0]
        self._page = [e for e in rep_json if e.name == 'Rows']
        return self._page

    def __init_query(self):
        rep_json = self._table.get_elts(0)
        if rep_json is None:
            return []
        rep_json = rep_json[0]
        self._count = rep_json['TotalRows'].value
        self._count_page = rep_json['NumPages'].value

        self._page = [e for e in rep_json if e.name == 'Rows']
        self._page_size = len(self._page)

        self._page_size = len(self._page)
        return self._page

    def __compute_index(self, item: Union[int, slice]) -> Tuple[int, int]:
        if isinstance(item, int):
            if item < 0:
                return item + len(self), -1
            return item, -1
        # item is a slice
        start = item.start if item.start is not None else 0
        if start < 0:
            start = start + len(self)
        stop = item.stop if item.stop is not None else len(self)
        if stop < 0:
            stop = stop + len(self)
        return start, stop

    def append(self, obj: Any) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def copy(self) -> List[DrbNode]:
        raise NotImplementedError

    def count(self, value: Any) -> int:
        raise NotImplementedError

    def index(self, value: Any, start: int = ..., stop: int = ...) -> int:
        raise NotImplementedError

    def insert(self, index: int, obj: DrbNode) -> None:
        raise NotImplementedError

    def pop(self, index: int = ...):
        raise NotImplementedError

    def remove(self, value: Any) -> None:
        raise NotImplementedError

    def reverse(self) -> None:
        raise NotImplementedError

    def sort(self: List, *, key: None = ..., reverse: bool = ...) -> None:
        raise NotImplementedError

    def __getitem_index(self, index):
        if index not in range(self._skip, self._skip + self._page_size):
            page_number = index // self._page_size
            self._skip = page_number * self._page_size
            self.__perform_query(page_number)
        return self._page[index % self._page_size]

    def __getitem__(self, item):
        if self._count == -1:
            self.__init_query()

        if isinstance(item, int):
            index, _ = self.__compute_index(item)
            return self.__getitem_index(index)
        elif isinstance(item, slice):
            start, stop = self.__compute_index(item)
            result = []
            for index in range(start, stop):
                node = self.__getitem_index(index)
                result.append(node)
            return result
        else:
            raise KeyError(f'Invalid key: {type(item)}')

    def __iter__(self):
        def generator(count, page_size):
            page_num = 1
            buffer = None
            for i in range(count):
                if i % page_size == 0:
                    rep = self._table.get_elts(page_num)
                    if rep is None:
                        return None
                    elts = rep[0]
                    buffer = [e for e in elts if e.name == 'Rows']
                    page_num += 1
                idx = i % page_size
                yield buffer[idx]

        return generator(len(self), self._page_size)

    def __len__(self):
        if self._count == -1:
            self.__init_query()
        return self._count

    def __contains__(self, item):
        raise NotImplementedError

    def __iadd__(self, other):
        raise NotImplementedError

    def __imul__(self, other):
        raise NotImplementedError


class DrbDiscodataTableNode(AbstractNode):
    """
    The DrbDiscodataDataBaseNode is used to represend a database of discodata

    The DrbDiscodataDataBaseNode contains:


            **DrbDiscodataTableNode**: The groups dictionary maps the names
            of groups created
            for this `Dataset` or `Group` to instances of the `Group` class
            (the `Dataset` class is simply a special case of the `Group` class
            which describes the root group in the netCDF4 file).

    Parameters:
        parent(DrbNode): The parent of the node.
    """

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    def close(self) -> None:
        pass

    def __init__(self, parent: DrbNode, table_node: DrbNode):
        super().__init__()

        self._table_node = table_node

        self._name = table_node['name'].value
        self._parent: DrbNode = parent

        self._attributes = {}
        for col in table_node['Columns', :]:
            dict_col = {}
            for child_col in col:
                dict_col[child_col.name] = child_col.value
            self._attributes[col['name'].value, None] = dict_col

        self._children: List[DrbNode] = None
        self._path = None

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def path(self) -> ParsedPath:
        return self._parent.path / self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        if namespace_uri is None and (name, None) in self.attributes.keys():
            return self.attributes[(name, None)]
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = DrbDiscodataRowList(self)
        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    def get_elts(self, page_number):
        parent = self.parent
        table_name = self._name
        database_name_version = None
        while parent is not None \
                and not isinstance(parent, DrbDiscodataServiceNode):
            if isinstance(parent, DrbDiscodataDataBaseNode):
                database_name_version = parent.get_database_name_version()
            parent = parent.parent

        if database_name_version is not None \
                and isinstance(parent, DrbDiscodataServiceNode):
            return parent.get_elts(table_name, database_name_version,
                                   page_number)

        return None


class DrbDiscodataDataBaseNode(AbstractNode):
    """
    The DrbDiscodataDataBaseNode is used to represend a database of discodata

    The DrbDiscodataDataBaseNode contains:


            **DrbDiscodataTableNode**: The groups dictionary maps the names
            of groups created
            for this `Dataset` or `Group` to instances of the `Group` class
            (the `Dataset` class is simply a special case of the `Group` class
            which describes the root group in the netCDF4 file).

    Parameters:
        parent(DrbNode): The parent of the node.
    """

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    def close(self) -> None:
        pass

    def __init__(self, parent: DrbNode, database_node: DrbNode):
        super().__init__()

        self._database_node = database_node
        self._version = ''
        self._name = database_node['database'].value
        self._parent: DrbNode = parent

        self._children: List[DrbNode] = None
        self._path = None

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def path(self) -> ParsedPath:
        return self._parent.path / self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            if self._database_node.has_child('Schemas'):
                node_schema = self._database_node['Schemas', -1]

                self._version = node_schema['schema'].value
                try:
                    tables = node_schema['Tables', :]
                    for child_node in tables:
                        self._children.append(
                            DrbDiscodataTableNode(self, child_node))
                except Exception:
                    pass
        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    def get_database_name_version(self):
        return f'[{self._name}].[{self._version}]'


class DrbDiscodataServiceNode(AbstractNode):
    """
    Represent a node for browsing Eurostat data.

    Its attribute "tables" contain the list of all the available
    dataset and tables in the eurostat service.
    Its children is a list of DrbEurostatDataNode that can be browsed
    by dataset code.
    This node has no implementations.
    """

    def __init__(self, path='https://discodata.eea.europa.eu',
                 auth: Union[AuthBase, str] = None):
        super().__init__()
        path = path.replace('+discodata', '') if '+discodata' in path else path

        self._children = None
        if path.endswith('/'):
            path = path[:-1]
        self._path = path
        self._auth = auth
        self._path_map = path.replace('discodata', 'discomap')

    @property
    def name(self) -> str:
        return 'DISCODATA'

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException(f'Attribute not found: ({name}, {namespace_uri})')

    @property
    def parent(self) -> Optional[DrbNode]:
        return None

    @property
    def path(self) -> ParsedPath:
        return ParsedPath(self._path)

    @property
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            node = DrbHttpNode(self._path + "/md")
            json_node = create(node)

            if json_node.has_child('md'):
                for database in json_node['md'].children:
                    dt_child = DrbDiscodataDataBaseNode(self,
                                                        database)
                    self._children.append(dt_child)

        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(f'Do not support implementation: {impl}')

    def close(self) -> None:
        pass

    def get_elts(self, table_name, database_name_version, page_number):
        json = {"Page": page_number,
                "SortBy": "",
                "SortAscending": True,
                "RequestFilter": {}}

        node_ret = DrbHttpNode.post(
            self._path_map +
            f"/App/DiscodataViewer/data?fqn="
            f"{database_name_version}.[{table_name}]",
            data=json)

        return JsonBaseNode(node_ret, node_ret.get_impl(io.BufferedIOBase))


class DiscodataFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, DrbDiscodataServiceNode):
            return node
        if isinstance(node, DrbHttpNode):
            node_discodata_service = DrbDiscodataServiceNode(
                path=node.path.original_path,
                auth=node.auth)
        else:
            node_discodata_service = DrbDiscodataServiceNode(node.path.name)
        try:
            node_discodata_service.children
        except Exception:
            final_url = node.path.name.replace('+discodata', '')
            raise DrbFactoryException(f'Unsupported DISCODATA service: '
                                      f'{final_url}')
        return node_discodata_service
