from typing import List

from rick.form import RequestRecord
from flask import request
from .helpers import ParseListError, parse_list_parameters
from pokie.rest import RestService, RestServiceMixin
from pokie.constants import DI_SERVICES
from inspect import isclass


class RestMixin:
    record_class = None
    search_fields = None  # type: List
    service_name = None
    list_limit = -1

    def get(self, id=None):
        """
        Read single record by id
        :param id_record:
        :return:
        """
        if id is None:
            return self.list()

        record = self.svc.get(id)
        if record is None:
            return self.not_found()

        return self.success(record)

    def list(self):
        """
        Query records
        :return:
        """
        search_fields = self.search_fields if self.search_fields is not None else []
        text, match, limit, offset, sort = parse_list_parameters(
            request.args, self.record_class
        )

        # automatically cap records
        if offset is None and limit is None and self.list_limit > 0:
            limit = self.list_limit

        try:
            count, data = self.svc.list(
                search_fields=search_fields,
                search_text=text,
                match_fields=match,
                limit=limit,
                offset=offset,
                sort_fields=sort,
            )
            result = {"total": count, "rows": data}
            return self.success(result)
        except ParseListError as e:
            return self.error(str(e))

    def post(self):
        """
        Create Record
        :return:
        """
        record = self.request.bind(self.record_class)
        self.svc.insert(record)
        return self.success()

    def put(self, id):
        """
        Update Record
        :return:
        """
        record = self.request.bind(self.record_class)
        self.svc.update(id, record)
        return self.success()

    def delete(self, id):
        """
        delete Record by id
        :param id_record:
        :return:
        """
        if not self.svc.exists(id):
            return self.not_found()

        self.svc.delete(id_record)
        return self.success()

    @property
    def svc(self) -> RestService:
        mgr = self.di.get(DI_SERVICES)
        if self.service_name is None:
            svc_name = "svc.rest.{}.{}".format(
                self.__module__,
                str(self.record_class.__name__).replace("Record", "", 1),
            )
            if mgr.contains(svc_name):
                return mgr.get(svc_name)

            # register new service that relies on a RestService instance
            mgr.add(svc_name, "pokie.rest.RestService")
            # get new service to patch it
            svc = mgr.get(svc_name)
            # patch it
            svc.set_record_class(self.record_class)
            return svc

        svc = mgr.get(self.service_name)
        if not isinstance(svc, RestServiceMixin):
            raise RuntimeError("Service '{}' does not implement RestService mixin")
        return svc
