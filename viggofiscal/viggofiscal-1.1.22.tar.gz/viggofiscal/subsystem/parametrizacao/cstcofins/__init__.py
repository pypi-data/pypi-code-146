from viggocore.common import subsystem
from viggofiscal.subsystem.parametrizacao.cstcofins \
    import resource, manager, controller

subsystem = subsystem.Subsystem(resource=resource.Cstcofins,
                                manager=manager.Manager,
                                controller=controller.Controller)
