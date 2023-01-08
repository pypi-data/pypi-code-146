import re

from datetime import datetime
from functools import wraps
from flask import request, jsonify, make_response
from flask_cors import CORS
from json import dumps
from marshmallow_mongoengine import ModelSchema
from flask_restful import Api, reqparse, inputs
from flask_mongoengine import MongoEngine, DoesNotExist
from flask_jwt_extended import get_jwt_identity
from mongoengine.queryset.visitor import Q
from mongoengine.errors import ValidationError

from .exceptions import InvalidPayloadSupplied, BadRequest, Forbidden

# Constant fields

API_PREFIX = '/api'


class QueryArgs:
    DAY = 'day'
    ORDER_BY = 'order_by'
    DESC = 'desc'

    GREATER = 'gt'

    URL = 'url'


# Pagination
DEFAULT_PAGE_SIZE = 10

api = Api()

mongo = MongoEngine()


def create_module(app):

    mongo.init_app(app)
    CORS(app)

    from .v1 import create_module as create_api_v1

    create_api_v1(app, api)

    # Using workaround from here to handle inherit exception handling from flask: https://github.com/flask-restful/flask-restful/issues/280#issuecomment-280648790
    handle_exceptions = app.handle_exception
    handle_user_exception = app.handle_user_exception
    api.init_app(app)
    app.handle_user_exception = handle_exceptions
    app.handle_user_exception = handle_user_exception


@api.representation('application/json')
def output_json(data, code, headers=None):
    """
        NOTE: if a resource method is decorated with 'paginated' this method is not called
    """
    if isinstance(data, mongo.Document) or isinstance(data, mongo.EmbeddedDocument):
        data = data.to_mongo()

    resp = make_response(jsonify(data), code)
    resp.headers.extend(headers or {})
    return resp


def validate_payload(model_schema: ModelSchema, kwname='payload'):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data, errors = model_schema.load(request.get_json())

            if len(errors) != 0:
                raise InvalidPayloadSupplied(
                    'invalid payload supplied', errors)

            kwargs[kwname] = data

            return func(*args, **kwargs)
        return wrapper

    return decorate


def parse_query_args(func):
    query_args_reqparse = reqparse.RequestParser()
    query_args_reqparse.add_argument(
        QueryArgs.DAY,
        type=str,
        location=['args'],
        required=False,
        default=None
    )
    query_args_reqparse.add_argument(
        QueryArgs.ORDER_BY,
        type=str,
        location=['args'],
        required=False,
        default=None
    )
    query_args_reqparse.add_argument(
        QueryArgs.DESC,
        type=bool,
        location=['args'],
        required=False,
        default=False
    )
    query_args_reqparse.add_argument(
        QueryArgs.GREATER,
        type=str,
        location=['args'],
        required=False
    )
    query_args_reqparse.add_argument(
        QueryArgs.URL,
        type=inputs.regex(
            "^(https?:\\/\\/(?:www\\.)?)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"),
        location=['args'],
        required=False
    )

    @wraps(func)
    def wrapper(*args, **kwargs):
        query_args = query_args_reqparse.parse_args()

        kwargs['query_args'] = {
            QueryArgs.DAY: query_args[QueryArgs.DAY],
            QueryArgs.ORDER_BY: query_args[QueryArgs.ORDER_BY],
            QueryArgs.DESC: query_args[QueryArgs.DESC],
            QueryArgs.GREATER: query_args[QueryArgs.GREATER],
            QueryArgs.URL: query_args[QueryArgs.URL],
        }

        return func(*args, **kwargs)
    return wrapper


def get_payload(kwname='payload'):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            kwargs[kwname] = data

            return func(*args, **kwargs)
        return wrapper

    return decorate


def load_user_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from .models import User
        try:
            user = User.objects(Q(email=get_jwt_identity())).get()
        except DoesNotExist:
            raise Forbidden()

        kwargs['user_info'] = user

        return func(*args, **kwargs)
    return wrapper


def paginated(func):
    pagination_reqparse = reqparse.RequestParser()
    pagination_reqparse.add_argument(
        'page',
        type=int,
        location=['args'],
        required=False,
        default=1
    )
    pagination_reqparse.add_argument(
        'per_page',
        type=int,
        location=['args'],
        required=False,
        default=DEFAULT_PAGE_SIZE
    )

    @wraps(func)
    def wrapper(*args, **kwargs):
        page_args = pagination_reqparse.parse_args()
        page = page_args['page']
        per_page = page_args['per_page']

        if page <= 0:
            raise BadRequest('page argument must be greater than zero')

        if per_page <= 0:
            raise BadRequest('per_page argument must be greater than zero')

        kwargs['page_args'] = {
            'page': page,
            'per_page': per_page
        }

        page = func(*args, **kwargs)

        return jsonify({
            # "results": page.items,
            "results": [item.to_mongo() if isinstance(item, mongo.Document) else item for item in page.items],
            "pages": page.pages
        })

    return wrapper


def _update_embedded_document(new_doc: mongo.EmbeddedDocument, old_doc: mongo.EmbeddedDocument, patch=True):
    if patch == True:
        for field in new_doc.__class__._fields:
            if new_doc[field] != None:
                old_doc[field] = new_doc[field]
        return old_doc
    else:
        return new_doc


def _update_document(coll_class: mongo.Document.__class__, new_doc: mongo.Document, old_doc: mongo.Document, patch=True):
    # Remove generated id and link new doc with current owner
    new_doc._id = old_doc._id
    new_doc.owner = old_doc.owner
    new_doc.insert_timestamp = old_doc.insert_timestamp

    if patch == True:
        return coll_class._get_collection().update_one(
            {'_id': old_doc.id}, {'$set': new_doc.to_mongo()})
    else:
        return coll_class._get_collection().replace_one(
            {'_id': old_doc.id}, new_doc.to_mongo())


def put_document(coll_class: mongo.Document.__class__, new_doc: mongo.Document, old_doc: mongo.Document):
    return _update_document(coll_class, new_doc, old_doc, patch=False)


def patch_document(coll_class: mongo.Document.__class__, new_doc: mongo.Document, old_doc: mongo.Document):
    return _update_document(coll_class, new_doc, old_doc, patch=True)


def put_embedded_document(new_doc: mongo.EmbeddedDocument, old_doc: mongo.EmbeddedDocument):
    return _update_embedded_document(new_doc, old_doc, patch=False)


def patch_embedded_document(new_doc: mongo.EmbeddedDocument, old_doc: mongo.EmbeddedDocument):
    return _update_embedded_document(new_doc, old_doc, patch=True)


def _build_query_by_params(base_query, query_args):
    if QueryArgs.DAY in query_args and query_args[QueryArgs.DAY] is not None:
        if bool(re.search(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$', query_args[QueryArgs.DAY])):
            try:
                searched_day = datetime.strptime(
                    query_args[QueryArgs.DAY], '%Y-%m-%d')
            except ValueError as ex:
                raise BadRequest(
                    'invalid day parameter supplied: {}'.format(ex))
        else:
            raise BadRequest('invalid day format')

        base_query = base_query & Q(date=searched_day)

    if QueryArgs.GREATER in query_args and query_args[QueryArgs.GREATER] is not None:
        if (not bool(re.search(r'^\w+\$\d+$', query_args[QueryArgs.GREATER]))):
            raise BadRequest('invalid gt value')

        split = query_args[QueryArgs.GREATER].split('$')

        base_query = base_query & Q(**{"{}__gt".format(split[0]): split[1]})

    return base_query


def _apply_ordering(filtered_objects, query_args):
    if (query_args[QueryArgs.ORDER_BY] != None and query_args[QueryArgs.ORDER_BY] != ''):
        if (query_args[QueryArgs.DESC] == True):
            filtered_objects = filtered_objects.order_by(
                '-' + query_args[QueryArgs.ORDER_BY])  # descending "-"
        else:
            filtered_objects = filtered_objects.order_by(
                '+' + query_args[QueryArgs.ORDER_BY])  # ascending "+"

    return filtered_objects


def _apply_pagination(ordered_objects, page_args):
    return ordered_objects.paginate(page=page_args['page'], per_page=page_args['per_page'])


def search_on_model(coll_class: mongo.Document.__class__, base_query, query_args, page_args):
    query_filter = _build_query_by_params(base_query, query_args)

    filtered_objects = coll_class.objects(query_filter)
    ordered_objects = _apply_ordering(filtered_objects, query_args)
    paginated_objects = _apply_pagination(ordered_objects, page_args)

    return paginated_objects
