from powerml.utils.utils import run_and_postprocess


def fuzzy_duplicate_filter(text, return_duplicates=False):
    '''
    Uses LLM to check whether text has nonsensical duplicates (model is repeating itself).

    text: Input text to check.
    '''
    prompt_append = f'\n\nFrom the above text, extract any repetitive phrases that makes no sense. If none, write "none".'
    prompt = text + prompt_append

    bool_check, extra = run_and_postprocess(prompt,
                                            return_extra=return_duplicates,
                                            uses_bool_none=True,
                                            )

    if return_duplicates:
        return bool_check, extra
    else:
        return bool_check


if __name__ == "__main__":
    texts = [
        'I like carrots and llamas.',
        '''CX: I'd like to order.
AI: Sorry we are out of that.
CX: Sorry we are really really out of that.
Order: 1x Vanilla Syrup''',
    ]

    for text in texts:
        bool_check, duplicates = fuzzy_duplicate_filter(
            text, return_duplicates=True)

        print(f'Text: {text}')
        print(
            f'Are there duplicates that make no sense? {"Yes" if bool_check else "No"}')
        print(f'If yes, the reason is {duplicates}')
        print('=============================')
