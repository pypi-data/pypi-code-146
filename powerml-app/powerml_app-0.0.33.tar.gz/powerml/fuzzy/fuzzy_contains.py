from powerml.utils.utils import run_and_postprocess


def fuzzy_contains(text, check_contains, return_reason=False):
    '''
    Uses LLM to check whether text contains a concept.

    text: Input text to check against.
    check_contains: Word or phrase to check if it's contained in `text`. Case matters.
    return_reason: If the check is contained, then return the word(s) from the text that support check.
    '''

    # Prepend is to avoid non-professionalism in output
    # TODO: Create and add to shared prepended prompts file
    prompt_prepend = f'The following material is from a professional setting:\n\n'

    prompt_append = f'\n\nFrom the above text, extract any mention of {check_contains}, or say "none" if there aren\'t any:'
    prompt = prompt_prepend + text + prompt_append
    # TODO: check length of `text`` and truncate

    # Run rerun on high logprobs outputs from first run, need to catch b/c model likes to say none
    is_contained = run_and_postprocess(prompt,
                                           return_extra=return_reason,
                                           run_rerun=True,
                                           uses_bool_none=True,
                                           )

    return is_contained


if __name__ == "__main__":
    texts = ['I like carrots and llamas.',
             'I dream of deforesting rainforests so that we have enough trees to capture all the carbon that we are all emitting.',
             '''CX: I want a taco with carnitas please.
             AI: Great, would you want a drink with that?
             CX: Actually, yeah, a large coke would be great. 
             ''',
             ]

    checks_contains = ['an orange item',
                       'climate change',
                       'upsell attempt by the AI'
                       ]

    for text, check_contains in zip(texts, checks_contains):
        is_contained, reason = fuzzy_contains(
            text, check_contains, return_reason=True)

        print(f'Text: {text}')
        print(f'Is {check_contains} in the text? {"Yes" if is_contained else "No"}')
        print(f'If yes, the reason is {reason}')
        print('=============================')
