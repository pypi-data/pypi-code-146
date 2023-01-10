from viggocore.common import subsystem, controller
from viggofiscal.subsystem.parametrizacao.tipo_operacao \
    import resource, manager

subsystem = subsystem.Subsystem(resource=resource.TipoOperacao,
                                manager=manager.Manager,
                                controller=controller.CommonController)
