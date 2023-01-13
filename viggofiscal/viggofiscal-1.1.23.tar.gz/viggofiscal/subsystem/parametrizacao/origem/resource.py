from enum import Enum
import sqlalchemy
from sqlalchemy import orm, ForeignKeyConstraint

from viggocore.database import db
from viggocore.common.subsystem import entity


class Origem(entity.Entity, db.Model):

    attributes = ['origem', 'descricao']
    attributes += entity.Entity.attributes

    origem = db.Column(db.String(2), nullable=False, unique=True)
    descricao = db.Column(db.String(100), nullable=False)

    def __init__(self, id, origem, descricao,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.origem = origem
        self.descricao = descricao

    @classmethod
    def collection(cls):
        return 'origens'