from viggocore.common import subsystem
from viggofiscal.subsystem.parametrizacao.forma_pagamento_sefaz \
    import resource, router

subsystem = subsystem.Subsystem(resource=resource.FormaPagamentoSefaz,
                                router=router.Router)
