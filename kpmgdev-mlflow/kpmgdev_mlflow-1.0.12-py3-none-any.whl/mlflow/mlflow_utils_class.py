import shutil
import warnings
import numpy as np
import torch
import mlflow
import pandas as pd
import os
import json
import pickle


# MlFlowLogging

class MlFlowMainLogging:
    """
    saves and documents all the required info on the kpmgdev-mlflow local dir and presents it on the Mlflow UI -
    that splits into three main sections:  parameters, metrics and artifacts
    """

    @staticmethod
    def get_experiment_id(experiment_name: str, artifact_location: str = None):

        """
        Gets the experiment id by an existing experiment or by defining a new one

        param:
        experiment_name: string of the experiment name (str)
        artifact_location:  The location to store run artifacts (str). If not provided (None), the server picks an appropriate default.

        return: the experiment number id (str)
        """

        # Checks if the experiment already exist, if it's not, None will return
        experiment_details = mlflow.get_experiment_by_name(experiment_name)

        if not experiment_details:
            # The experiment doesn't exist, so we are creating a new one
            experiment_id = mlflow.create_experiment(name=experiment_name,
                                                     artifact_location=artifact_location)
        else:
            experiment_id = experiment_details.experiment_id

        return experiment_id

    @staticmethod
    def log_metrics_from_dict(metrics_dict: dict):
        """
        logs every metric in "metrics_dict" to the MlFlow

        param:
          metrics: dict of metrics - {metric name : the metric object}

        """
        for key_i in metrics_dict.keys():

            try:

                metric_i = metrics_dict[key_i]
                for j in range(len(metric_i)):
                    mlflow.log_metric(key=key_i, value=metric_i[j], step=j + 1)

            except Exception as e:
                warnings.warn(str(e))

    @staticmethod
    def log_object_as_artifact_BY_type(artifacts: dict, key: str, dir_path: str):

        """
        Finds the required file type, and logging the object to the Mlflow

        param:
            artifacts: Dict of objects(artifacts), each key contain list of the object and its required file type - {artifact name : [artifact, type:(csv,txt,json,xlsx, pkl)]}
            key: The artifact name (str)
            dir_path: local dir to save the needed artifact, so the kpmgdev-mlflow will be able to log it

        """

        file, file_type = artifacts[key]
        file_name = key + '.' + file_type

        if np.isin(file_type, ['txt', 'html']):
            mlflow.log_text(file, file_name)

        elif np.isin(file_type, ['png', 'jpeg', 'jpg']):
            mlflow.log_image(file, file_name)

        elif np.isin(file_type, ['json', 'yml', 'yaml']):
            mlflow.log_dict(file, file_name)

        else:

            tmp_save_file_path = dir_path + '/' + file_name

            if file_type == 'pkl':
                pd.DataFrame(file).to_pickle(tmp_save_file_path)

            elif file_type == 'xlsx':
                pd.DataFrame(file).to_excel(tmp_save_file_path)

            elif file_type == 'csv':
                pd.DataFrame(file).to_csv(tmp_save_file_path)

            elif file_type == 'npy':
                np.save(tmp_save_file_path, np.array(file))

            mlflow.log_artifact(tmp_save_file_path)

    @staticmethod
    def log_artifacts_from_dict(artifacts_dict: dict):

        """
        saves needed objects as an artifacts on the MlFlow dir and presents it at kpmgdev-mlflow UI

        param:
          artifacts: dict of artifacts, each key contain list of the artifact and its required file type - {artifact name : [artifact, type:(csv,txt,json,xlsx, pkl)]}

        """

        # creating a temp local dir to save the needed artifact, so the Mlflow will be able to save it on its mlflow_run dir and presents it on its UI
        tmp_save_dir_path = os.getcwd() + '/mlflow_save'  # /' + file_name
        if not os.path.isdir(tmp_save_dir_path):
            os.makedirs(tmp_save_dir_path)

        # loop over all the artifacts, save each locally by their file type, and load it to the kpmgdev-mlflow
        for key_i in artifacts_dict.keys():

            try:
                file, file_type = artifacts_dict[key_i]
                MlFlowMainLogging.log_object_as_artifact_BY_type(artifacts=artifacts_dict, key=key_i,
                                                                 dir_path=tmp_save_dir_path)

            except FileNotFoundError:
                warnings.warn('Error file format ** ' + file_type +
                              ' ** has no support. The required file did not log as an artifact!')
            except Exception as e:
                warnings.warn(str(e))

        # deleting the temporary local artifact dir that was created earlier
        shutil.rmtree(tmp_save_dir_path)

    @staticmethod
    def log_model_as_artifact(model_list: list):
        """
        saves the Model as an artifact on MlFlow dir and presents it at kpmgdev-mlflow UI

        param:
          model_list: list of - [the model, type:( pt,pickle)] - "pt" is pytorch format , "pickle" often used in sklearn model

        """

        try:

            # gets the current local path to save the model temporary
            tmp_save_dir_path = os.getcwd()

            # save the model by its type
            model, model_saving_format = model_list
            model_file_path = tmp_save_dir_path + '/model.' + model_saving_format

            if model_saving_format == 'pt':
                torch.save(model, model_file_path)

            elif model_saving_format == 'pickle':
                pickle.dump(model, open(model_file_path, "wb"))

            # saving by kpmgdev-mlflow
            mlflow.log_artifact(model_file_path)

            # remove the temporary saved model file
            os.remove(model_file_path)

        # in cases the model_saving_format is not "pt" or "pickle", The log_artifact will raise an error = FileNotFoundError , so i've made a custum error
        except FileNotFoundError:
            warnings.warn('Error model format ** ' + model_saving_format +
                          ' ** has no support. The required model did not log as an artifact!')
        except Exception as e:
            warnings.warn(str(e))

    @staticmethod
    def main_mlflow_models_doc(experiment_name: str, run_name: str, description: str = None,
                               parameters_dict: dict = None, metrics_dict: dict = None
                               , artifacts_dict: dict = None, model_list: list = None, artifact_location: str = None):

        """
        param:
         experiment_name: The experiment name on the MLflow - insert an experiment name, but if it's already exist, insert the required experiment name
         user_name: if the experiment already exist , insert the user on the databricks who created the required experiment
         run_name: the title of the current run
         description: An optional string that populates the description box of the run (default = None)
         parameters: dict of parameters - {'parameter name' : parameter(int,str,float)}
         metrics: dict of metrics - {metric name : the metric object}
         artifacts: dict of artifacts, each key contain list of the artifact and its required file type - {artifact name : [artifact, type:(csv,txt,json,xlsx, pkl)]}
         model_list: list of - [the model, type:( pt,pickle)]
         artifact_location: The location to store run artifacts (str). If not provided (None), the server picks an appropriate default.
        """

        try:

            # setting the URI for documenting the run on the MLflow UI
            # kpmgdev-mlflow.set_tracking_uri(tracking_uri)

            experiment_id = MlFlowMainLogging.get_experiment_id(experiment_name=experiment_name,
                                                                artifact_location=artifact_location)

            with mlflow.start_run(run_name=run_name, experiment_id=experiment_id, description=description) as run:

                # saves the run_id as a parameter
                run_id = run.info.run_id
                mlflow.log_param(key='run_id', value=run_id)

                # logging the parameters
                if parameters_dict:
                    mlflow.log_params(params=parameters_dict)

                # logging the metrics
                if metrics_dict:
                    MlFlowMainLogging.log_metrics_from_dict(metrics_dict=metrics_dict)

                # logging the artifacts
                if artifacts_dict:
                    MlFlowMainLogging.log_artifacts_from_dict(artifacts_dict=artifacts_dict)

                # logging the model as artifact
                if model_list:
                    MlFlowMainLogging.log_model_as_artifact(model_list=model_list)

        except Exception as e:
            warnings.warn(str(e))
