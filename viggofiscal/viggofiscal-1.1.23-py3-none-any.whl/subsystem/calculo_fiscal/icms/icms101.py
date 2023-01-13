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


class Icms101():

    def __init__(self, valor_produto: float, valor_frete: float,
                 valor_seguro: float, despesas_acessorias: float,
                 valor_desconto: float, percentual_credito_sn: float,
                 percentual_reducao: float=0.0):
        self.valor_produto = float(valor_produto)
        self.valor_frete = float(valor_frete)
        self.valor_seguro = float(valor_seguro)
        self.despesas_acessorias = float(despesas_acessorias)
        self.valor_desconto = float(valor_desconto)
        self.percentual_credito_sn = float(percentual_credito_sn)
        self.percentual_reducao = float(percentual_reducao)

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

    def valor_credito_sn(self):
        valor_credito_sn = (
            self.base_icms_proprio() * (self.percentual_credito_sn / 100))
        return round_abnt(valor_credito_sn, 2)
