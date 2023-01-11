from powerml.utils.utils import run_and_postprocess


def fuzzy_coherence_check(text, return_reasons=False):
    '''
    Uses LLM to check whether text has incoherences.

    text: Input text to check.
    '''
    prompt_append = f'\n\nIn the above text, is there anything incoherent? Answer yes or no. If yes, list the incoherences in bullet points.'
    prompt = text + prompt_append

    bool_check, reasons = run_and_postprocess(
        prompt,
        return_extra=return_reasons,
        uses_bool_bullet=True,
        max_tokens=200,
    )

    # Make sure to flip the bool b/c it was used for checking incoherence
    if return_reasons:
        return not bool_check, reasons
    else:
        return not bool_check


if __name__ == "__main__":
    texts = [
        'I like carrots and llamas.',
        '''CX: I'd like to order.
AI: Sorry we are out of that.
CX: Sorry we are really really out of that.
Order: 1x Vanilla Syrup''',
    ]

    for text in texts:
        bool_check, reasons = fuzzy_coherence_check(text, return_reasons=True)

        print(f'Text: {text}')
        print(f'Is it coherent? {"Yes" if bool_check else "No"}')
        print(f'If no, the reasons are {reasons}')
        print('=============================')
