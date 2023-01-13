from viggocore.database import db
from viggocore.common.subsystem import entity


class Cfop(entity.Entity, db.Model):

    attributes = ['cfop', 'descricao', 'observacao', 'tipo']
    attributes += entity.Entity.attributes

    cfop = db.Column(db.String(5), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=False)
    observacao = db.Column(db.String(800), nullable=False)
    tipo = db.Column(db.Numeric(1), nullable=False)

    def __init__(self, id, cfop, descricao, observacao, tipo,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.cfop = cfop
        self.descricao = descricao
        self.observacao = observacao
        self.tipo = tipo