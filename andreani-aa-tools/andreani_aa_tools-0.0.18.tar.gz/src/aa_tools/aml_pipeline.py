
from azureml.core import Workspace, Environment, ScriptRunConfig
import pickle
from azureml.core.experiment import Experiment
from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import DockerConfiguration
from datetime import datetime
from aa_tools import logger

class pipeline:

    def __init__(self, project, model, model_type, tags, seed = 0):
        self._project = project
        self._model = model
        self._model_type = model_type

        if not "scale" in tags.keys() or not tags["scale"] in ["true", "false"]:
            raise Exception("Tag scale not defined - accepted values: true, false")

        if not "balanced" in tags.keys() or not tags["balanced"] in ["over sampling", "under sampling", "false"]:
            raise Exception("Tag balanced not defined - accepted values: over sampling, under sampling, false")

        if not "outliers" in tags.keys() or not tags["outliers"] in ["true", "false"]:
            raise Exception("Tag outliers not defined - accepted values: true, false")

        if not "target" in tags.keys():
            raise Exception("Tag target not defined.")

        self._tags = tags
        self._seed = seed
        self._experiment_name = f'{project}_{model}'


    def run(self, credentials_file, environment_file, directory, script_file, log = None):
        if log is None:
            log = logger("aml_pipeline", "aa_tools.aml_pipeline.pipeline.run")
        else:
            log = log.start_function("aa_tools.aml_pipeline.pipeline.run")

        self._connect_to_workspace(credentials_file)
        log.log_console("Connected to workspace", "INFO")

        self._create_experiment()
        log.log_console("Experiment created", "INFO")

        self._create_environment(environment_file)
        log.log_console("Environment created", "INFO")

        self._define_script_config(directory, script_file)
        log.log_console("Config setted", "INFO")

        self._run(log)


    def _connect_to_workspace(self, credentials_file):
        with open(credentials_file, "rb") as file:
                ws_name, subs_id, res_group = pickle.load(file)

        self._ws = Workspace.get(
            name = ws_name,
            subscription_id = subs_id,
            resource_group = res_group
        )


    def _create_experiment(self):
        self._experiment = Experiment(workspace = self._ws, name = self._experiment_name)


    def _create_environment(self, environment_file):
        self._env = Environment.from_conda_specification(self._experiment_name, environment_file)


    def _define_script_config(self, directory, script_file):
        docker_config = DockerConfiguration(use_docker=False)
        cpu_cluster = ComputeTarget(workspace = self._ws, name="advanced-analytics-cluster")

        arguments = ['--seed', self._seed, '--project', self._project, '--model', self._model, '--model-type', self._model_type]

        for k, v in self._tags.items():
            arguments += ["--tag", k, v]

        self._config = ScriptRunConfig(source_directory = directory,
                                    script = script_file,
                                    arguments = arguments,
                                    compute_target = cpu_cluster,
                                    environment = self._env,
                                    docker_runtime_config = docker_config)


    def _run(self, log):
        log = log.start_function("aa_tools.aml_pipeline.pipeline.run._run")
        run = self._experiment.submit(config = self._config, tags = self._tags)
        self._check_satus(run, log)
        log.log_console(f"Experiment finished with status: {run.get_status()}", "INFO")
        log.close()


    def _check_satus(self, run, log):
        start_at = datetime.now()
        last_changed_at = datetime.now()
        last_status = "None"
        ready = False
        while not ready:
            status = run.get_status()
            if status != last_status:
                changed_at = datetime.now()
                log.log_console(f"New status: {status} - Status time: {changed_at - last_changed_at} - Total time: {changed_at - start_at}", "INFO")
                last_changed_at = changed_at
                last_status = status
            ready = status in ["Failed", "Completed"]


def create_train_template(filename):
    with open(filename, 'w') as file:
        file.write(template_code)

template_code = """
# ------------|| Packages ||-------------

from aa_tools import logger

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from numpy import random
from pandas import DataFrame

import click
import mlflow

# ------------|| Auxiliary Functions ||-------------

def load_data(seed, log):
    log = log.start_function("load_data")

    # creamos dataset artificial
    random.seed(seed)
    data = DataFrame({
        "total_unidades" : list(random.poisson(10, 1000)) + list(random.poisson(100, 750)) + list(random.poisson(1000, 250))
    })
    data["total_lineas"] = data.total_unidades.apply(lambda x: random.randint(1, x) if x > 1 else 1)
    data["target"] = data.apply(lambda x: random.gamma(x.total_unidades / 8, x.total_lineas / 100), axis = 1)

    # Train - test split
    X_train, X_test, y_train, y_test = train_test_split(data.drop(columns = ["target"]), data.target, test_size = 0.33, random_state = seed)
    log.log_console(f"Total train data: {X_train.shape[0]} - test: {X_test.shape[0]}", "INFO")

    log.close()
    return X_train, X_test, y_train, y_test

# ------------|| Main Function ||-------------

@click.command()
@click.option("--seed", default = 0, help = "Random state value.")
@click.option("--project", default = "aa_analysis", help = "Project name.")
@click.option("--model", default = "linear_regressor", help = "Model name.")
@click.option("--model-type", default = "regression", help = "Model type.")
@click.option("--tag", multiple = True, type = (str, str), help = "Extra tags to add.")
def main(seed, project, model, model_type, tag):
    log = logger("aml_training", "main")
    mlrun = mlflow.start_run()

    # Get data
    X_train, X_test, y_train, y_test = load_data(seed, log)

    # Training
    regresor = LinearRegression(fit_intercept = False).fit(X_train, y_train)
    log.log_console("Model trained", "INFO")

    mse = mean_squared_error(y_test, regresor.predict(X_test))
    log.log_console(f"Model MSE: {mse}", "INFO")
    mlflow.log_metric('MSE', mse)

    # Save model
    model_name = f"{project}_{model}"
    model_file = f"{model_name}.pkl"
    model_tags = {
        "project" : project,
        "algorithm" : model,
        "type" : model_type
    }
    for t in tag:
        model_tags[t[0]] = t[1]

    model_info = mlflow.sklearn.log_model(regresor, model_file, registered_model_name = model_name)
    mlflow.register_model(model_info.model_uri, model_name)

    log.close()

# ------------|| Main Script ||-------------

if __name__ == "__main__":
    main()

"""
