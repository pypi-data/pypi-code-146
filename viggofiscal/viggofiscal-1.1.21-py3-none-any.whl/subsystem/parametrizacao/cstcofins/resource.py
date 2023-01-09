from viggocore.database import db
from viggocore.common.subsystem import entity


class Cstcofins(entity.Entity, db.Model):

    attributes = ['cst', 'descricao']
    attributes += entity.Entity.attributes

    cst = db.Column(db.String(5), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.Numeric(1), nullable=False)

    def __init__(self, id, cst, descricao, tipo,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.cst = cst
        self.descricao = descricao
        self.tipo = tipo