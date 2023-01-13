from viggofiscal.subsystem.calculo_fiscal.icms.base_reduzida_icms_proprio \
    import BaseReduzidaIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.base_icms_proprio \
    import BaseIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.icms00 \
    import Icms00
from viggofiscal.subsystem.calculo_fiscal.icms.valor_icms_proprio \
    import ValorIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt, to_decimal
from viggofiscal.subsystem.calculo_fiscal.icms.base_icms_st \
    import BaseIcmsST
from viggofiscal.subsystem.calculo_fiscal.icms.base_reduzida_icms_st \
    import BaseReduzidaIcmsST
from viggofiscal.subsystem.calculo_fiscal.icms.valor_icms_st \
    import ValorIcmsST


class Icms201():

    def __init__(self, valor_produto: float, valor_frete: float,
                 valor_seguro: float, despesas_acessorias: float,
                 valor_desconto: float, aliq_icms_proprio: float,
                 aliq_icms_st: float, mva: float,
                 percentual_credito_sn: float,
                 percentual_reducao: float=0.0,
                 percentual_reducao_st: float=0.0):
        self.valor_produto = float(valor_produto)
        self.valor_frete = float(valor_frete)
        self.valor_seguro = float(valor_seguro)
        self.despesas_acessorias = float(despesas_acessorias)
        self.valor_desconto = float(valor_desconto)
        self.aliq_icms_proprio = float(aliq_icms_proprio)
        self.aliq_icms_st = float(aliq_icms_st)
        self.mva = float(mva)
        self.percentual_credito_sn = float(percentual_credito_sn)
        self.percentual_reducao = float(percentual_reducao)
        self.percentual_reducao_st = float(percentual_reducao_st)

    # ICMS Próprio
    def base_icms_proprio(self):
        if self.percentual_reducao == 0:
            self.bc_icms_proprio = BaseIcmsProprio(
                self.valor_produto, self.valor_frete, self.valor_seguro,
                self.despesas_acessorias, self.valor_desconto)
            return self.bc_icms_proprio.calcular_base_icms_proprio()
        else:
            self.bc_reduzida_icms_proprio = BaseReduzidaIcmsProprio(
                self.valor_produto, self.valor_frete, self.valor_seguro,
                self.despesas_acessorias, self.valor_desconto,
                self.percentual_reducao)
            return self.bc_reduzida_icms_proprio.\
                calcular_base_reduzida_icms_proprio()

    def valor_icms_proprio(self):
        valor_icms_proprio = ValorIcmsProprio(
            self.base_icms_proprio(), self.aliq_icms_proprio).\
            calcular_valor_icms_proprio()
        return valor_icms_proprio

    def valor_credito_sn(self):
        valor_credito_sn = (
            self.base_icms_proprio() * (self.percentual_credito_sn / 100))
        return round_abnt(valor_credito_sn, 2)

    # ICMS ST
    def base_icms_st(self) -> float:
        if self.percentual_reducao_st == 0.0:
            self.bc_icms_st = BaseIcmsST(self.base_icms_proprio(), self.mva)
            return self.bc_icms_st.calcular_base_icms_st()
        else:
            self.bc_reduzida_icms_st = BaseReduzidaIcmsST(
                self.base_icms_proprio(), self.mva, self.percentual_reducao_st)
            return self.bc_reduzida_icms_st.calcular_base_reduzida_icms_st()

    def valor_icms_st(self) -> float:
        valor_icms_st = ValorIcmsST(
            self.base_icms_st(), self.aliq_icms_st, self.valor_icms_proprio()).\
            calcular_valor_icms_st()
        return valor_icms_st
