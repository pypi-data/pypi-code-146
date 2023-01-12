from powerml.utils.run_ai import run_ai
import re


def more_sql_like_this(example, n=1):
    '''
    Uses LLM to get more queries like the example.
    '''
    prompt_append = f'Write %d more example(s) that use the same schema, but answer a different business question than the above. List them below.\n\nExample 1. ' % (
        n)
    prompt = f'Example: {example}\n\n{prompt_append}'
    text = run_ai(prompt,
                  max_tokens=256,
                  )
    results = re.split("Example \d+\.", text)
    results = [strip_end_of_query(r).strip() for r in results]
    return results


def strip_end_of_query(query):
    location = query.find(";")

    if location > 0:
        return query[:location+1]

    return query
