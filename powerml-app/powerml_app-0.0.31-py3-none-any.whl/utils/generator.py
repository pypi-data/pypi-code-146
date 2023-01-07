from powerml.utils.constants import KEYWORDS, DELAY_IN_SECONDS
from powerml.fuzzy.fuzzy_contains import fuzzy_contains
import json
from collections import defaultdict
from sql_metadata import Parser
import time

def get_types(model_predictions, gold_types):
    generated_types = set()
    for model_prediction in model_predictions:
        for gold_type in gold_types:
            if gold_type not in generated_types:
                is_contained = fuzzy_contains(model_prediction, gold_type)
                if is_contained:
                    time.sleep(DELAY_IN_SECONDS)
                    generated_types.add(gold_type)
    return generated_types

def load_menu(menu_filename):
    items = []
    with open(menu_filename) as menu_file:
        menu_data = json.load(menu_file)
        for menu_datum in menu_data:
            items.append(menu_datum['name'])
    return items

def load_menu_with_associated_aliases(menu_filename, alias_filename):
    with open(alias_filename) as alias_file:
        alias = json.load(alias_file)
        menu = load_menu(menu_filename)
        menu_with_aliases = {}
        for item in menu:
            menu_with_aliases[item] = item
            if item in alias:
                if 'display_name' in alias[item]:
                    menu_with_aliases[alias[item]['display_name']] = item
                if 'extra_display_name' in alias[item]:
                    menu_with_aliases[alias[item]['extra_display_name']] = item
    return menu_with_aliases

def load_menu_from_files():
    menu_filename = 'deltaco.json'
    alias_filename = 'deltaco_props.json'
    return load_menu_with_associated_aliases(
        menu_filename, alias_filename)

def create_schema(queries):
        tables = defaultdict(set)
        for query in queries:
            try:
                query_parser = Parser(query)
                if query.startswith('select'):
                    table = query_parser.tables
                    if not table:
                        from_index = query.find(' from ') + len(' from ')
                        where_index = query.find(' where ')
                        table = query[from_index:where_index]
                    else:
                        table = table[0]
                    tables[table].update({column for column in query_parser.columns if column not in KEYWORDS})
                else: # query.startswith('with')
                    for with_query in query_parser.with_queries.values():
                        with_query_parser = Parser(with_query)
                        table = with_query_parser.tables[0]
                        if table not in query_parser.with_names:
                            tables[table].update({column.split('.')[-1] for column in with_query_parser.columns if column not in KEYWORDS})
            except:
                continue
        return tables

def tables_to_schema(tables):
    schema = []
    for table in tables:
        columns = ',\n    '.join(tables[table]) + ','
        schema.append(f"""create table {table} (\n    {columns}\n);""")
    return schema