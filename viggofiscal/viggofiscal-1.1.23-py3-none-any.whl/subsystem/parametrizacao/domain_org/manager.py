from viggocore.common.subsystem import operation
from viggocore.common.subsystem import manager


class Create(operation.Create):

    def post(self):

        natureza_list = ['Compra', 'Venda', 'Transferência', 'Devolução',
                         'Importação', 'Consignação', 'Outra',
                         'Remessa para fins de demonstração',
                         'Remessa para fins de industrialização']

        domain_org_id = self.entity.id
        if domain_org_id is not None:
            for item in natureza_list:
                natureza = {
                    'domain_org_id': domain_org_id,
                    'titulo': item,
                    'descricao': item
                }
                self.manager.api.natureza_operacaos().create(**natureza)


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.create = Create(self)
