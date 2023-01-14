from erptocrmsaleic.saleicSaveCrm import get_data
from erptocrmsaleic.salesicToCRM import ERP2CRM

def run():
    acc = ERP2CRM()
    acc.ERP2DMS()
    res = get_data()
    return res

print(run())