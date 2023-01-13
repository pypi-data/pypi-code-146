from .gaminet import GAMINetClassifier, GAMINetRegressor
from .ebm_module import ExplainableBoostingRegressor, ExplainableBoostingClassifier, EBMExplainer
from .reludnn import ReluDNNClassifier, ReluDNNRegressor, UnwrapperRegressor, UnwrapperClassifier
from .gam import GAMRegressor, GAMClassifier
from .glm import GLMRegressor, GLMClassifier
from .dt import PiDecisionTreeClassifier, PiDecisionTreeRegressor
from .xgb.xgboost import PiXGBClassifier, PiXGBRegressor
from .figs import FIGSClassifier, FIGSRegressor
from xgboost import XGBRegressor, XGBClassifier

__all__ = ["UnwrapperRegressor", "UnwrapperClassifier", 'GAMINetClassifier', 'GAMINetRegressor',
            'ExplainableBoostingRegressor', 'ExplainableBoostingClassifier', 'EBMExplainer',
            'ReluDNNClassifier', 'ReluDNNRegressor', "GAMRegressor", "GAMClassifier", "GLMRegressor",
            "GLMClassifier", 'PiDecisionTreeClassifier', 'PiDecisionTreeRegressor',
            'PiXGBClassifier', 'PiXGBRegressor', 'XGBRegressor', 'XGBClassifier', 'FIGSClassifier', 'FIGSRegressor']


def get_all_supported_models():
    return sorted(__all__)
