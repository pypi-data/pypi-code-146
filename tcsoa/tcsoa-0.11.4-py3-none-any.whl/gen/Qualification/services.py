from tcsoa.gen.Qualification._2014_06.services import QualificationManagementService as imp0
from tcsoa.base import TcService


class QualificationManagementService(TcService):
    appendQualificationLevel = imp0.appendQualificationLevel
    assignUserQualification = imp0.assignUserQualification
    createQualification = imp0.createQualification
    removeQualificationLevel = imp0.removeQualificationLevel
    removeUserQualification = imp0.removeUserQualification
    updateQualification = imp0.updateQualification
