from viggocore.common import subsystem
from viggofiscal.subsystem.parametrizacao.csticms \
    import resource, manager, controller

subsystem = subsystem.Subsystem(resource=resource.Csticms,
                                manager=manager.Manager,
                                controller=controller.Controller)
