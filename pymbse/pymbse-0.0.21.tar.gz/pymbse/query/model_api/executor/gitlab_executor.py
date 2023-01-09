import ast
import datetime
import json
import os
import time
import warnings

import requests
from requests import Response

from pymbse.query.model_api.executor.executor import Executor, read_figures_of_merit, ARTEFACTS_KEYWORD
from pymbse.query.model_api.snapshot.model_snapshot import ModelSnapshot


class GitLabExecutor(Executor):

    def execute_with_snapshot(self) -> ModelSnapshot:
        """Method executing a model and returning a model snapshot

        :return: an initialized ModelSnapshot instance
        """
        job_id = self._execute_without_figures_of_merit_and_artefacts()
        outputs_dct = self._get_figures_of_merit_and_artefacts(job_id)
        return self._initialize_model_snapshot(job_id, outputs_dct)

    def _initialize_model_snapshot(self, job_id: int, outputs_dct: dict) -> ModelSnapshot:
        """Method initializing a model snapshot from model execution output dictionary and additional pieces of
        information.

        :param outputs_dct: a dictionary with figures of merit and artefacts
        :return: an initialized ModelSnapshot instance
        """
        abs_path = f"{self.model_dependency_config.project_url}/-/tree/{self.model_dependency_config.branch_or_tag}/" \
                   f"{self.model_dependency_config.model_rel_path}"
        artefacts = self._read_artefacts(job_id, outputs_dct)
        figures_of_merit = read_figures_of_merit(outputs_dct)
        return ModelSnapshot(
            name=self.model_dependency_config.get_model_name_without_ext(),
            abs_path=abs_path,
            execution_time=str(datetime.datetime.now()),
            modification_timestamp=int(self._get_last_commit_time()),
            input_parameters=self.input_parameters,
            artefacts=artefacts,
            figures_of_merit=figures_of_merit,
        )

    def _get_last_commit_time(self) -> int:
        """
        Method querying the timestamp of the last commit for model snapshot

        https://docs.gitlab.com/ee/api/commits.html#get-a-single-commit

        :return: timestamp of the last commit in seconds
        """
        url = f"{self.model_dependency_config.project_url}/repository/commits/{self.model_dependency_config.branch_or_tag}"
        headers = {"PRIVATE-TOKEN": os.environ["PRIVATE_TOKEN"]}
        response_commit = requests.get(url, headers=headers)
        created_at = response_commit.json()['created_at']
        dt = datetime.datetime.strptime(''.join(created_at.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S.%f%z')
        return int(time.mktime(dt.timetuple()))

    def execute(self) -> dict:
        job_id = self._execute_without_figures_of_merit_and_artefacts()
        return self._get_figures_of_merit_and_artefacts(job_id)

    def _execute_without_figures_of_merit_and_artefacts(self):
        self._put_ci_cd_file_variable(file_variable_name="input_parameters", file_content=self.input_parameters)
        self._put_ci_cd_file_variable(file_variable_name="input_files", file_content=self.input_files)
        response_pipeline = self._trigger_pipeline()
        pipeline_id = response_pipeline.json()["id"]
        response_jobs = self._wait_until_pipeline_is_done(pipeline_id)
        return response_jobs.json()[0]["id"]

    def _put_ci_cd_file_variable(self, file_variable_name: str, file_content: dict) -> None:
        """
        Method putting (updating) CI/CD file variable in GitLab

        For more info consult: https://docs.gitlab.com/ee/api/project_level_variables.html
        :param file_variable_name: name of a variable to set
        :param file_content: file content to write
        """
        url = f"{self.model_dependency_config.project_url}/variables/{file_variable_name}"
        headers = {"PRIVATE-TOKEN": os.environ["PRIVATE_TOKEN"]}

        data = {
            "variable_type": "file",
            "key": "parameter",
            "value": json.dumps(file_content)}
        response = requests.put(url, headers=headers, json=data)
        if response.status_code != 200:
            warnings.warn(f"Couldn't update CI/CD variable {file_variable_name}.")

    def _trigger_pipeline(self) -> Response:
        """
        Method triggers a pipeline and returns a response

        :return: response from pipeline trigger
        """
        url = f"{self.model_dependency_config.project_url}/trigger/pipeline"
        token = os.environ["PIPELINE_TOKEN"]
        notebook_out_path = self._get_notebook_name()
        notebook_html_path = self._get_report_name()
        artefacts_dir = os.path.dirname(self.model_dependency_config.model_rel_path)
        variables = {"NOTEBOOK_PATH": self.model_dependency_config.model_rel_path,
                     "NOTEBOOK_OUT_PATH": notebook_out_path,
                     "HTML_OUT_PATH": notebook_html_path,
                     "FIGURES_OF_MERIT_AND_ARTEFACTS_PATH": "figures_of_merit_and_artefacts.json",
                     "ARTEFACTS_DIR": artefacts_dir}
        data = {"token": token,
                "ref": self.model_dependency_config.branch_or_tag,
                "variables": variables}
        return requests.post(url, json=data)

    def _get_notebook_name(self) -> str:
        return self.model_dependency_config.model_rel_path.replace(".ipynb", "_out.ipynb")

    def _get_report_name(self) -> str:
        return self.model_dependency_config.model_rel_path.replace(".ipynb", "_out.html")

    def _wait_until_pipeline_is_done(self, pipeline_id: int) -> Response:
        url = f"{self.model_dependency_config.project_url}/pipelines/{pipeline_id}/jobs"
        headers = {"PRIVATE-TOKEN": os.environ["PRIVATE_TOKEN"]}

        response_jobs = requests.get(url, headers=headers)
        while response_jobs.json()[0]["status"] in {"pending", "running"}:
            print(f"Status of job {response_jobs.json()[0]['id']} is {response_jobs.json()[0]['status']}. "
                  f"Waiting 1 second and checking again.")
            time.sleep(self.model_dependency_config.time_sleep_in_sec)
            response_jobs = requests.get(url, headers=headers)

        return response_jobs

    def _get_figures_of_merit_and_artefacts(self, job_id: int) -> dict:
        return ast.literal_eval(self._get_artefact(job_id, "figures_of_merit_and_artefacts.json"))

    def _get_artefact(self, job_id: int, artefact_name: str) -> str:
        url = f"{self.model_dependency_config.project_url}/jobs/{job_id}/artifacts/{artefact_name}"
        headers = {"PRIVATE-TOKEN": os.environ["PRIVATE_TOKEN"]}

        response_art = requests.get(url, headers=headers)

        if response_art.status_code != 200:
            warnings.warn(f"Couldn't get artefact {artefact_name} for job {job_id}.")

        return response_art.text

    def _read_artefacts(self, job_id: int, outputs_dct: dict) -> dict:
        if ARTEFACTS_KEYWORD not in outputs_dct:
            return {}

        return {
            artefact: self._get_artefact(job_id=job_id, artefact_name=artefact)
            for artefact in outputs_dct[ARTEFACTS_KEYWORD]
        }
