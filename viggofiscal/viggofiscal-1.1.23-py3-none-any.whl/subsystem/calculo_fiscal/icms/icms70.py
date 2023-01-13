from viggofiscal.subsystem.calculo_fiscal.icms.base_reduzida_icms_proprio \
    import BaseReduzidaIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.base_icms_proprio \
    import BaseIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.icms00 \
    import Icms00
from viggofiscal.subsystem.calculo_fiscal.icms.icms10 \
    import Icms10
from viggofiscal.subsystem.calculo_fiscal.icms.valor_icms_proprio \
    import ValorIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt, to_decimal
from viggofiscal.subsystem.calculo_fiscal.icms.base_icms_st \
    import BaseIcmsST
from viggofiscal.subsystem.calculo_fiscal.icms.base_reduzida_icms_st \
    import BaseReduzidaIcmsST
from viggofiscal.subsystem.calculo_fiscal.icms.valor_icms_st \
    import ValorIcmsST


class Icms70():

    def __init__(self, valor_produto: float, valor_frete: float,
                 valor_seguro: float, despesas_acessorias: float,
                 valor_ipi: float, valor_desconto: float,
                 aliq_icms_proprio: float, aliq_icms_st: float,
                 mva: float, percentual_reducao: float,
                 percentual_reducao_st: float=0.0):
        self.valor_produto = float(valor_produto)
        self.valor_frete = float(valor_frete)
        self.valor_seguro = float(valor_seguro)
        self.despesas_acessorias = float(despesas_acessorias)
        self.valor_ipi = float(valor_ipi)
        self.valor_desconto = float(valor_desconto)
        self.aliq_icms_proprio = float(aliq_icms_proprio)
        self.aliq_icms_st = float(aliq_icms_st)
        self.mva = float(mva)
        self.percentual_reducao = float(percentual_reducao)
        self.percentual_reducao_st = float(percentual_reducao_st)
        self.bc_reduzida_icms_proprio = BaseReduzidaIcmsProprio(
            valor_produto, valor_frete, valor_seguro, despesas_acessorias,
            valor_desconto, percentual_reducao)

    # ICMS Próprio
    def base_icms_proprio(self) -> float:
        return self.bc_reduzida_icms_proprio.\
            calcular_base_reduzida_icms_proprio()

    def valor_icms_proprio(self) -> float:
        valor_icms_proprio = ValorIcmsProprio(
            self.base_icms_proprio(), self.aliq_icms_proprio).\
            calcular_valor_icms_proprio()
        return valor_icms_proprio

    def valor_icms_proprio_desonerado(self) -> float:
        icms00 = Icms00(
            self.valor_produto, self.valor_frete, self.valor_seguro,
            self.despesas_acessorias, 0.0, self.valor_desconto,
            self.aliq_icms_proprio)
        valor_icms_normal = icms00.valor_icms_proprio()
        valor_icms_desonerado = valor_icms_normal - self.valor_icms_proprio()
        return round_abnt(valor_icms_desonerado, 2)

    # ICMS ST
    def base_icms_st(self) -> float:
        if self.percentual_reducao_st == 0.0:
            self.bc_icms_st = BaseIcmsST(self.base_icms_proprio(), self.mva,
                                         self.valor_ipi)
            return self.bc_icms_st.calcular_base_icms_st()
        else:
            self.bc_reduzida_icms_st = BaseReduzidaIcmsST(
                self.base_icms_proprio(), self.mva, self.percentual_reducao_st,
                self.valor_ipi)
            return self.bc_reduzida_icms_st.calcular_base_reduzida_icms_st()

    def valor_icms_st(self) -> float:
        valor_icms_st = ValorIcmsST(
            self.base_icms_st(), self.aliq_icms_st, self.valor_icms_proprio()).\
            calcular_valor_icms_st()
        return valor_icms_st
    
    # funções criadas para calcular a base_icms_st sem redução
    def base_icms_st_normal(self) -> float:
        if self.percentual_reducao_st > 0.0:
            valor_ipi = 0.0
        else:
            valor_ipi = self.valor_ipi

        self.bc_icms_st = BaseIcmsST(self.base_icms_proprio(), self.mva,
                                     valor_ipi)
        return self.bc_icms_st.calcular_base_icms_st()
    
    def valor_icms_st_normal(self) -> float:
        valor_icms_st = ValorIcmsST(
            self.base_icms_st_normal(),
            self.aliq_icms_st,
            self.valor_icms_proprio()).\
            calcular_valor_icms_st()
        return valor_icms_st

    def valor_icms_st_desonerado(self) -> float:
        valor_icms_st_normal = self.valor_icms_st_normal()
        valor_icms_st_desonerado = valor_icms_st_normal - self.valor_icms_st()

        return round_abnt(valor_icms_st_desonerado, 2)