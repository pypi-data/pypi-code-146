from powerml.utils.run_ai import run_ai
import re


def more_like_this(example, n=1):
    '''
    Uses LLM to get more text like the example.
    '''
    prompt_append = f'Write %d more example(s) written about the same topic but by a different person from the above. List them below.\n1. ' % (
        n)
    prompt = f'Example: {example}\n\n{prompt_append}'
    text = run_ai(prompt,
                  max_tokens=128,
                  )
    results = re.split("\d+\.", text)
    results = [r.strip() for r in results]
    return results


def sql_from_columns(columns=[], n=1):
    '''
    Uses LLM to get more sql queries like the example.
    '''
    column_list_string = "[" + ", ".join(columns) + "]"
    prompt = f'\"\"\"\nTable customers, columns = {column_list_string}\nWrite a complex SQL query for the customers table. Terminate with a semicolon\n\"\"\"\nselect'
    text = run_ai(prompt,
                  max_tokens=128,
                  stop=["\"", ";", "#"],
                  model="code-davinci-002",
                  api="openai",
                  temperature=1,
                  )
    results = re.split("\d+\.", text)
    results = [r.strip() for r in results]
    return results


if __name__ == "__main__":
    texts1 = [
        'AI: Hi, what can we make fresh for you today?\nCX: Chicken Cheddar Quesadilla.',
        'extra habenero sauce',
        'cinnamon roll shake',
    ]

    for text1 in texts1:
        text = more_like_this(
            text1, n=1)

        print(f'Example: {text1}')
        print(f'Similar generated output: {text}')
