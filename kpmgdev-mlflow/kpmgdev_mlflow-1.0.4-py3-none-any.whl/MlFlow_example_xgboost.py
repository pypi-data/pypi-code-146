# Databricks notebook source
from sklearn import datasets
import sklearn
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import pandas as pd
from main_mlflow_run import mlflow_logging

# simple ml model example - xgb + iris dataset

iris = datasets.load_iris() #dataset loading
X = pd.DataFrame(iris.data)               #Features stored in X 
y = iris.target    


x_train, x_test_val, y_train, y_test_val = train_test_split(X, y, test_size=0.3, random_state=42)
x_test, x_val, y_test, y_val = train_test_split(x_test_val, y_test_val, test_size=0.5, random_state=42)


xgb_clf = XGBClassifier()


param_dist = {'objective':'binary:logistic', 'n_estimators':300}
xgb_clf = XGBClassifier(**param_dist)

eval_set = [(x_train, y_train), (x_val, y_val)]

xgb_clf.fit(x_train, y_train,
        eval_set=eval_set,
        eval_metric='mlogloss',verbose=True)

y_pred = xgb_clf.predict(x_test)

cr_df = pd.DataFrame(sklearn.metrics.classification_report(y_test, y_pred, output_dict= True)).T
print('\n\n',cr_df)


#### example of objects you can document on kpmgdev-mlflow

# parmeters - model configurations , for example, loss_function
parameters_dict = {'test_size':0.15, 'val_size':0.15, 'eval_metric': 'mlogloss', 'objective': 'binary:logistic', 'n_estimators':300, 'accuracy': cr_df.loc[['accuracy'],['f1-score']].iloc[0,0]}

#artifacts - object we want to keep , for example: list of ids, final model, classification report
artifacts_dict = {'x_train_ids':[x_train.index,'csv'], 'x_val_ids':[x_val.index,'csv'], 'x_test_ids':[x_test.index,'csv'],
             'classification_report':[cr_df,'xlsx'],'txt_file':['asd and fgfg','txt'],'json_file':['hellllooo','json']}

#metric - scores over iterations/epochs
train_loss ,val_loss = pd.DataFrame(xgb_clf.evals_result()).T.iloc[:,0]
metrics_dict = {'train_loss':train_loss, "val_loss":val_loss}

#models
model_list = [xgb_clf, 'pickle']




# final mlFlow function

experiment_name = 'IRIS_classification'
run_name = "run1"

mlflow_running_location = 'azureml'
# workspace_dict = {'subscription_id_name' : '824b6b2b-8b60-4860-b57e-9c9f3157ab69',
#                     'workspace_name' : 'dna-workspace01',
#                     'resource_group' : 'rg-ml01'}
workspace_dict = {'subscription_id_name' : '824b6b2b-8b60-4860-b57e-9c9f3157ab69',
                    'workspace_name' : 'databricks-ws0',
                    'resource_group' : 'rg-ml01'}

mlflow_log = mlflow_logging(workspace_location= mlflow_running_location, workspace_dict=workspace_dict)
mlflow_log.main_mlflow_models_doc(experiment_name=experiment_name,
                                           run_name = run_name,
                                           # artifact_location = '/Users/elinorrahamim/mlruns',
                                           parameters_dict=parameters_dict,
                                           metrics_dict=metrics_dict,
                                           artifacts_dict=artifacts_dict,
                                           model_list = model_list)