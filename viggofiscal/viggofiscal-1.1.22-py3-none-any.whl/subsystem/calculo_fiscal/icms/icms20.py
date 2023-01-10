from viggofiscal.subsystem.calculo_fiscal.icms.base_reduzida_icms_proprio \
    import BaseReduzidaIcmsProprio
from viggofiscal.subsystem.calculo_fiscal.icms.icms00 \
    import Icms00
from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt


class Icms20():

    def __init__(self, valor_produto: float, valor_frete: float,
                 valor_seguro: float, despesas_acessorias: float,
                 valor_ipi: float, valor_desconto: float,
                 aliq_icms_proprio: float, percentual_reducao: float):
        self.valor_produto = float(valor_produto)
        self.valor_frete = float(valor_frete)
        self.valor_seguro = float(valor_seguro)
        self.despesas_acessorias = float(despesas_acessorias)
        self.valor_ipi = float(valor_ipi)
        self.valor_desconto = float(valor_desconto)
        self.aliq_icms_proprio = float(aliq_icms_proprio)
        self.percentual_reducao = float(percentual_reducao)
        self.base_reduzida_icms = BaseReduzidaIcmsProprio(
            valor_produto, valor_frete, valor_seguro, despesas_acessorias,
            valor_desconto, percentual_reducao, valor_ipi)

    def calcular_bc_icms(self) -> float:
        return self.base_reduzida_icms.calcular_bc_icms()

    def base_reduzida_icms_proprio(self):
        return self.base_reduzida_icms.calcular_base_reduzida_icms_proprio()

    def valor_icms_proprio(self) -> float:
        base_reduzida_icms = self.base_reduzida_icms_proprio()
        valor_icms = base_reduzida_icms * (self.aliq_icms_proprio / 100)
        return round_abnt(valor_icms, 2)

    def valor_icms_desonerado(self) -> float:
        icms00 = Icms00(
            self.valor_produto,
            self.valor_frete, self.valor_seguro, self.despesas_acessorias,
            0, self.valor_desconto, self.aliq_icms_proprio)

        valor_icms_normal = icms00.valor_icms_proprio()
        valor_icms_desonerado = valor_icms_normal - self.valor_icms_proprio()
        return round_abnt(valor_icms_desonerado, 2)