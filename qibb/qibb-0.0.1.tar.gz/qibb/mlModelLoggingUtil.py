import mlflow
import mlflow.keras
import os

class modelLogRegisterUtil():
    def __init__(self,dict1):

        self.experiment_name = dict1['experiment_name']
        self.run_name = dict1['run_name']
        self.destinationDir = dict1['destination_dir']
        self.tags = list(map(str, dict1['tags'].split(',')))
        self.run_desc = dict1['run_description']
        self.register_model_name = dict1['register_model_name']

        os.environ['AWS_ACCESS_KEY_ID']= 'AKIA2KXYWVN7XARYRZEM'
        os.environ['AWS_SECRET_ACCESS_KEY']= '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'

    def logging(self,trained_model=None,run_params=None ,run_metrics=None):
        '''
        This function start a run and log parameters, metrics, model, tags, etc and return a run_id.
        '''

        mlflow.set_tracking_uri('https://mlflow.qritrim.com/')
        # mlflow.set_tracking_uri("http://127.0.0.2:5000")
        
        mlflow.set_experiment(self.experiment_name)

        
        with mlflow.start_run(run_name=self.run_name,description=self.run_desc):
            run_id = mlflow.active_run().info.run_id

            if not trained_model == None:
                mlflow.sklearn.log_model(trained_model, self.run_name)

            if not run_params == None:
                for param in run_params:
                    mlflow.log_param(param, run_params[param])
                
            if not run_metrics == None:
                for metric in run_metrics:
                    mlflow.log_metric(metric, run_metrics[metric])
            
            for count,tag in enumerate(self.tags):
                mlflow.set_tag(f"Tag{count+1}", tag)

            
        print(f'Run - "{self.run_name}" is logged to Experiment - "{self.experiment_name}"')
        return run_id

    def modelRegister(self,run_id):
        register_model = mlflow.register_model(f"runs:/{run_id}/{self.run_name}",f"{self.register_model_name}",await_registration_for=None)
        return dict(register_model)
    
