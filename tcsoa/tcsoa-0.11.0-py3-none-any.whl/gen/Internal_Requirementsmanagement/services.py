from tcsoa.gen.Internal_Requirementsmanagement._2012_10.services import RequirementsManagementService as imp0
from tcsoa.gen.Internal_Requirementsmanagement._2012_02.services import RequirementsManagementService as imp1
from tcsoa.gen.Internal_Requirementsmanagement._2009_10.services import RequirementsManagementService as imp2
from tcsoa.base import TcService


class RequirementsManagementService(TcService):
    getMatchingLines = imp0.getMatchingLines
    getTraceabilityMatrix = imp1.getTraceabilityMatrix
    getTraceabilityMatrix2 = imp0.getTraceabilityMatrix
    importUnmanagedData = imp2.importUnmanagedData
