import sqlvalidator
from powerml.utils.utils import run_and_postprocess


def validate_sql_select(query):
    '''
    Uses library to check whether text is valid sql select statement

    query: Input text to check.
    '''
    sql_query = sqlvalidator.parse(query)
    return sql_query.is_valid()


def fuzzy_is_sql(query):
    '''
    Uses LLM to check whether text contains a valid SQL program.

    text: Input query to check.
    '''

    examples = [
        "SELECT * from customers;\n\nFrom the above text, determine if it is a valid SQL program.  Answer Yes or No.\nYes. This query is valid.",
        "SELECT CAT(month as timestamp) as month from customers;\n\nFrom the above text, determine if it is a valid SQL program.  Answer Yes or No.\nNo. CAT should be CAST."
    ]

    prompt_append = f'\n\nFrom the above text, determine if it is a valid SQL program.  Answer Yes or No, and explain why or why not.'
    prompt = "\n\n".join(examples) + query + prompt_append

    is_sql = run_and_postprocess(prompt)

    # Prepend is to avoid non-professionalism in output
    # TODO: Create and add to shared prepended prompts file

    # prompt_append = f'\n\nFrom the above text, determine if it is a valid SQL program, or if there are any syntax errors.  Answer Yes or No.'
    # prompt = query + prompt_append

    # is_sql = run_and_postprocess(prompt)

    return is_sql


if __name__ == "__main__":
    texts = [
        'I like carrots and llamas.',
        '''CX: I'd like to order.
AI: Sorry we are out of that.
CX: Sorry we are really really out of that.
Order: 1x Vanilla Syrup''',
        '''
CREATE TABLE STATION
(ID INTEGER PRIMARY KEY,
CITY CHAR(20),
STATE CHAR(2),
LAT_N REAL,
LONG_W REAL);''',
        '''
SELECT * from table;''', '''
SELECT * from table'''
    ]

    for text in texts:
        bool_check = validate_sql_select(text)
        print(bool_check)
