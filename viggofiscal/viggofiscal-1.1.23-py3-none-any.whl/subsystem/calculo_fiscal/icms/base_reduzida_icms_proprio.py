from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt


class BaseReduzidaIcmsProprio():

    def __init__(self, valor_produto: float, valor_frete: float,
                 valor_seguro: float, despesas_acessorias: float,
                 valor_desconto: float, percentual_reducao: float,
                 valor_ipi: float=0.0):
        self.valor_produto = float(valor_produto)
        self.valor_frete = float(valor_frete)
        self.valor_seguro = float(valor_seguro)
        self.despesas_acessorias = float(despesas_acessorias)
        self.valor_desconto = float(valor_desconto)
        self.percentual_reducao = float(percentual_reducao)
        self.valor_ipi = float(valor_ipi)

    def calcular_bc_icms(self) -> float:
        return (
            self.valor_produto + self.valor_frete + self.valor_seguro +
            self.despesas_acessorias - self.valor_desconto)

    def calcular_base_reduzida_icms_proprio(self) -> float:
        base_icms = self.calcular_bc_icms()
        base_reduzida_icms_proprio = (
            base_icms - (base_icms * (self.percentual_reducao / 100)) +
            self.valor_ipi)
        return round_abnt(base_reduzida_icms_proprio, 2)
