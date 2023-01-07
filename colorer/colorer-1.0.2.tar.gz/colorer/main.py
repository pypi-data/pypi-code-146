from .colors import Fore, Back, Style


def string(text: str, clean_spaces: bool = False):
    params = text[text.find('((')+2:text.find('))')]
    src_params = text[text.find(f'(({params}'):text.find('))')+2]
    f_string = text[text.find(src_params)+len(src_params):]
    style_end = f_string[f_string.find('(('):f_string.find('))')+2]

    if len(style_end) > 0:
        f_string = f_string[:f_string.find(style_end)]

    if clean_spaces:
        f_string = f_string.strip()

    params = params.split(',')

    text_style = '\033['

    for param in params:
        param = param.lower().strip().split('=')

        global is_fore_digit

        if param[0] == 'style':
            if param[1] == 'normal':
                text_style += Style.NORMAL
            elif param[1] == 'bold':
                text_style += Style.BOLD
            elif param[1] == 'light':
                text_style += Style.LIGHT
            elif param[1] == 'italic':
                text_style += Style.ITALIC
            elif param[1] == 'underlined':
                text_style += Style.UNDERLINED
            elif param[1] == 'blink':
                text_style += Style.BLINK
        if param[0] == 'fore':
            if param[1].isdigit():
                text_style = '\033[38;5;' + param[1] + 'm'
                is_fore_digit = True
            else:
                is_fore_digit = False

                if param[1] == 'black':
                    text_style += Fore.BLACK
                elif param[1] == 'red':
                    text_style += Fore.RED
                elif param[1] == 'green':
                    text_style += Fore.GREEN
                elif param[1] == 'yellow':
                    text_style += Fore.YELLOW
                elif param[1] == 'blue':
                    text_style += Fore.BLUE
                elif param[1] == 'purple':
                    text_style += Fore.PURPLE
                elif param[1] == 'cyan':
                    text_style += Fore.CYAN
                elif param[1] == 'white':
                    text_style += Fore.WHITE
                elif param[1] == 'none':
                    text_style += Fore.NONE
        if param[0] == 'back':
            if param[1].isdigit():
                text_style = '\033[48;5;' + param[1] + 'm'
            else:
                if param[1] == 'black':
                    text_style += Back.BLACK
                elif param[1] == 'red':
                    text_style += Back.RED
                elif param[1] == 'green':
                    text_style += Back.GREEN
                elif param[1] == 'yellow':
                    text_style += Back.YELLOW
                elif param[1] == 'blue':
                    text_style += Back.BLUE
                elif param[1] == 'purple':
                    text_style += Back.PURPLE
                elif param[1] == 'cyan':
                    text_style += Back.CYAN
                elif param[1] == 'white':
                    text_style += Back.WHITE
                elif param[1] == 'none' and is_fore_digit is False:
                    text_style += Back.NONE

    text_style += f_string + '\033[0;0m'

    return text_style
