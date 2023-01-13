from enum import Enum, IntEnum
import sqlalchemy
from sqlalchemy import orm
from viggocore.database import db
from viggocore.common.subsystem import entity
from viggocore.common import exception


class TipoIpi(Enum):
    AD_VALOREM = 'AD_VALOREM'
    ESPECIFICA = 'ESPECIFICA'


class RegraFiscalModelo(IntEnum):
    NFE = 55
    NFCE = 65


class RegraFiscal(entity.Entity, db.Model):

    attributes = ['domain_org_id', 'cstcofins_id', 'csticms_id', 'cstpis_id',
                  'cfop_id', 'cstipi_id', 'descricao', 'aliq_especifica_icms',
                  'aliq_especifica_icms_st', 'aliq_reducao_base_icms',
                  'aliq_reducao_base_st', 'aliq_diferimento', 'indice_difal',
                  'difal_base_dupla', 'icms_sob_pis_cofins', 'icms_sob_frete',
                  'tipo_ipi', 'icms_sob_ipi', 'codigo_cst_icms',
                  'codigo_cst_pis', 'codigo_cfop', 'codigo_cst_ipi',
                  'codigo_cst_cofins', 'mod_bc', 'mod_bc_st', 'gera_receita',
                  'gera_estoque', 'cst_icms_trabalha_st', 'modelo',
                  'numero_modelo']
    attributes += entity.Entity.attributes

    domain_org_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain_org.id'), nullable=False)
    cstcofins_id = db.Column(
        db.CHAR(32), db.ForeignKey('cstcofins.id'), nullable=False)
    cstcofins = orm.relationship('Cstcofins', backref=orm.backref('cstcofinss'))
    csticms_id = db.Column(
        db.CHAR(32), db.ForeignKey('csticms.id'), nullable=False)
    csticms = orm.relationship('Csticms', backref=orm.backref('csticmss'))
    cstpis_id = db.Column(
        db.CHAR(32), db.ForeignKey('cstpis.id'), nullable=False)
    cstpis = orm.relationship('Cstpis', backref=orm.backref('cstpiss'))
    cfop_id = db.Column(
        db.CHAR(32), db.ForeignKey('cfop.id'), nullable=False)
    cfop = orm.relationship('Cfop', backref=orm.backref('cfops'))
    cstipi_id = db.Column(
        db.CHAR(32), db.ForeignKey('cstipi.id'), nullable=True)
    cstipi = orm.relationship('Cstipi', backref=orm.backref('cstipis'))

    descricao = db.Column(db.String(100), nullable=False)
    aliq_especifica_icms = db.Column(
        db.Numeric(5, 2), nullable=False, default=0, server_default="0")
    aliq_especifica_icms_st = db.Column(
        db.Numeric(5, 2), nullable=False, default=0, server_default="0")
    aliq_reducao_base_icms = db.Column(
        db.Numeric(5, 2), nullable=False, default=0, server_default="0")
    aliq_reducao_base_st = db.Column(
        db.Numeric(5, 2), nullable=False, default=0, server_default="0")
    aliq_diferimento = db.Column(
        db.Numeric(5, 2), nullable=False, default=0, server_default="0")
    indice_difal = db.Column(db.Boolean, nullable=False)
    difal_base_dupla = db.Column(db.Boolean, nullable=False)
    icms_sob_pis_cofins = db.Column(db.Boolean, nullable=False)
    icms_sob_frete = db.Column(db.Boolean, nullable=False)
    tipo_ipi = db.Column(sqlalchemy.Enum(TipoIpi), nullable=True)
    
    icms_sob_ipi = db.Column(db.Boolean, nullable=True)

    mod_bc = db.Column(db.Numeric(1), nullable=True)
    mod_bc_st = db.Column(db.Numeric(1), nullable=True)

    gera_receita = db.Column(
        db.Boolean, nullable=False, default=False, server_default='false')
    gera_estoque = db.Column(
        db.Boolean, nullable=False, default=False, server_default='false')

    modelo = db.Column(sqlalchemy.Enum(RegraFiscalModelo),
                       nullable=False, server_default='NFE')

    def __init__(self, id, domain_org_id, cstcofins_id, csticms_id,
                 cfop_id, cstipi_id, descricao, indice_difal, difal_base_dupla,
                 icms_sob_pis_cofins, icms_sob_frete, modelo,
                 aliq_especifica_icms=0, aliq_especifica_icms_st=0,
                 aliq_reducao_base_icms=0, aliq_reducao_base_st=0,
                 aliq_diferimento=0, cstpis_id=None, tipo_ipi=None,
                 icms_sob_ipi=None, mod_bc=None, mod_bc_st=None,
                 gera_receita=False, gera_estoque=False,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_org_id = domain_org_id
        self.cstcofins_id = cstcofins_id
        self.csticms_id = csticms_id
        self.cfop_id = cfop_id
        self.cstipi_id = cstipi_id
        self.descricao = descricao
        self.aliq_especifica_icms = float(aliq_especifica_icms)
        self.aliq_especifica_icms_st = float(aliq_especifica_icms_st)
        self.aliq_reducao_base_icms = float(aliq_reducao_base_icms)
        self.aliq_reducao_base_st = float(aliq_reducao_base_st)
        self.indice_difal = indice_difal
        self.difal_base_dupla = difal_base_dupla
        self.icms_sob_pis_cofins = icms_sob_pis_cofins
        self.icms_sob_frete = icms_sob_frete
        self.cstpis_id = cstpis_id
        self.tipo_ipi = tipo_ipi
        self.icms_sob_ipi = icms_sob_ipi
        self.aliq_diferimento = float(aliq_diferimento)
        self.mod_bc = mod_bc
        self.mod_bc_st = mod_bc_st
        self.gera_receita = gera_receita
        self.gera_estoque = gera_estoque
        self.modelo = modelo

    def is_stable(self):
        # validação se icms_sob_ipi
        if (self.icms_sob_ipi is True and
            (self.tipo_ipi is None and self.cstipi_id is None)):
            raise exception.BadRequest('Se icms_sob_ipi é verdadeiro então' +
                'tipo_ipi e cstipi_id devem ser informados.')

        # TODO(JorgeSilva): verificar como fazer essas validações do tipo de
        # icms pois na criação eu ainda n tenho os backrefs.
        # # validações por tipo de icms
        # if self.csticms.cstcsosn == 20 and self.aliq_reducao_base_icms <= 0:
        #     raise exception.BadRequest('Se o cst_icms for igual a 20 a ' +
        #         'aliq_reducao_base_icms tem que ser maior que zero.')
        # elif self.csticms.cstcsosn == 51 and self.aliq_diferimento <= 0:
        #     raise exception.BadRequest('Se o cst_icms for igual a 51 a ' +
        #         'aliq_diferimento tem que ser maior que zero.')
        return True

    @property
    def codigo_cst_icms(self):
        return self.csticms.cstcsosn

    @property
    def codigo_cst_cofins(self):
        return self.cstcofins.cst

    @property
    def codigo_cst_pis(self):
        return self.cstpis.cst

    @property
    def codigo_cfop(self):
        return self.cfop.cfop

    @property
    def codigo_cst_ipi(self):
        if self.cstipi is None:
            return None
        return self.cstipi.cst

    @property
    def cst_icms_trabalha_st(self):
        return self.csticms.trabalha_st

    @property
    def numero_modelo(self):
        return self.modelo.value

    @classmethod
    def individual(cls):
        return 'regra_fiscal'
