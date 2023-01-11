from tcsoa.gen.Internal_Validation._2007_06.services import ValidationService as imp0
from tcsoa.gen.Internal_Validation._2012_02.services import ValidationService as imp1
from tcsoa.gen.Internal_Validation._2008_06.services import ValidationService as imp2
from tcsoa.gen.Internal_Validation._2010_04.services import ValidationService as imp3
from tcsoa.base import TcService


class ValidationService(TcService):
    createOrUpdateValidationAgents = imp0.createOrUpdateValidationAgents
    createOrUpdateValidationData = imp0.createOrUpdateValidationData
    createOrUpdateValidationResults = imp0.createOrUpdateValidationResults
    createOrUpdateValidationResults2 = imp1.createOrUpdateValidationResults2
    evaluateValidationResultsWithRules = imp2.evaluateValidationResultsWithRules
    getValidationResults = imp0.getValidationResults
    getValidationResults2 = imp3.getValidationResults2
    getValidationTargets = imp3.getValidationTargets
    parseRequirementExpressions = imp2.parseRequirementExpressions
    performActionOnOverrideApproval = imp1.performActionOnOverrideApproval
    runValidation = imp3.runValidation
