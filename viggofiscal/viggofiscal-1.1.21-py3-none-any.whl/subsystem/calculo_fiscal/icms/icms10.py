from viggofiscal.subsystem.calculo_fiscal.icms.base_reduzida_icms_proprio \
    import BaseReduzidaIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.base_icms_proprio \
    import BaseIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.icms00 \
    import Icms00
from viggofiscal.subsystem.calculo_fiscal.icms.valor_icms_proprio \
    import ValorIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt
from viggofiscal.subsystem.calculo_fiscal.icms.base_icms_st \
    import BaseIcmsST
from viggofiscal.subsystem.calculo_fiscal.icms.base_reduzida_icms_st \
    import BaseReduzidaIcmsST
from viggofiscal.subsystem.calculo_fiscal.icms.valor_icms_st \
    import ValorIcmsST


class Icms10():

    def __init__(self, valor_produto: float, valor_frete: float,
                 valor_seguro: float, despesas_acessorias: float,
                 valor_ipi: float, valor_desconto: float,
                 aliq_icms_proprio: float, aliq_icms_st: float,
                 mva: float, percentual_reducao_st: float=0.0):
        self.valor_produto = float(valor_produto)
        self.valor_frete = float(valor_frete)
        self.valor_seguro = float(valor_seguro)
        self.despesas_acessorias = float(despesas_acessorias)
        self.valor_ipi = float(valor_ipi)
        self.valor_desconto = float(valor_desconto)
        self.aliq_icms_proprio = float(aliq_icms_proprio)
        self.aliq_icms_st = float(aliq_icms_st)
        self.mva = float(mva)
        self.percentual_reducao_st = float(percentual_reducao_st)
        self.bc_icms_proprio = BaseIcmsProprio(
            valor_produto, valor_frete, valor_seguro, despesas_acessorias,
            valor_desconto)

    # ICMS Próprio
    def base_icms_proprio(self) -> float:
        return self.bc_icms_proprio.calcular_base_icms_proprio()

    def valor_icms_proprio(self) -> float:
        base_icms_proprio = self.base_icms_proprio()
        valor_icms_proprio = ValorIcmsProprio(
            base_icms_proprio, self.aliq_icms_proprio).\
            calcular_valor_icms_proprio()
        return valor_icms_proprio

    def valor_icms_desonerado(self) -> float:
        return self.valor_icms_proprio()

    # ICMS ST
    def base_icms_st(self) -> float:
        if self.percentual_reducao_st == float('0.0'):
            self.bc_icms_st = BaseIcmsST(self.base_icms_proprio(), self.mva,
                                         self.valor_ipi)
            return self.bc_icms_st.calcular_base_icms_st()
        else:
            self.bc_reduzida_icms_st = BaseReduzidaIcmsST(
                self.base_icms_proprio(), self.mva, self.percentual_reducao_st,
                self.valor_ipi)
            return self.bc_reduzida_icms_st.calcular_base_reduzida_icms_st()
    
    def base_icms_st_normal(self) -> float:
        self.bc_icms_st = BaseIcmsST(
            self.base_icms_proprio(), self.mva, 0.0)
        return self.bc_icms_st.calcular_base_icms_st()

    def valor_icms_st_normal(self, base_icms_st: float) -> float:
        base_icms_st = base_icms_st
        valor_icms_st = ValorIcmsST(
            base_icms_st, self.aliq_icms_st, self.valor_icms_proprio()).\
            calcular_valor_icms_st()
        return valor_icms_st

    def valor_icms_st(self) -> float:
        valor_icms_st = self.valor_icms_st_normal(self.base_icms_st())
        return valor_icms_st

    def valor_icms_st_desonerado(self) -> float:
        valor_icms_st_normal = self.valor_icms_st_normal(
            self.base_icms_st_normal())
        valor_icms_st_desonerado = valor_icms_st_normal - self.valor_icms_st()
        return round_abnt(valor_icms_st_desonerado, 2)