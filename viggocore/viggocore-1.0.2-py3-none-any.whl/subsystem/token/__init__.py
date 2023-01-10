from viggocore.common import subsystem
from viggocore.subsystem.token import manager
from viggocore.subsystem.token import resource
from viggocore.subsystem.token import router

subsystem = subsystem.Subsystem(resource=resource.Token,
                                manager=manager.Manager,
                                router=router.Router)
