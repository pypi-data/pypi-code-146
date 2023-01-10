from enum import Enum
import sqlalchemy
from sqlalchemy import orm, ForeignKeyConstraint

from viggocore.database import db
from viggocore.common.subsystem import entity


class NcmIbpt(entity.Entity, db.Model):

    attributes = ['ncm', 'uf', 'chave', 'versao', 'descricao', 'extipi',
                  'aliq_nacional', 'aliq_importacao', 'aliq_estadual',
                  'aliq_municipal', 'inicio_vigencia', 'fim_vigencia']
    attributes += entity.Entity.attributes

    ncm = db.Column(db.Numeric(8), nullable=False)
    uf = db.Column(db.CHAR(2), nullable=False)
    chave = db.Column(db.String(100), nullable=False)
    versao = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    aliq_nacional = db.Column(db.Numeric(5, 2), nullable=False)
    aliq_importacao = db.Column(db.Numeric(5, 2), nullable=False)
    aliq_estadual = db.Column(db.Numeric(5, 2), nullable=False)
    aliq_municipal = db.Column(db.Numeric(5, 2), nullable=False)
    inicio_vigencia = db.Column(db.Date(), nullable=False)
    fim_vigencia = db.Column(db.Date(), nullable=False)
    extipi = db.Column(db.Numeric(), nullable=True)

    def __init__(self, id, ncm, uf, chave, versao, descricao, 
                 aliq_nacional, aliq_importacao, aliq_estadual,
                 aliq_municipal, inicio_vigencia, fim_vigencia,
                 extipi=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.ncm = ncm
        self.uf = uf
        self.chave = chave
        self.versao = versao
        self.descricao = descricao
        self.aliq_nacional = aliq_nacional
        self.aliq_importacao = aliq_importacao
        self.aliq_estadual = aliq_estadual
        self.aliq_municipal = aliq_municipal
        self.inicio_vigencia = inicio_vigencia
        self.fim_vigencia = fim_vigencia
        self.extipi = extipi
