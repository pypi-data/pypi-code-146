from tcsoa.gen.BusinessModeler._2008_06.services import ConditionEngineService as imp0
from tcsoa.gen.BusinessModeler._2007_06.services import RulesBasedFrameworkService as imp1
from tcsoa.gen.BusinessModeler._2008_06.services import DeepCopyRulesService as imp2
from tcsoa.gen.BusinessModeler._2007_06.services import ConstantsService as imp3
from tcsoa.gen.BusinessModeler._2011_06.services import ConstantsService as imp4
from tcsoa.gen.BusinessModeler._2010_04.services import BusinessRulesService as imp5
from tcsoa.base import TcService


class ConditionEngineService(TcService):
    evaluateConditions = imp0.evaluateConditions


class RulesBasedFrameworkService(TcService):
    executeRbfRules = imp1.executeRbfRules


class DeepCopyRulesService(TcService):
    getDeepCopyInfo = imp2.getDeepCopyInfo


class ConstantsService(TcService):
    getGlobalConstantValues = imp3.getGlobalConstantValues
    getGlobalConstantValues2 = imp4.getGlobalConstantValues2
    getPropertyConstantValues = imp3.getPropertyConstantValues
    getTypeConstantValues = imp3.getTypeConstantValues


class BusinessRulesService(TcService):
    getVerificationRules = imp5.getVerificationRules
