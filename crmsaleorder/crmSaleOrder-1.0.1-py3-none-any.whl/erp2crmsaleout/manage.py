from erp2crmsaleout.saleOutToDMS import ERP2CRM
from erp2crmsaleout.salesOutStock import get_data

def run():
    acc = ERP2CRM()
    acc.ERP2DMS()
    res = get_data()
    return res