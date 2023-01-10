from viggocore.database import db
from viggocore.common.subsystem import entity


class NaturezaOperacao(entity.Entity, db.Model):

    attributes = ['titulo', 'descricao']
    attributes += entity.Entity.attributes

    domain_org_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain_org.id'), nullable=False)

    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)

    def __init__(self, id, domain_org_id, titulo, descricao,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_org_id = domain_org_id
        self.titulo = titulo
        self.descricao = descricao

    @classmethod
    def individual(cls):
        return 'natureza_operacao'
