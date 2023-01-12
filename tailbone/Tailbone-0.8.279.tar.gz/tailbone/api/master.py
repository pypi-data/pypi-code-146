# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Tailbone Web API - Master View
"""

from __future__ import unicode_literals, absolute_import

import json

import six

from rattail.config import parse_bool
from rattail.db.util import get_fieldnames

from cornice import resource, Service

from tailbone.api import APIView, api
from tailbone.db import Session


class SortColumn(object):

    def __init__(self, field_name, model_name=None):
        self.field_name = field_name
        self.model_name = model_name


class APIMasterView(APIView):
    """
    Base class for data model REST API views.
    """
    listable = True
    creatable = True
    viewable = True
    editable = True
    deletable = True
    supports_autocomplete = False
    supports_download = False
    supports_rawbytes = False

    @property
    def Session(self):
        return Session

    @classmethod
    def get_model_class(cls):
        if hasattr(cls, 'model_class'):
            return cls.model_class
        raise NotImplementedError("must set `model_class` for {}".format(cls.__name__))

    @classmethod
    def get_normalized_model_name(cls):
        if hasattr(cls, 'normalized_model_name'):
            return cls.normalized_model_name
        return cls.get_model_class().__name__.lower()

    @classmethod
    def get_route_prefix(cls):
        """
        Returns a prefix which (by default) applies to all routes provided by
        this view class.
        """
        prefix = getattr(cls, 'route_prefix', None)
        if prefix:
            return prefix
        model_name = cls.get_normalized_model_name()
        return '{}s'.format(model_name)

    @classmethod
    def get_permission_prefix(cls):
        """
        Returns a prefix which (by default) applies to all permissions
        leveraged by this view class.
        """
        prefix = getattr(cls, 'permission_prefix', None)
        if prefix:
            return prefix
        return cls.get_route_prefix()

    @classmethod
    def get_collection_url_prefix(cls):
        """
        Returns a prefix which (by default) applies to all "collection" URLs
        provided by this view class.
        """
        prefix = getattr(cls, 'collection_url_prefix', None)
        if prefix:
            return prefix
        return '/{}'.format(cls.get_route_prefix())

    @classmethod
    def get_object_url_prefix(cls):
        """
        Returns a prefix which (by default) applies to all "object" URLs
        provided by this view class.
        """
        prefix = getattr(cls, 'object_url_prefix', None)
        if prefix:
            return prefix
        return '/{}'.format(cls.get_route_prefix())

    @classmethod
    def get_object_key(cls):
        if hasattr(cls, 'object_key'):
            return cls.object_key
        return cls.get_normalized_model_name()

    @classmethod
    def get_collection_key(cls):
        if hasattr(cls, 'collection_key'):
            return cls.collection_key
        return '{}s'.format(cls.get_object_key())

    @classmethod
    def establish_method(cls, method_name):
        """
        Establish the given HTTP method for this Cornice Resource.

        Cornice will auto-register any class methods for a resource, if they
        are named according to what it expects (i.e. 'get', 'collection_get'
        etc.).  Tailbone API tries to make things automagical for the sake of
        e.g. Poser logic, but in this case if we predefine all of these methods
        and then some subclass view wants to *not* allow one, it's not clear
        how to "undefine" it per se.  Or at least, the more straightforward
        thing (I think) is to not define such a method in the first place, if
        it was not wanted.

        Enter ``establish_method()``, which is what finally "defines" each
        resource method according to what the subclass has declared via its
        various attributes (:attr:`creatable`, :attr:`deletable` etc.).

        Note that you will not likely have any need to use this
        ``establish_method()`` yourself!  But we describe its purpose here, for
        clarity.
        """
        def method(self):
            internal_method = getattr(self, '_{}'.format(method_name))
            return internal_method()

        setattr(cls, method_name, method)

    def make_filter_spec(self):
        if not self.request.GET.has_key('filters'):
            return []

        filters = json.loads(self.request.GET.getone('filters'))
        return filters

    def make_sort_spec(self):

        # we prefer a "native sort"
        if self.request.GET.has_key('nativeSort'):
            return json.loads(self.request.GET.getone('nativeSort'))

        # these params are based on 'vuetable-2'
        # https://www.vuetable.com/guide/sorting.html#initial-sorting-order
        if 'sort' in self.request.params:
            sort = self.request.params['sort']
            sortkey, sortdir = sort.split('|')
            if sortdir != 'desc':
                sortdir = 'asc'
            return [
                {
                    # 'model': self.model_class.__name__,
                    'field': sortkey,
                    'direction': sortdir,
                },
            ]

        # these params are based on 'vue-tables-2'
        # https://github.com/matfish2/vue-tables-2#server-side
        if 'orderBy' in self.request.params and 'ascending' in self.request.params:
            sortcol = self.interpret_sortcol(self.request.params['orderBy'])
            if sortcol:
                spec = {
                    'field': sortcol.field_name,
                    'direction': 'asc' if parse_bool(self.request.params['ascending']) else 'desc',
                }
                if sortcol.model_name:
                    spec['model'] = sortcol.model_name
                return [spec]

    def interpret_sortcol(self, order_by):
        """
        This must return a ``SortColumn`` object based on parsing of the given
        ``order_by`` string, which is "raw" as received from the client.

        Please override as necessary, but in all cases you should invoke
        :meth:`sortcol()` to obtain your return value.  Default behavior
        for this method is to simply do (only) that::

           return self.sortcol(order_by)

        Note that you can also return ``None`` here, if the given ``order_by``
        string does not represent a valid sort.
        """
        return self.sortcol(order_by)

    def sortcol(self, field_name, model_name=None):
        """
        Return a simple ``SortColumn`` object which denotes the field and
        optionally, the model, to be used when sorting.
        """
        if not model_name:
            model_name = self.model_class.__name__
        return SortColumn(field_name, model_name)

    def join_for_sort_spec(self, query, sort_spec):
        """
        This should apply any joins needed on the given query, to accommodate
        requested sorting as per ``sort_spec`` - which will be non-empty but
        otherwise no claims are made regarding its contents.

        Please override as necessary, but in all cases you should return a
        query, either untouched or else with join(s) applied.
        """
        model_name = sort_spec[0].get('model')
        return self.join_for_sort_model(query, model_name)

    def join_for_sort_model(self, query, model_name):
        """
        This should apply any joins needed on the given query, to accommodate
        requested sorting on a field associated with the given model.

        Please override as necessary, but in all cases you should return a
        query, either untouched or else with join(s) applied.
        """
        return query

    def make_pagination_spec(self):

        # these params are based on 'vuetable-2'
        # https://github.com/ratiw/vuetable-2-tutorial/wiki/prerequisite#sample-api-endpoint
        if 'page' in self.request.params and 'per_page' in self.request.params:
            page = self.request.params['page']
            per_page = self.request.params['per_page']
            if page.isdigit() and per_page.isdigit():
                return int(page), int(per_page)

        # these params are based on 'vue-tables-2'
        # https://github.com/matfish2/vue-tables-2#server-side
        if 'page' in self.request.params and 'limit' in self.request.params:
            page = self.request.params['page']
            limit = self.request.params['limit']
            if page.isdigit() and limit.isdigit():
                return int(page), int(limit)

    def base_query(self):
        cls = self.get_model_class()
        query = self.Session.query(cls)
        return query

    def get_fieldnames(self):
        if not hasattr(self, '_fieldnames'):
            self._fieldnames = get_fieldnames(
                self.rattail_config, self.model_class,
                columns=True, proxies=True, relations=False)
        return self._fieldnames

    def normalize(self, obj):
        data = {'_str': six.text_type(obj)}

        for field in self.get_fieldnames():
            data[field] = getattr(obj, field)

        return data

    def _collection_get(self):
        from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination

        query = self.base_query()
        context = {}

        # maybe filter query
        filter_spec = self.make_filter_spec()
        if filter_spec:
            query = apply_filters(query, filter_spec)

        # maybe sort query
        sort_spec = self.make_sort_spec()
        if sort_spec:
            query = self.join_for_sort_spec(query, sort_spec)
            query = apply_sort(query, sort_spec)

            # maybe paginate query
            pagination_spec = self.make_pagination_spec()
            if pagination_spec:
                number, size = pagination_spec
                query, pagination = apply_pagination(query, page_number=number, page_size=size)

                # these properties are based on 'vuetable-2'
                # https://www.vuetable.com/guide/pagination.html#how-the-pagination-component-works
                context['total'] = pagination.total_results
                context['per_page'] = pagination.page_size
                context['current_page'] = pagination.page_number
                context['last_page'] = pagination.num_pages
                context['from'] = pagination.page_size * (pagination.page_number - 1) + 1
                to = pagination.page_size * (pagination.page_number - 1) + pagination.page_size
                if to > pagination.total_results:
                    context['to'] = pagination.total_results
                else:
                    context['to'] = to

                # these properties are based on 'vue-tables-2'
                # https://github.com/matfish2/vue-tables-2#server-side
                context['count'] = pagination.total_results

        objects = [self.normalize(obj) for obj in query]

        # TODO: test this for ratbob!
        context[self.get_collection_key()] = objects

        # these properties are based on 'vue-tables-2'
        # https://github.com/matfish2/vue-tables-2#server-side
        context['data'] = objects
        if 'count' not in context:
            context['count'] = len(objects)

        return context

    def get_object(self, uuid=None):
        if not uuid:
            uuid = self.request.matchdict['uuid']

        obj = self.Session.query(self.get_model_class()).get(uuid)
        if obj:
            return obj

        raise self.notfound()

    def _get(self, obj=None, uuid=None):
        if not obj:
            obj = self.get_object(uuid=uuid)
        key = self.get_object_key()
        normal = self.normalize(obj)
        return {key: normal, 'data': normal}

    def _collection_post(self):
        """
        Default method for actually processing a POST request for the
        collection, aka. "create new object".
        """
        # assume our data comes only from request JSON body
        data = self.request.json_body

        # add instance to session, and return data for it
        obj = self.create_object(data)
        self.Session.flush()
        return self._get(obj)

    def create_object(self, data):
        """
        Create a new object instance and populate it with the given data.

        Note that this method by default will only populate *simple* fields, so
        you may need to subclass and override to add more complex field logic.
        """
        # create new instance of model class
        cls = self.get_model_class()
        obj = cls()

        # "update" new object with given data
        obj = self.update_object(obj, data)

        # that's all we can do here, subclass must override if more needed
        self.Session.add(obj)
        return obj

    def _post(self, uuid=None):
        """
        Default method for actually processing a POST request for an object,
        aka. "update existing object".
        """
        if not uuid:
            uuid = self.request.matchdict['uuid']
        obj = self.Session.query(self.get_model_class()).get(uuid)
        if not obj:
            raise self.notfound()

        # assume our data comes only from request JSON body
        data = self.request.json_body

        # try to update data for object, returning error as necessary
        obj = self.update_object(obj, data)
        if isinstance(obj, dict) and 'error' in obj:
            return {'error': obj['error']}

        # return data for object
        self.Session.flush()
        return self._get(obj)

    def update_object(self, obj, data):
        """
        Update the given object instance with the given data.

        Note that this method by default will only update *simple* fields, so
        you may need to subclass and override to add more complex field logic.
        """
        # set values for simple fields only
        for key, value in data.items():
            if hasattr(obj, key):
                # TODO: what about datetime, decimal etc.?
                setattr(obj, key, value)

        # that's all we can do here, subclass must override if more needed
        return obj

    ##############################
    # delete
    ##############################

    def _delete(self):
        """
        View to handle DELETE action for an existing record/object.
        """
        obj = self.get_object()
        self.delete_object(obj)

    def delete_object(self, obj):
        """
        Delete the object, or mark it as deleted, or whatever you need to do.
        """
        # flush immediately to force any pending integrity errors etc.
        self.Session.delete(obj)
        self.Session.flush()

    ##############################
    # download
    ##############################

    def download(self):
        """
        GET view allowing for download of a single file, which is attached to a
        given record.
        """
        obj = self.get_object()

        filename = self.request.GET.get('filename', None)
        if not filename:
            raise self.notfound()
        path = self.download_path(obj, filename)

        response = self.file_response(path)
        return response

    def download_path(self, obj, filename):
        """
        Should return absolute path on disk, for the given object and filename.
        Result will be used to return a file response to client.
        """
        raise NotImplementedError

    def rawbytes(self):
        """
        GET view allowing for direct access to the raw bytes of a file, which
        is attached to a given record.  Basically the same as 'download' except
        this does not come as an attachment.
        """
        obj = self.get_object()

        filename = self.request.GET.get('filename', None)
        if not filename:
            raise self.notfound()
        path = self.download_path(obj, filename)

        response = self.file_response(path, attachment=False)
        return response

    ##############################
    # autocomplete
    ##############################

    def autocomplete(self):
        """
        View which accepts a single ``term`` param, and returns a list of
        autocomplete results to match.
        """
        term = self.request.params.get('term', '').strip()
        term = self.prepare_autocomplete_term(term)
        if not term:
            return []

        results = self.get_autocomplete_data(term)
        return [{'label': self.autocomplete_display(x),
                 'value': self.autocomplete_value(x)}
                for x in results]

    @property
    def autocomplete_fieldname(self):
        raise NotImplementedError("You must define `autocomplete_fieldname` "
                                  "attribute for API view class: {}".format(
                                      self.__class__))

    def autocomplete_display(self, obj):
        return getattr(obj, self.autocomplete_fieldname)

    def autocomplete_value(self, obj):
        return obj.uuid

    def get_autocomplete_data(self, term):
        query = self.make_autocomplete_query(term)
        return query.all()

    def make_autocomplete_query(self, term):
        model_class = self.get_model_class()
        query = self.Session.query(model_class)
        query = self.filter_autocomplete_query(query)

        field = getattr(model_class, self.autocomplete_fieldname)
        query = query.filter(field.ilike('%%%s%%' % term))\
                     .order_by(field)

        return query

    def filter_autocomplete_query(self, query):
        return query

    def prepare_autocomplete_term(self, term):
        """
        If necessary, massage the incoming search term for use with the
        autocomplete query.
        """
        return term

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)

    @classmethod
    def _defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        permission_prefix = cls.get_permission_prefix()
        collection_url_prefix = cls.get_collection_url_prefix()
        object_url_prefix = cls.get_object_url_prefix()

        # first, the primary resource API

        # list/search
        if cls.listable:
            cls.establish_method('collection_get')
            resource.add_view(cls.collection_get, permission='{}.list'.format(permission_prefix))

        # create
        if cls.creatable:
            cls.establish_method('collection_post')
            if hasattr(cls, 'permission_to_create'):
                permission = cls.permission_to_create
            else:
                permission = '{}.create'.format(permission_prefix)
            resource.add_view(cls.collection_post, permission=permission)

        # view
        if cls.viewable:
            cls.establish_method('get')
            resource.add_view(cls.get, permission='{}.view'.format(permission_prefix))

        # edit
        if cls.editable:
            cls.establish_method('post')
            resource.add_view(cls.post, permission='{}.edit'.format(permission_prefix))

        # delete
        if cls.deletable:
            cls.establish_method('delete')
            resource.add_view(cls.delete, permission='{}.delete'.format(permission_prefix))

        # register primary resource API via cornice
        object_resource = resource.add_resource(
            cls,
            collection_path=collection_url_prefix,
            # TODO: probably should allow for other (composite?) key fields
            path='{}/{{uuid}}'.format(object_url_prefix))
        config.add_cornice_resource(object_resource)

        # now for some more "custom" things, which are still somewhat generic

        # autocomplete
        if cls.supports_autocomplete:
            autocomplete = Service(name='{}.autocomplete'.format(route_prefix),
                                   path='{}/autocomplete'.format(collection_url_prefix))
            autocomplete.add_view('GET', 'autocomplete', klass=cls,
                                  permission='{}.list'.format(permission_prefix))
            config.add_cornice_service(autocomplete)

        # download
        if cls.supports_download:
            download = Service(name='{}.download'.format(route_prefix),
                               # TODO: probably should allow for other (composite?) key fields
                               path='{}/{{uuid}}/download'.format(object_url_prefix))
            download.add_view('GET', 'download', klass=cls,
                              permission='{}.download'.format(permission_prefix))
            config.add_cornice_service(download)

        # rawbytes
        if cls.supports_rawbytes:
            rawbytes = Service(name='{}.rawbytes'.format(route_prefix),
                               # TODO: probably should allow for other (composite?) key fields
                               path='{}/{{uuid}}/rawbytes'.format(object_url_prefix))
            rawbytes.add_view('GET', 'rawbytes', klass=cls,
                              permission='{}.download'.format(permission_prefix))
            config.add_cornice_service(rawbytes)
