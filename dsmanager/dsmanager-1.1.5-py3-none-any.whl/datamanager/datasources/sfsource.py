"""@Author: Rayane AMROUCHE

SalesForce Sources Handling.
"""

import os
import json

from typing import Any

import simple_salesforce  # type: ignore # pylint: disable=import-error

import pandas as pd  # type: ignore

from dsmanager.datamanager.datasources.datasource import DataSource


class SFSource(DataSource):
    """Inherited Data Source Class for sql sources."""

    @staticmethod
    def show_schema() -> None:
        """Get source metadata schema."""
        schema = {
            "source_type": "salesforce",
            "username_env_name": "sf_username_environment_variable_name",
            "password_env_name": "sf_password_environment_variable_name",
            "token_env_name": "sf_token_environment_variable_name",
            "domain_env_name": "sf_domain_environment_variable_name",
            "table_name": "TABLE",
            "args": {"simple_salesforce_argument_keyword": "value_for_this_argument"},
        }
        print(json.dumps(schema, indent=4))

    @staticmethod
    def read_source(
        username_env_name: str,
        password_env_name: str,
        token_env_name: str,
        domain_env_name: str,
        table_name: str,
        **kwargs: Any,
    ) -> Any:
        """Salesforce source reader.

        Args:
            username_env_name (str): Name of the username env variable.
            password_env_name (str): Name of the password env variable.
            token_env_name (str): Name of the token env variable.
            domain_env_name (str): Name of the domain env variable.
            table_name (str): Name of the table in the dataset.

        Returns:
            Any: Data from source.
        """
        engine = simple_salesforce.Salesforce(
            username=os.environ.get(username_env_name, ""),
            password=os.environ.get(password_env_name, ""),
            security_token=os.environ.get(token_env_name, ""),
            domain=os.environ.get(domain_env_name, ""),
            **kwargs,
        )
        if table_name:
            column_list = (
                pd.DataFrame(getattr(engine, table_name).describe()["fields"])["name"]
            ).to_list()

            columns = ", ".join(column_list)
            query = f"""SELECT {columns} FROM {table_name}"""

            data = engine.query(query)["records"]
            data = pd.DataFrame.from_dict(data, orient="columns").drop(
                "attributes", axis=1
            )
        else:
            data = engine

        return data

    def read(self, source_info: dict, **kwargs: Any) -> Any:
        """Handle source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source datas.
        """
        self.load_source(source_info, **kwargs)
        args = source_info["args"] if "args" in source_info else {}

        data = self.read_source(
            source_info["username_env_name"],
            source_info["password_env_name"],
            source_info["token_env_name"],
            source_info["domain_env_name"],
            source_info["table_name"],
            **args,
        )

        self.logger.info("Read data from salesforce.")
        return data

    def read_db(self, source_info: dict, **kwargs: Any) -> Any:
        """Read source and returns a source engine.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source engine.
        """
        self.load_source(source_info, **kwargs)
        args = source_info["args"] if "args" in source_info else {}

        engine = self.read_source(
            source_info["username_env_name"],
            source_info["password_env_name"],
            source_info["token_env_name"],
            source_info["domain_env_name"],
            "",
            **args,
        )

        self.logger.info("Connect to salesforce.")

        return engine
