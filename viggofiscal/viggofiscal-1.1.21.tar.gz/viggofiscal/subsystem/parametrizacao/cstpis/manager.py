import flask

from viggocore.common.subsystem import operation
from viggocore.common.subsystem.pagination import Pagination
from viggocore.common import manager

from viggofiscal.subsystem.parametrizacao.cstpis.resource import Cstpis


class List(operation.List):

    def do(self, session, **kwargs):

        if flask.has_request_context():
            token_id = flask.request.headers.get('token')
            if token_id is not None:
                self.token = self.manager.api.tokens().get(id=token_id)
                if self.token is not None:
                    self.user = self.manager.api.users().get(
                        id=self.token.user_id)

        empresa = None
        crt_empresa = None
        if self.user is not None:
            empresa = self.manager.api.domain_orgs().get(id=self.user.domain_id)
        if empresa is not None:
            crt_empresa = empresa.crt
        cst_list = ["2", "4", "8", "49"]

        query = session.query(Cstpis)

        if crt_empresa.value == 1:
            query = query.filter(Cstpis.cst.in_(cst_list))
        elif crt_empresa.value == 2 or crt_empresa.value == 3:
            query = query.filter(Cstpis.cst.not_in(cst_list))

        query = self.manager.apply_filters(query, Cstpis, **kwargs)

        query = query.distinct()

        total_rows = None
        if self.manager.with_pagination(**kwargs):
            total_rows = query.count()

        pagination = Pagination.get_pagination(Cstpis, **kwargs)
        if pagination.order_by is not None:
            pagination.adjust_order_by(Cstpis)
        query = self.driver.apply_pagination(query, pagination)
        result = query.all()

        return (result, total_rows)


class Manager(manager.CommonManager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.list = List(self)