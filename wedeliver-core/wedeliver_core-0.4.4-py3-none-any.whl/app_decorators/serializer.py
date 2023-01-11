import json
from functools import wraps
from sqlalchemy.orm.base import object_mapper
import flask_sqlalchemy
from flask import request
from marshmallow import ValidationError
from sqlalchemy.orm.exc import UnmappedInstanceError

from wedeliver_core.helpers.exceptions import AppValidationError


def is_mapped(obj):
    try:
        data = obj
        if isinstance(data, list) and len(data):
            data = obj[0]
        object_mapper(data)
    except UnmappedInstanceError:
        return False
    return True


def serializer(schema=None, many=False):
    def factory(func):
        @wraps(func)
        def decorator(*args, **kwargs):

            appended_kws = kwargs.pop('appended_kws', None)

            try:
                client_data = dict()

                if request.json:
                    client_data = request.json
                elif request.form:
                    client_data = request.form.to_dict()
                    for key, value in client_data.items():
                        try:
                            # look for strings like objects to convert them to python objects
                            client_data[key] = json.loads(value)
                        except json.JSONDecodeError as e:
                            pass

                if request.args:
                    client_data.update(request.args.to_dict())

                inputs = client_data  # .to_dict()
                if appended_kws:
                    inputs.update(appended_kws)

                if schema:
                    result = schema(many=many).load(inputs)
                else:
                    result = inputs
            except ValidationError as e:
                raise AppValidationError(e.messages)

            if result:
                kwargs.update(dict(validated_data=result))

            # if schema and request.method == "GET":
            try:
                result = func(*args, **kwargs)
                if isinstance(result, flask_sqlalchemy.Pagination):
                    items = schema(many=isinstance(result.items, list)).dump(result.items)
                    output = dict(
                        items=items,
                        total=result.total,
                        next_num=result.next_num,
                        prev_num=result.prev_num,
                        page=result.page,
                        per_page=result.per_page
                    )
                elif is_mapped(result):  # is model instance
                    output = schema(many=isinstance(result, list)).dump(result)
                else:
                    output = result
            except ValidationError as e:
                raise AppValidationError(e.messages)

            return output

            # return func(*args, **kwargs)

        return decorator

    return factory
