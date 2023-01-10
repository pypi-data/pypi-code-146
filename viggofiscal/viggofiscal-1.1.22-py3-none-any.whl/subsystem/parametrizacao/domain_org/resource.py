from enum import Enum
import sqlalchemy
from sqlalchemy import orm, ForeignKeyConstraint

from viggocore.database import db
from viggocore.common.subsystem import entity


class Crt(Enum):
    SIMPLES_NACIONAL = 1
    SN_EXC_REC_BRUTA = 2
    REGIME_NORMAL = 3
    MEI = 4


class RegPisCofins(Enum):
    CUMULATIVO = 1
    NAO_CUMULATIVO = 2


class DomainOrg(entity.Entity, db.Model):

    attributes = ['crt', 'cpf_cnpj', 'insc_est', 'razao_social',
                  'nome_fantasia', 'insc_mun', 'cnae', 'cpf_cnpj_contador',
                  'reg_pis_cofins', 'aliq_pis', 'aliq_cofins', 'cred_sn']
    attributes += entity.Entity.attributes

    domain = orm.relationship(
        'Domain', backref=orm.backref('domain_org_domain'))

    crt = db.Column(sqlalchemy.Enum(Crt), nullable=False)
    cpf_cnpj = db.Column(db.String(14), nullable=False)
    insc_est = db.Column(db.String(14), nullable=False)
    razao_social = db.Column(db.String(100), nullable=False)
    nome_fantasia = db.Column(db.String(100), nullable=False)
    insc_mun = db.Column(db.String(15), nullable=True)
    cnae = db.Column(db.String(15), nullable=True)
    cpf_cnpj_contador = db.Column(db.String(14), nullable=True)
    reg_pis_cofins = db.Column(sqlalchemy.Enum(RegPisCofins), nullable=True)
    aliq_pis = db.Column(db.Numeric(7, 2), nullable=True)
    aliq_cofins = db.Column(db.Numeric(7, 2), nullable=True)
    cred_sn = db.Column(db.Numeric(7, 2), nullable=True)

    __table_args__ = (ForeignKeyConstraint(['id'], ['domain.id']),)

    def __init__(self, id, crt, cpf_cnpj, insc_est, razao_social,
                 nome_fantasia, insc_mun=None, cnae=None,
                 cpf_cnpj_contador=None, reg_pis_cofins=None, aliq_pis=None,
                 aliq_cofins=None, cred_sn=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.crt = crt
        self.cpf_cnpj = cpf_cnpj
        self.insc_est = insc_est
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia
        self.insc_mun = insc_mun
        self.cnae = cnae
        self.cpf_cnpj_contador = cpf_cnpj_contador
        self.reg_pis_cofins = reg_pis_cofins
        self.aliq_pis = aliq_pis
        self.aliq_cofins = aliq_cofins
        self.cred_sn = cred_sn

    @classmethod
    def individual(cls):
        return 'domain_org'