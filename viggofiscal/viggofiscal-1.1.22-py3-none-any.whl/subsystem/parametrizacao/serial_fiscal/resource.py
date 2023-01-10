from enum import Enum
import sqlalchemy

from viggocore.database import db
from viggocore.common.subsystem import entity


class SerieFiscalAmbiente(Enum):
    HOMOLOGACAO = 'HOMOLOGACAO'
    PRODUCAO = 'PRODUCAO'


class SerieFiscalStatus(Enum):
    ATIVO = 'ATIVO'
    INATIVO = 'INATIVO'


class SerieFiscal(entity.Entity, db.Model):

    attributes = ['domain_org_id', 'ambiente', 'modelo', 'serie',
                  'ultimo_doc', 'status']
    attributes += entity.Entity.attributes

    domain_org_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain_org.id'), nullable=False)
    ambiente = db.Column(sqlalchemy.Enum(SerieFiscalAmbiente))
    modelo = db.Column(db.Numeric(10), nullable=False)
    serie = db.Column(db.Numeric(10), nullable=False)
    ultimo_doc = db.Column(db.Numeric(15), nullable=False)
    status = db.Column(sqlalchemy.Enum(SerieFiscalStatus))

    def __init__(self, id, domain_org_id, ambiente, modelo, serie,
                 ultimo_doc, status,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_org_id = domain_org_id
        self.ambiente = ambiente
        self.modelo = modelo
        self.serie = serie
        self.ultimo_doc = ultimo_doc
        self.status = status

    @classmethod
    def individual(cls):
        return 'serie_fiscal'
