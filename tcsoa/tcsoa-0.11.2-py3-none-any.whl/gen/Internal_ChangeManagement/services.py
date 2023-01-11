from tcsoa.gen.Internal_ChangeManagement._2015_03.services import ChangeManagementService as imp0
from tcsoa.gen.Internal_ChangeManagement._2012_10.services import ChangeManagementService as imp1
from tcsoa.gen.Internal_ChangeManagement._2020_01.services import MassUpdateService as imp2
from tcsoa.base import TcService


class ChangeManagementService(TcService):
    connectChangeNoticeToContext = imp0.connectChangeNoticeToContext
    createOrUpdatePreviousEffectivity = imp0.createOrUpdatePreviousEffectivity
    disconnectChangeNoticeFromContext = imp0.disconnectChangeNoticeFromContext
    getCreatableChangeTypes = imp1.getCreatableChangeTypes
    removePrevEffectivityFromChgNotice = imp0.removePrevEffectivityFromChgNotice
    updateChangeNoticeRelations = imp0.updateChangeNoticeRelations


class MassUpdateService(TcService):
    hasActiveMarkupAssociated = imp2.hasActiveMarkupAssociated
    saveImpactedAssemblies = imp2.saveImpactedAssemblies
