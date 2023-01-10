from viggocore.common.subsystem.manager import Manager
import flask

from enum import Enum
from viggocore.common import exception, utils
# TODO(samueldmq): find a better name to this
# from viggocore.common.subsystem import manager as m


class ListOptions(Enum):
    ACTIVE_ONLY = {'id': 0, 'value': True}
    INACTIVE_ONLY = {'id': 1, 'value': False}
    ACTIVE_AND_INACTIVE = {'id': 2, 'value': None}

    @classmethod
    def new(cls, option):
        if option:
            return ListOptions[option]
        else:
            return ListOptions.ACTIVE_ONLY

    @classmethod
    def invalid_message_error(cls):
        return 'Invalid list_options.\nAvailables options are {}'.\
            format(', '.join(ListOptions. _member_names_))


class Controller(object):

    def __init__(self, manager: Manager,
                 resource_wrap: str,
                 collection_wrap: str) -> None:
        self.manager = manager
        self.resource_wrap = resource_wrap
        self.collection_wrap = collection_wrap

    def _filters_parse(self):
        filters = {
            k: flask.request.args.get(k) for k in flask.request.args.keys()}
        # TODO(samueldmq): fix this to work in a better way
        for k, v in filters.items():
            if v == 'true':
                filters[k] = True
            elif v == 'false':
                filters[k] = False
            elif v == 'null':
                filters[k] = None

        return filters

    def _filter_args(self, filters):
        filter_args = {k: v for k, v in filters.items() if '.' in k}

        return filter_args

    def _filters_cleanup(self, filters):
        _filters_cleanup = filters

        filter_args = self._filter_args(_filters_cleanup)
        # clean up original filters
        for k in filter_args.keys():
            # NOTE(samueldmq): I'm not sure I can pop
            # in the list comprehesion above...
            _filters_cleanup.pop(k)

        return _filters_cleanup

    def _parse_list_options(self, filters):
        _filters = filters.copy()
        options = _filters.pop('list_options', None)
        if 'active' in _filters.keys():
            return _filters
        try:
            options = ListOptions.new(options)
        except KeyError:
            raise exception.BadRequest(ListOptions.invalid_message_error())

        value = options.value['value']
        if value is not None:
            _filters['active'] = value

        return _filters

    def _get_include_dict(self, query_arg, filter_args):
        lists = [li.split('.') for li in query_arg.split(',')]
        include_dict = {}
        for list in lists:
            current = include_dict
            for i in range(len(list)):
                if list[i] in current:
                    current[list[i]].update({
                        list[i + 1]: {}} if i < (len(list) - 1) else {})
                else:
                    current[list[i]] = {
                        list[i + 1]: {}} if i < (len(list) - 1) else {}
                current = current[list[i]]

        for k, v in filter_args.items():
            list = k.split('.')
            current = include_dict
            for i in list[:-1]:  # last element is the attribute to filter on
                try:
                    current = current[i]
                except AttributeError:
                    # ignore current filter,
                    # entity to filter on is not included
                    continue
            current[list[-1]] = v

        return include_dict

    def _get_include_dicts(self):
        filters = self._filters_parse()

        include_args = filters.pop('include', None)
        filter_args = self._filter_args(filters)

        include_dict = self._get_include_dict(
            include_args, filter_args) if include_args else {}

        return include_dict

    def _entities_to_dict(self, entities, include_dicts=None):
            collection = []
            for entity in entities:
                if isinstance(entity, dict):
                    collection.append(entity)
                else:
                    try:
                        collection.append(
                            entity.to_dict(include_dict=include_dicts))
                    except AssertionError:
                        # ignore current entity, filter mismatch
                        pass

            return collection

    def _clean_filters(self, **kwargs):
        excludes = ['include', 'page', 'page_size', 'order_by',
                    'require_pagination']
        filters_args = dict()
        for arg in kwargs:
            if arg not in excludes:
                filters_args.update({arg: kwargs.get(arg, None)})
        return filters_args

    def create(self):
        data = flask.request.get_json()

        try:
            if data:
                entity = self.manager.create(**data)
            else:
                entity = self.manager.create()
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=utils.to_json(response),
                              status=201,
                              mimetype="application/json")

    def get(self, id):
        try:
            entity = self.manager.get(id=id)

            include_dicts = self._get_include_dicts()

            entity_dict = entity.to_dict(include_dict=include_dicts)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.resource_wrap: entity_dict}

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype="application/json")

    def list(self):
        filters = self._filters_parse()
        filters = self._filters_cleanup(filters)

        try:
            filters = self._parse_list_options(filters)
            entities = self.manager.list(**filters)

            with_pagination = False
            require_pagination = filters.get('require_pagination', False)
            page = filters.get('page', None)
            page_size = filters.get('page_size', None)

            if (page and page_size is not None) and require_pagination is True:
                with_pagination = True
                count = self.manager.count(**(self._clean_filters(**filters)))
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
        except ValueError:
            raise exception.BadRequest('page or page_size is invalid')

        collection = self._entities_to_dict(
            entities, self._get_include_dicts())

        response = {self.collection_wrap: collection}

        if with_pagination:
            response.update({'pagination': {'page': int(page),
                                            'page_size': int(page_size),
                                            'total': count}})

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype="application/json")

    def update(self, id):
        data = flask.request.get_json()

        try:
            entity = self.manager.update(**data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype="application/json")

    def delete(self, id):
        try:
            self.manager.delete(id=id)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")
