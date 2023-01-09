from viggocore.common import subsystem
from viggofiscal.subsystem.parametrizacao.cstpis \
    import resource, manager, controller

subsystem = subsystem.Subsystem(resource=resource.Cstpis,
                                manager=manager.Manager,
                                controller=controller.Controller)
