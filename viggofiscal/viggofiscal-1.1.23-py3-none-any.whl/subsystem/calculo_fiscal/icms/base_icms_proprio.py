from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt


class BaseIcmsProprio():

    def __init__(self, valor_produto: float, valor_frete: float,
                 valor_seguro: float, despesas_acessorias: float,
                 valor_desconto: float, valor_ipi: float=0.0):
        self.valor_produto = float(valor_produto)
        self.valor_frete = float(valor_frete)
        self.valor_seguro = float(valor_seguro)
        self.despesas_acessorias = float(despesas_acessorias)
        self.valor_desconto = float(valor_desconto)
        self.valor_ipi = float(valor_ipi)

    def calcular_base_icms_proprio(self) -> float:
        base_icms_proprio = (
            self.valor_produto + self.valor_frete + self.valor_seguro +
            self.despesas_acessorias + self.valor_ipi - self.valor_desconto)
        return round_abnt(base_icms_proprio, 2)
