from viggocore.common.subsystem import operation
from viggocore.common.subsystem.pagination import Pagination
from viggocore.common import manager

from viggofiscal.subsystem.parametrizacao.tipo_operacao.resource \
    import TipoOperacao


class Create(operation.Create):

    def pre(self, session, **kwargs):
        codigo = kwargs.get('codigo', None)
        domain_id = kwargs.get('domain_org_id', None)

        if not codigo and domain_id:
            kwargs['codigo'] = self.manager.api.domain_sequences().\
                get_nextval(id=domain_id, name=TipoOperacao.CODIGO_SEQUENCE)

        return super().pre(session=session, **kwargs)


class List(operation.List):

    def do(self, session, **kwargs):
        query = session.query(TipoOperacao)

        query = self.manager.apply_filters(query, TipoOperacao, **kwargs)
        query = query.distinct()

        total_rows = None
        if self.manager.with_pagination(**kwargs):
            total_rows = query.count()

        pagination = Pagination.get_pagination(TipoOperacao, **kwargs)
        if pagination.order_by is not None:
            pagination.adjust_order_by(TipoOperacao)
        query = self.driver.apply_pagination(query, pagination)
        result = query.all()

        return (result, total_rows)


class Manager(manager.CommonManager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.create = Create(self)
        self.list = List(self)
