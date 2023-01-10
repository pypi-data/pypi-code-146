from typing import List
import flask

from viggocore.common import exception, utils
from viggocore.common.input import InputResource
from viggocore.common.subsystem import controller


class Controller(controller.Controller):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super().__init__(manager, resource_wrap, collection_wrap)

    def _get_resources(self, exceptions) -> List[InputResource]:
        resources = []
        for exception_resource in exceptions:
            endpoint = exception_resource.get('endpoint')
            methods = exception_resource.get('methods', [])
            resource = (endpoint, methods)
            resources.append(resource)

        return resources

    def create(self):
        data = flask.request.get_json()

        try:
            if data:
                exceptions = data.get('exceptions', None)
                if exceptions:
                    data['exceptions'] = self._get_resources(exceptions)
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

    def get_roles(self, id: str):
        try:
            roles = self.manager.get_roles(id=id)
            response = {"roles": [role.to_dict() for role in roles]}

        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype="application/json")

    def update_settings(self, id):
        try:
            data = flask.request.get_json()

            settings = self.manager.update_settings(id=id, **data)
            response = {'settings': settings}

            return flask.Response(response=utils.to_json(response),
                                  status=200,
                                  mimetype="application/json")
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

    def _get_keys_from_args(self):
        keys = flask.request.args.get('keys')
        if not keys:
            raise exception.BadRequest(
                'ERRO! The keys parameter was not passed correctly')
        return list(filter(None, keys.split(',')))

    def remove_settings(self, id):
        try:
            keys = self._get_keys_from_args()
            kwargs = {'keys': keys}

            settings = self.manager.remove_settings(id=id, **kwargs)
            response = {'settings': settings}

            return flask.Response(response=utils.to_json(response),
                                  status=200,
                                  mimetype="application/json")
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

    def get_application_settings_by_keys(self, id):
        try:
            keys = self._get_keys_from_args()
            kwargs = {'keys': keys}

            settings = self.manager.get_application_settings_by_keys(
                id=id, **kwargs)
            response = {'id': id, 'settings': settings}

            return flask.Response(response=utils.to_json(response),
                                  status=200,
                                  mimetype="application/json")
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
