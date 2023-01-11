
from powerml import PowerML
import logging
import re
logger = logging.getLogger(__name__)


class AutocompleteSQLModel:
    def __init__(self,
                 config={},
                 max_output_tokens=256,
                 ):
        self.model = PowerML(config)
        self.model_name = "hex/sql-autocomplete/v2"
        self.max_output_tokens = max_output_tokens
        self.table_schemas = []
        self.example_queries = []

    def fit(self, table_schemas=[], example_queries=[]):
        """
        Parameters
        ----------
        table_schemas : list
            Takes in a list of schema definitions where element of the
            list corresponds to the schema for one table.
        example_queries: list
            Takes a list of sql queries that have been used with the tables
            to get sql results.
        """
        self.table_schemas = table_schemas
        self.example_queries = example_queries

    def predict(self, sql_prompt):
        prompt = {
            "{{input}}": sql_prompt,
            "{{examples}}": "\nEND".join(self.example_queries),
            "{{table_schemas}}": "\n".join(self.table_schemas)
        }

        output = self.model.predict(
            prompt,
            max_tokens=self.max_output_tokens,
            stop=['\\\\nEND', '\\nEND', '\nEND', ';'],
            temperature=0.7,
            model=self.model_name)
        print(output)
        return self.post_process(output)

    def post_process(self, output):
        # TODO: replace with stop tokens
        results = re.split('\\\\nEND|\\nEND|\nEND|select|;', output)
        return results[0].strip()
