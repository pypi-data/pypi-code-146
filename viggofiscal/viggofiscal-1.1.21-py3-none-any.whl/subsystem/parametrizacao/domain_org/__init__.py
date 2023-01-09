from viggocore.common import subsystem
from viggofiscal.subsystem.parametrizacao.domain_org \
    import resource, manager

subsystem = subsystem.Subsystem(resource=resource.DomainOrg,
                                manager=manager.Manager)