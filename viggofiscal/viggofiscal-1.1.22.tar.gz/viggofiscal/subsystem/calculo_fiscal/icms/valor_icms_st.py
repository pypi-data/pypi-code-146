from viggofiscal.subsystem.calculo_fiscal.utils import round_abnt, to_decimal


class ValorIcmsST():

    def __init__(self, base_calculo_st: float, aliq_icms_st: float,
                 valor_icms_proprio: float):
        self.base_calculo_st = float(base_calculo_st)
        self.aliq_icms_st = float(aliq_icms_st)
        self.valor_icms_proprio = float(valor_icms_proprio)

    def calcular_valor_icms_st(self):
        valor_icms_st = (
            (self.base_calculo_st * (self.aliq_icms_st / 100)) - 
            self.valor_icms_proprio)
        return round_abnt(valor_icms_st, 2)
