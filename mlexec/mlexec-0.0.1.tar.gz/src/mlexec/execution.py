import gc

import pandas as pd

from .preprocessing.prep_train_data import DFPreprocessor
from .tuning.model_assembly import ModelAssembler
from .evaluation.evaluate import ModelEvaluator

class MLExecutor(DFPreprocessor, ModelAssembler, ModelEvaluator):
    """
    Master Executor class to perform end to end ML
    """
    def __init__(self, 
                df:pd.DataFrame,
                target_col: str,
                task:str="classification",
                encode_opt:str="one-hot",
                continuous_cols:list=[],
                high_cardinality_cols:list=[],
                low_cardinality_cols:list=[],
                exclude_cols:list=[],
                categorical_threshold=0.05,
                cardinality_threshold:int=5,
                continuous_impute_method="mean",
                model_list=["lgb","rf","xgb"],
                metric:str=None,
                model_save_path:str=".",
                normalize:bool=True,
                class_weights:dict={0:1, 1:1},
                tune_flag:bool=True,
                cv:str="basic",
                n_fold:int=5,
                internal_val:bool=False,
                final_train_flag:bool=True,
                max_evals:int=10):
        # preprocessing data
        DFPreprocessor.__init__(self,
                                df,
                                target_col,
                                task,
                                encode_opt,
                                model_save_path=model_save_path,
                                continuous_cols=continuous_cols,
                                high_cardinality_cols=high_cardinality_cols,
                                low_cardinality_cols=low_cardinality_cols,
                                exclude_cols=exclude_cols,
                                categorical_threshold=categorical_threshold,
                                cardinality_threshold=cardinality_threshold,
                                continuous_impute_method=continuous_impute_method)
        x_train, x_test, y_train, y_test = self.prepare_data()
        
        # performing tuning and model training
        ModelAssembler.__init__(self,
                                x_train=x_train,
                                y_train=y_train,
                                model_list=model_list,
                                metric=metric,
                                task=task,
                                normalize=normalize,
                                class_weights=class_weights,
                                tune_flag=tune_flag,
                                cv=cv,
                                n_fold=n_fold,
                                internal_val=internal_val,
                                final_train_flag=final_train_flag)
        self.run_tuning(max_evals=max_evals)

        ModelEvaluator.__init__(self, 
                        x_test=x_test,
                        y_test=y_test,
                        optimization_criterion="f1_score")
        
        self.val_results = self.get_val_scores()
        self.test_results = self.evaluate(find_best_threshold=False)