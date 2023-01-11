from powerml.utils.utils import run_and_postprocess
import numpy as np


def fuzzy_assert_equals(text1, text2):
    '''
    Uses LLM to check whether text1 and text2 are about the same thing.
    '''
    prompt_append = f'Compare the two texts above. Are they the same thing? Answer Yes or No.'
    prompt = f'Text 1: {text1}\n\nText 2: {text2}\n\n{prompt_append}'

    is_equal = run_and_postprocess(prompt,
                                   uses_bool_none=False,
                                   )
    return is_equal


def fuzzy_assert_equals_with_probs(text1, text2):
    '''
    Uses LLM to check whether text1 and text2 are about the same thing.
    '''
    prompt_append = f'Compare the two texts above. Are they the same thing? Answer Yes or No.'
    prompt = f'Text 1: {text1}\n\nText 2: {text2}\n\n{prompt_append}'

    is_equal, logprobs = run_and_postprocess(prompt,
                                             return_top_tokens=True,
                                             uses_bool_none=False,
                                             )
    probs = []
    for token, logprob in logprobs:
        # Only keep yes and no tokens, and compute their probs from logprobs
        if token.lower() not in ['yes', 'no']:
            continue
        prob = np.exp(logprob)
        probs.append((token, prob))

    return is_equal, probs


if __name__ == "__main__":
    texts1 = [
        'Diet coke',
        'extra habenero sauce',
        'cinnamon roll shake',
    ]

    texts2 = [
        'Del coke zero',
        'extra hashbrown sauce',
        'cinnamon red sauce',
    ]

    for text1, text2 in zip(texts1, texts2):
        bool_check, probs = fuzzy_assert_equals(
            text1, text2, return_probs=True)

        print(f'Text 1: {text1}')
        print(f'Text 2: {text2}')
        print(
            f'Are these about the same thing? {"Yes" if bool_check else "No"}')
        print(f'Probs are {probs}')
        print('=============================')
