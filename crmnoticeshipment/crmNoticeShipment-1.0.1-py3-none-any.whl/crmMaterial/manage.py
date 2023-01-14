import datetime

from pyrda.dbms.rds import RdClient

from crmMaterial.src_crm_material import ERPTOCrm


def run():
    c = ERPTOCrm()
    token_erp = 'B405719A-772E-4DF9-A560-C24948A3A5D6'
    app3 = RdClient(token=token_erp)
    FDate = '2023-01-04'
    c.proto_crm(app3, FDate)

print(run())