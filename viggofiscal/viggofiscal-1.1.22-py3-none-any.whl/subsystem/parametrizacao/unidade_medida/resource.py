from enum import Enum
import sqlalchemy
from sqlalchemy import orm, ForeignKeyConstraint

from viggocore.database import db
from viggocore.common.subsystem import entity


class UnidadeMedida(entity.Entity, db.Model):

    attributes = ['sigla', 'descricao']
    attributes += entity.Entity.attributes

    sigla = db.Column(db.CHAR(6), nullable=False, unique=True)
    descricao = db.Column(db.String(100), nullable=False)

    def __init__(self, id, sigla, descricao,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.sigla = sigla
        self.descricao = descricao