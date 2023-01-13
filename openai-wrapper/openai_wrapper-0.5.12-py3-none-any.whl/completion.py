import json
from datetime import datetime
from typing import Callable, Dict, Any, List

import aiohttp
from typeguard import typechecked

from openai_wrapper.config import Config
import logging

logging.basicConfig(level=logging.INFO)


def _preprocess_prompt(prompt: str) -> str:
    """
    Basic implementation of preprocessing the prompt.

    Args:
        prompt: The prompt to preprocess

    Returns:
        The preprocessed prompt
    """
    return prompt


def _process_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic implementation of processing the response.

    Args:
        response: The response to preprocess

    Returns:
        The preprocessed response
    """
    return response


@typechecked
class Completion:
    """
    A wrapper for the openai.Completion class

    Attributes:
        use_case_name: name of the use case so it can be used as a collection name in MongoDB (e.g. "Q&A", "Quiz_Generation")
        config: A Config object
        model: The model to use for the completion
        model_params: A dictionary of parameters used to create the GPT-3 completion
        experiment_metadata: A dictionary of pre-defined metadata in project_experiment.ini about the experiment
        project_metadata: A dictionary of pre-defined metadata in project.ini about the project
        extra_params: Any extra parameters that should be stored in the MongoDB document
    """

    def __init__(self,
                 use_case_name: str,
                 config: Config,
                 model: str = "text-davinci-002",
                 model_params: Dict[str, Any] = None,
                 experiment_metadata: Dict[str, Any] = None,
                 project_metadata: Dict[str, Any] = None,
                 extra_params: Dict[Any, Any] = None):

        logging.info(f"Initializing Completion object for collection {use_case_name}")
        logging.info(f"GPT-3 Model: {model}")

        self.use_case_name = use_case_name
        self.config = config
        self.mongo_client = config.mongo_client
        self.async_mongo_client = config.async_mongo_client
        self.openai_client = config.openai_client
        if datetime.utcnow() < datetime(2022, 9, 1):
            self.TEXT_MODELS_COST_PER_1K_TOKENS = {
                "text-ada-001": 0.0008,
                "text-babbage-001": 0.0012,
                "text-curie-001": 0.0060,
                "text-davinci-002": 0.0600
            }
        else:
            self.TEXT_MODELS_COST_PER_1K_TOKENS = {
                "text-ada-001": 0.0004,
                "text-babbage-001": 0.0005,
                "text-curie-001": 0.002,
                "text-davinci-002": 0.02,
                "text-davinci-003": 0.02
            }

        self.model_params = {
            "model": model,
            "max_tokens": 256,
            "temperature": 0.7,
            "top_p": 1,
            "suffix": None,
            "stop": None,
            "stream": False,
            "logprobs": 5,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "user": "prosus-AI-team",
            "echo": False,
        }
        if model_params is None:
            logging.info(f"No model_params provided. Using default params: {self.model_params}")
        else:
            self.model_params.update(model_params)
            self.model_params["model"] = model
            logging.info(f"Updated default params. Updated params: {self.model_params}")

        self.experiment_metadata = experiment_metadata
        self.project_metadata = project_metadata
        self.extra_params = extra_params

    def _calculate_request_costs(self, total_number_of_tokens):
        """
            calculates the cost given the total number of tokens according to pricing information
            provided by openai: https://beta.openai.com/pricing
        """
        return total_number_of_tokens * self._calculate_cost_per_1000_tokens(self.model_params["model"]) / 1000

    def _calculate_cost_per_1000_tokens(self, model_name):
        """
        Calculates the cost per 1000 tokens for a given model
        """
        code_models_names = ["code-davinci-002", "code-davinci-001", "code-cushman-001"]

        if model_name in self.TEXT_MODELS_COST_PER_1K_TOKENS:
            return self.TEXT_MODELS_COST_PER_1K_TOKENS[model_name]
        elif model_name in code_models_names:
            return 0.0
        elif model_name.startswith("ada:"):
            return 0.0016
        elif model_name.startswith("babbage:"):
            return 0.0024
        elif model_name.startswith("curie:"):
            return 0.0120
        elif model_name.startswith("davinci:"):
            return 0.1200
        else:
            logging.warning(f"No cost per 1000 tokens found for model {model_name}, using default value of 0.0")
            return 0.0

    def create(self,
               prompt: str,
               prompt_version: str,
               prompt_version_description: str,
               preprocess_prompt: Callable = _preprocess_prompt,
               process_response: Callable = _process_response,
               preprocess_prompt_args: Dict[Any, Any] = None,
               process_response_args: Dict[Any, Any] = None) -> Dict[Any, Any]:
        """
        Create a completion request and store it in MongoDB

        Args:
            prompt: The prompt to use for the completion
            prompt_version: The version of the prompt (e.g. "1.0")
            prompt_version_description: A description of the prompt version (e.g. "Added more diverse examples")
            preprocess_prompt: A function that preprocesses the prompt
            process_response: A function that processes the response
            preprocess_prompt_args: A dictionary of arguments to pass to the preprocess_prompt function
            process_response_args: A dictionary of arguments to pass to the process_response function

        Returns:
            A dictionary containing the completion request and response
        """

        if preprocess_prompt_args is None:
            preprocess_prompt_args = {}
        if process_response_args is None:
            process_response_args = {}

        preprocessed_prompt = preprocess_prompt(prompt, **preprocess_prompt_args)
        response = self.openai_client.Completion.create(**self.model_params, prompt=preprocessed_prompt)

        if process_response is not None:
            response = process_response(response, **process_response_args)

        request_costs = self._calculate_request_costs(response["usage"]["total_tokens"])

        document = {
            "prompt": preprocessed_prompt,
            "prompt_version": prompt_version,
            "prompt_version_description": prompt_version_description,
            "completion_text": response["choices"][0]["text"],
            "openai_response": response.__dict__['_previous'],
            "model_params": self.model_params,
            "created_at": str(datetime.utcnow()),
            "experiment_metadata": self.experiment_metadata,
            "project_metadata": self.project_metadata,
            "request_cost_in_usd": request_costs
        }

        if self.extra_params is not None:
            document.update(self.extra_params)

        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.use_case_name]
        mongo_collection.insert_one(document)

        return document

    async def async_create(self,
                           prompt: str,
                           prompt_version: str,
                           prompt_version_description: str,
                           preprocess_prompt: Callable = _preprocess_prompt,
                           process_response: Callable = _process_response,
                           preprocess_prompt_args: Dict[Any, Any] = None,
                           process_response_args: Dict[Any, Any] = None) -> Dict[Any, Any]:
        """
        Create async completion using aihttp

        Args:
            prompt: The prompt to use for the completion
            prompt_version: The version of the prompt (e.g. "1.0")
            prompt_version_description: A description of the prompt version (e.g. "Added more diverse examples")
            preprocess_prompt: A function that preprocesses the prompt
            process_response: A function that processes the response
            preprocess_prompt_args: A dictionary of arguments to pass to the preprocess_prompt function
            process_response_args: A dictionary of arguments to pass to the process_response function

        Returns:
            A dictionary containing the completion request and response
        """
        if preprocess_prompt_args is None:
            preprocess_prompt_args = {}
        if process_response_args is None:
            process_response_args = {}

        logging.info(f"Sending async request to OpenAI with params: {self.model_params}")
        preprocessed_prompt = preprocess_prompt(prompt, **preprocess_prompt_args)
        self.model_params["prompt"] = preprocessed_prompt
        request_headers = {"Authorization": f"Bearer {self.config.openai_api_key}",
                           "Content-Type": "application/json"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.openai.com/v1/completions",
                                        headers=request_headers,
                                        json=self.model_params) as resp:
                    response = await resp.json()
                    logging.info(f"Response: {response}")

                    if process_response is not None:
                        response = process_response(response, **process_response_args)

                    request_costs = self._calculate_request_costs(response["usage"]["total_tokens"])

                    document = {
                        "prompt": preprocessed_prompt,
                        "prompt_version": prompt_version,
                        "prompt_version_description": prompt_version_description,
                        "completion_text": response["choices"][0]["text"],
                        "openai_response": response,
                        "model_params": self.model_params,
                        "created_at": str(datetime.utcnow()),
                        "experiment_metadata": self.experiment_metadata,
                        "project_metadata": self.project_metadata,
                        "request_cost_in_usd": request_costs
                    }

                    if self.extra_params is not None:
                        document.update(self.extra_params)

                    mongo_db = self.async_mongo_client[self.config.mongo_db_name]
                    mongo_collection = mongo_db[self.use_case_name]
                    await mongo_collection.insert_one(document)

                    return document
        except Exception as e:
            logging.error(f"Error in async request: {e}")
            raise e

    def get_completions_for_prompt(self, prompt: str, prompt_version: str = None) -> List[Dict[Any, Any]]:
        """
        Get all completions for a given prompt

        Args:
            prompt: The prompt to get completions for
            prompt_version: The version of the prompt (e.g. "1.0")

        Returns:
            A list of completions
        """

        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.use_case_name]
        if prompt_version:
            return list(mongo_collection.find({"prompt": prompt, "prompt_version": prompt_version}))
        else:
            return list(mongo_collection.find({"prompt": prompt}))

    def get_completion_by_id(self, completion_id: str) -> Dict[Any, Any]:
        """
        Get a completion by its id

        Args:
            completion_id: The id of the completion to get

        Returns:
            A dictionary containing the completion
        """
        from bson import ObjectId

        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.use_case_name]
        return mongo_collection.find_one({"_id": ObjectId(completion_id)})

    def get_completions_using_mongodb_filter(self, filters: Dict[Any, Any]) -> List[Dict[Any, Any]]:
        """
        Get completions by a MongoDB filter

        Args:
            filters: The filter to use to find the completion (e.g. {"prompt": "Hello", "prompt_version": "1.0"}

        Returns:
            A dictionary containing the completion
        """
        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.use_case_name]
        return list(mongo_collection.find(filters))

    @staticmethod
    def get_use_cases(config) -> List[str]:
        """
        Get all existing use cases (e.g. MongoDB collections)

        Returns:
            A list of use-cases/collections
        """
        mongo_db = config.mongo_client[config.mongo_db_name]
        return list(mongo_db.list_collection_names())
