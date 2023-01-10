from viggofiscal.subsystem.calculo_fiscal.icms.base_icms_proprio \
    import BaseIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.valor_icms_proprio \
    import ValorIcmsProprio


class Icms00():

    def __init__(self, valor_produto: float, valor_frete: float,
                 valor_seguro: float, despesas_acessorias: float,
                 valor_ipi: float, valor_desconto: float,
                 aliq_icms_proprio: float):
        self.valor_produto = float(valor_produto)
        self.valor_frete = float(valor_frete)
        self.valor_seguro = float(valor_seguro)
        self.despesas_acessorias = float(despesas_acessorias)
        self.valor_ipi = float(valor_ipi)
        self.valor_desconto = float(valor_desconto)
        self.aliq_icms_proprio = float(aliq_icms_proprio)
        self.base_icms = BaseIcmsProprio(
            valor_produto, valor_frete, valor_seguro, despesas_acessorias,
            valor_desconto, valor_ipi)

    def base_icms_proprio(self):
        return self.base_icms.calcular_base_icms_proprio()

    def valor_icms_proprio(self) -> float:
        return ValorIcmsProprio(
            self.base_icms_proprio(), self.aliq_icms_proprio).\
            calcular_valor_icms_proprio()
