from viggofiscal.subsystem.calculo_fiscal.icms.base_reduzida_icms_proprio \
    import BaseReduzidaIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.base_icms_proprio \
    import BaseIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.icms00 \
    import Icms00
from viggofiscal.subsystem.calculo_fiscal.icms.valor_icms_proprio \
    import ValorIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt, to_decimal


class Icms51():

    def __init__(self, valor_produto: float, valor_frete: float,
                 valor_seguro: float, despesas_acessorias: float,
                 valor_ipi: float, valor_desconto: float,
                 aliq_icms_proprio: float, percentual_reducao: float,
                 percentual_diferimento: float):
        self.valor_produto = float(valor_produto)
        self.valor_frete = float(valor_frete)
        self.valor_seguro = float(valor_seguro)
        self.despesas_acessorias = float(despesas_acessorias)
        self.valor_ipi = float(valor_ipi)
        self.valor_desconto = float(valor_desconto)
        self.aliq_icms_proprio = float(aliq_icms_proprio)
        self.percentual_reducao = float(percentual_reducao)
        self.percentual_diferimento = float(percentual_diferimento)

    def base_icms_proprio(self):
        if self.percentual_reducao == 0:
            self.bc_icms_proprio = BaseIcmsProprio(
                self.valor_produto, self.valor_frete, self.valor_seguro,
                self.despesas_acessorias, self.valor_desconto, self.valor_ipi)
            return self.bc_icms_proprio.calcular_base_icms_proprio()
        else:
            self.bc_reduzida_icms_proprio = BaseReduzidaIcmsProprio(
                self.valor_produto, self.valor_frete, self.valor_seguro,
                self.despesas_acessorias, self.valor_desconto,
                self.percentual_reducao, self.valor_ipi)
            return self.bc_reduzida_icms_proprio.\
                calcular_base_reduzida_icms_proprio()

    def valor_icms_operacao(self) -> float:
        return ValorIcmsProprio(
            self.base_icms_proprio(), self.aliq_icms_proprio).\
                calcular_valor_icms_proprio()

    def valor_icms_diferido(self) -> float:
        valor_icms_operacao = self.valor_icms_operacao()
        valor_icms_diferido = (
            valor_icms_operacao * (self.percentual_diferimento / 100))
        return round_abnt(valor_icms_diferido, 2)

    def valor_icms_proprio(self) -> float:
        valor_icms_proprio = (
            self.valor_icms_operacao() - self.valor_icms_diferido())
        return round_abnt(valor_icms_proprio, 2)
