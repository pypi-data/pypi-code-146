import math

from . import (
    lgbm,
    xgb
)


def get_n_estimators(learner):
    if isinstance(learner, lgbm.LGBMClassifier):
        num_classes = len(learner._classes)
        return int(math.ceil(learner.booster_.num_trees() / (num_classes - 1)))
    elif isinstance(learner, lgbm.LGBMRegressor):
        return learner.booster_.num_trees()
    elif isinstance(learner, xgb.XGBClassifier) or isinstance(learner, xgb.XGBRegressor):
        return learner.best_iteration
