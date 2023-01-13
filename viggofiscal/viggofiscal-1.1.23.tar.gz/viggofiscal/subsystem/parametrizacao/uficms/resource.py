from sqlalchemy import UniqueConstraint
from viggocore.database import db
from viggocore.common.subsystem import entity


class Uficms(entity.Entity, db.Model):

    attributes = ['sigla', 'aliq_icms_proprio', 'aliq_icms_st', 'aliq_fcp',
                  'aliq_fcp_st']
    attributes += entity.Entity.attributes

    domain_org_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain_org.id'), nullable=False)

    sigla = db.Column(db.CHAR(2), nullable=False)
    aliq_icms_proprio = db.Column(db.Numeric(5, 2), nullable=False)
    aliq_icms_st = db.Column(db.Numeric(5, 2), nullable=False)
    aliq_fcp = db.Column(db.Numeric(5, 2), nullable=False)
    aliq_fcp_st = db.Column(db.Numeric(5, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint('domain_org_id', 'sigla',
                         name='uficms_domain_org_id_sigla_uk'),)

    def __init__(self, id, domain_org_id, sigla, aliq_icms_proprio, aliq_icms_st,
                 aliq_fcp, aliq_fcp_st,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_org_id = domain_org_id
        self.sigla = sigla
        self.aliq_icms_proprio = aliq_icms_proprio
        self.aliq_icms_st = aliq_icms_st
        self.aliq_fcp = aliq_fcp
        self.aliq_fcp_st = aliq_fcp_st
