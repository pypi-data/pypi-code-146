import types
from typeguard import typechecked
import openai
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

@typechecked
class Config:
    """
    Config class to store all the parameters for OpenAI and MongoDB Atlas.

    Attributes:
        openai_api_key: OpenAI API key
        mongo_db_name: MongoDB Atlas database name
        mongo_cluster_url: MongoDB Atlas cluster URL
        mongo_user_name: MongoDB Atlas username
        mongo_password: MongoDB Atlas password
    """

    def __init__(self,
                 openai_api_key: str,
                 mongo_db_name: str,
                 mongo_cluster_url: str,
                 mongo_user_name: str,
                 mongo_password: str,
                 openai_organization_id: str = None):
        self.openai_api_key = openai_api_key
        self.mongo_db_name = mongo_db_name
        self.mongo_cluster_url = mongo_cluster_url
        self.mongo_user_name = mongo_user_name
        self.mongo_password = mongo_password
        self.openai_organization_id = openai_organization_id

    @property
    def openai_client(self) -> types.ModuleType:
        """
        OpenAI client
        """
        openai.api_key = self.openai_api_key

        if self.openai_organization_id is not None:
            openai.organization = self.openai_organization_id
        return openai

    @property
    def mongo_client(self) -> MongoClient:
        """
        MongoDB Atlas client
        """
        username_pass = f'{self.mongo_user_name}:{self.mongo_password}'
        connection_url = f'mongodb+srv://{username_pass}@{self.mongo_cluster_url}/{self.mongo_db_name}'
        return MongoClient(connection_url)

    @property
    def async_mongo_client(self) -> AsyncIOMotorClient:
        """
        MongoDB Atlas client
        """
        username_pass = f'{self.mongo_user_name}:{self.mongo_password}'
        connection_url = f'mongodb+srv://{username_pass}@{self.mongo_cluster_url}/{self.mongo_db_name}'
        return AsyncIOMotorClient(connection_url)
