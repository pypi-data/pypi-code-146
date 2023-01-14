from typing import Union, Literal

prefixes = ['__ANIMATE__']

def stylesheet(styles: dict[str, dict]):
    output = "" 

    for name, value in styles.items():
        props = ""
        if type(value) is not dict:
            props = ':' + value + ';'
        else:
            props = '{' + stylesheet(value) + '}'

        output += f'{name}{props}'

    for prefix in prefixes:
        output = output.replace(prefix, '')
    return output


def sub_style(parent_class: str, styles: dict[str, any]):
    return {f'{parent_class} {k}': v for k, v in styles.items()}


def animation(
        name: str,
        targets: list[str],
        keyframes: dict[str, any],
        duration_ms: Union[int, float] = 0,
        delay_ms: Union[int, float] = 0,
        play_state: Literal[
            'paused', 'running', 'initial', 'inherit'
            ] = 'running',
        timing_fn: str = 'ease',
        direction: Literal[
            'normal', 'reverse', 'alternate', 'alternate-reverse', 
            'initial', 'inherit'
            ] = 'normal',
        iteration_count: Union[
            int, Literal['infinite', 'initial', 'inherit']
            ] = 1,
        fill_mode: Literal[
            'none', 'forwards', 'backwards', 'both', 'initial', 'inherit'
            ] = 'none',
):
    props = f'{name} {duration_ms}ms {timing_fn} {delay_ms}ms {iteration_count} {direction} {fill_mode} {play_state}'
    return {
        f'@keyframes {name}': keyframes,
        **{f'__ANIMATE__{t}': {'animation': props} for t in targets}
    }
