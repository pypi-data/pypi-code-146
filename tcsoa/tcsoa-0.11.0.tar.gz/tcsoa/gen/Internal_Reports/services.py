from tcsoa.gen.Internal_Reports._2007_06.services import BOMRollupService as imp0
from tcsoa.base import TcService


class BOMRollupService(TcService):
    cloneRollupTemplates = imp0.cloneRollupTemplates
    createRollupCalculationTemplates = imp0.createRollupCalculationTemplates
    createRollupTemplates = imp0.createRollupTemplates
    generateRollupReports = imp0.generateRollupReports
    getRollupTemplateCalculations = imp0.getRollupTemplateCalculations
    getRollupTemplates = imp0.getRollupTemplates
    reviseRollupReports = imp0.reviseRollupReports
