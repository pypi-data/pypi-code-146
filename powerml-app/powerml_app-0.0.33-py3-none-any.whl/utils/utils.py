'''Utility functions'''

from powerml.utils.run_ai import run_ai
from powerml.utils.constants import MAX_SHORT_TOKENS, N_LOGPROBS, LOGPROB_THRESHOLD


def get_top_tokens_by_logprobs(logprobs, uses_bool_none=True):
    '''Gets the important tokens, based on logprobs. If it's for a bool check, filters out None's.'''
    filtered_tokens = []
    for t in logprobs['top_logprobs']:
        if '<|endoftext|>' in t and t['<|endoftext|>'] > LOGPROB_THRESHOLD:
            break

        top_tokens = t.keys()
        for top_t in top_tokens:
            if t[top_t] < LOGPROB_THRESHOLD:
                continue

            if '\n' in top_t:
                continue
            if uses_bool_none and ('none' in top_t.lower() or top_t.lower() == 'n'):
                continue

            filtered_tokens.append((top_t, t[top_t]))
    return sorted(filtered_tokens, key=lambda ft: ft[1], reverse=True)


def postprocess_bool_none(output):
    '''Postprocesses boolean outputs with "none" for boolean output, and explanation/reason as extra output.'''
    bool_check = True
    output = output.strip()
    if output.lower() == 'none':
        bool_check = False
        output = output.lower().replace('none', '')
    elif 'none' in output.lower():
        print(
            f'Not sure if none is it b/c other words are outputted. TODO: run another LLM on it to double check. Output is {output}')
        bool_check = False
        output = output.lower().replace('none', '')

    extra_output = postprocess_helper_extra_output(output)
    return bool_check, extra_output


def postprocess_bool_yes_no(output):
    '''Postprocesses boolean outputs with yes/no.'''
    bool_check = True
    output = output.strip()
    if 'no' in output.lower():
        bool_check = False
    extra_output = postprocess_helper_extra_output(output)
    return bool_check, extra_output


def postprocess_bool_bullet_explanations(output):
    '''Postprocesses boolean outputs with yes/no and bullet explanations'''
    bool_check = True
    output = output.strip().split('\n')
    extra_output = []
    for i, o in enumerate(output):
        if i == 0:
            if 'no' in o.lower():
                bool_check = False
        elif '-' in o:
            o = o.split('-')[-1]
            extra_output.append(o.strip())
        else:
            print(f'Skipping processing this output {o}')
    return bool_check, extra_output


def postprocess_helper_extra_output(output):
    extra_output = []
    for o in output.split('\n'):
        if o:
            o_comma_split = [oo for oo in o.split(',') if oo]
            extra_output.extend(o_comma_split)
    if extra_output == ['']:
        extra_output = []
    return extra_output


def run_and_postprocess(prompt,
                        return_extra=False,
                        return_top_tokens=False,
                        uses_bool_none=False,
                        uses_bool_bullet=False,
                        run_rerun=False,
                        rerun_prompt_append=None,
                        max_tokens=MAX_SHORT_TOKENS,
                        ):
    '''
    Run LLM and postprocesses output.
    run_rerun: In a setting where we rerun with previous iteration's high logprobs.
    rerun_prompt_append: If run_rerun is True, use this extra bit in prompt
    '''
    if run_rerun and rerun_prompt_append:
        prompt += f' {rerun_prompt_append.strip()}'
        output = run_ai(prompt=prompt,
                        max_tokens=max_tokens,
                        return_logprobs=False,
                        )
        rerun_output = rerun_prompt_append + output
        print(f'Rerun output is: {rerun_output}')
    else:
        output, logprobs = run_ai(prompt=prompt,
                                  max_tokens=max_tokens,
                                  n_logprobs=N_LOGPROBS,
                                  return_logprobs=True,
                                  )
    if uses_bool_none:
        bool_check, extra_output = postprocess_bool_none(output)
    elif uses_bool_bullet:
        bool_check, extra_output = postprocess_bool_bullet_explanations(output)
    else:
        bool_check, extra_output = postprocess_bool_yes_no(output)

    is_check_high_logprobs = run_rerun and not bool_check and rerun_prompt_append is None

    if not logprobs is None:
        if return_top_tokens or is_check_high_logprobs:
            high_tokens_logprobs = get_top_tokens_by_logprobs(
                logprobs, uses_bool_none)

            # Check for high logprob tokens that could've been missed, in original run (not rerun)
            if is_check_high_logprobs:
                print(
                    f'Tokens with important logprobs that were not sampled: {high_tokens_logprobs}')

                if high_tokens_logprobs:
                    # TODO: Check all of them, not just the first one (best one, b/c sorted)
                    rerun_prompt_append = high_tokens_logprobs[0][0]
                    bool_logprob_check, extra_output_logprob_check = run_and_postprocess(
                        prompt,
                        return_extra=True,
                        return_top_tokens=False,
                        run_rerun=True,
                        rerun_prompt_append=rerun_prompt_append
                    )

                    # Override contains if applicable
                    bool_check = max(bool_check, bool_logprob_check)
                    if bool_check:
                        rerun_output = rerun_prompt_append
                        if extra_output_logprob_check:
                            rerun_output += extra_output_logprob_check[0]
                        extra_output.append(rerun_output)

    returns = [bool_check]
    if return_extra:
        returns.append(extra_output)

    if return_top_tokens and not logprobs is None:
        returns.append(high_tokens_logprobs)

    if len(returns) > 1:
        return returns
    else:
        return returns[0]
