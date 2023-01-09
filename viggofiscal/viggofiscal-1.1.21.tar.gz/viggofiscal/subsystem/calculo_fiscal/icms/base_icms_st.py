from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt


class BaseIcmsST():

    def __init__(self, base_icms_proprio: float, mva: float,
                 valor_ipi: float=0.0):
        self.base_icms_proprio = float(base_icms_proprio)
        self.mva = float(mva)
        self.valor_ipi = float(valor_ipi)

    def calcular_base_icms_st(self) -> float:
        base_icms_st = (
            (self.base_icms_proprio + self.valor_ipi) * (1 + (self.mva / 100)))
        return round_abnt(base_icms_st, 2)
