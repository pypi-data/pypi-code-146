import datacollector_ECB
import datacollector_ICE
import datacollector_Boliga
import datacollector_Business_insider
import datacollector_Entsoe
import datacollector_energidataservice


class ECB(datacollector_ECB.ECB):
    pass

class ICE(datacollector_ICE.ICE):
    pass

class Entsoe(datacollector_Entsoe.Entsoe):
    pass

class Boliga(datacollector_Boliga.Boliga):
    pass

class Business_insider(datacollector_Business_insider.Business_insider):
    pass

class Energidataservice(datacollector_energidataservice.Energidataservice):
    pass

