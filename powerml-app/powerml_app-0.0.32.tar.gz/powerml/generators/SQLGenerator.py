from powerml import Generator
from powerml import AutocompleteSQLModel
from powerml.utils.generator import create_schema, tables_to_schema
from math import ceil

class SQLGenerator(Generator):
    '''
    This is a class that can be used to generate more queries for AutocompleteSQLModels.
    '''

    def __init__(self, schema):
        super().__init__(schema, 'code-davinci-002', max_output_tokens=1250)

    def coverage_generator(self, queries, return_metrics=True):
        model = AutocompleteSQLModel()
        model.fit(tables_to_schema(self.gold_types), queries)
        model_predictions = []
        for query in queries:
            query = query.split()[0]
            model_predictions.append(query + ' ' + model.predict(query))
        generated_schema = create_schema(model_predictions)
        metrics = self.compute_coverage(generated_schema)
        coverage = metrics['Coverage']
        rare_tables = metrics['Rare Types']
        generated_queries = []
        if rare_tables:
            # generate at least 1 example per rare_table, proportional to the amount of coverage of the queries
            num_generate = ceil((1 - coverage) * len(queries) / len(rare_tables))
            print(f'num generate: {num_generate}')
            for table in rare_tables:
                modifier = f'include \'{table}\''
                generated_queries.extend(self._generate_modified(queries, modifier, num_generate))
        if return_metrics:
            return generated_queries, metrics
        return generated_queries