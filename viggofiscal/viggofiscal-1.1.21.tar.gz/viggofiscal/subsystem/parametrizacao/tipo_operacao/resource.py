from viggocore.database import db
from viggocore.common.subsystem import entity
from sqlalchemy import UniqueConstraint


class TipoOperacao(entity.Entity, db.Model):

    CODIGO_SEQUENCE = 'tipo_operacao_codigo_sq'

    attributes = ['domain_org_id', 'codigo', 'descricao']
    attributes += entity.Entity.attributes

    domain_org_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain_org.id'), nullable=False)

    codigo = db.Column(db.Numeric(10), db.Sequence(CODIGO_SEQUENCE),
                       nullable=False)
    descricao = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'domain_org_id', 'codigo',
            name='tipo_operacao_domain_org_id_codigo_uk'),)

    def __init__(self, id, domain_org_id, codigo, descricao,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_org_id = domain_org_id
        self.codigo = codigo
        self.descricao = descricao

    @classmethod
    def individual(cls):
        return 'tipo_operacao'
