from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt


class BaseReduzidaIcmsST():

    def __init__(self, base_icms_proprio: float, mva: float,
                 percentual_reducao_st: float,
                 valor_ipi: float=0.0):
        self.base_icms_proprio = float(base_icms_proprio)
        self.mva = float(mva)
        self.percentual_reducao_st = float(percentual_reducao_st)
        self.valor_ipi = float(valor_ipi)

    def calcular_base_reduzida_icms_st(self) -> float:
        base_icms_st = self.base_icms_proprio * (1 + (self.mva / 100))
        base_icms_st = (
            base_icms_st - (base_icms_st * (self.percentual_reducao_st / 100)))
        base_reduzida_icms_st = base_icms_st + self.valor_ipi
        return round_abnt(base_reduzida_icms_st, 2)
