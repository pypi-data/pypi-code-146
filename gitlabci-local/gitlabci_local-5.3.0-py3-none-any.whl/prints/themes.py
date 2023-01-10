#!/usr/bin/env python3

# Modules libraries
from prompt_toolkit.styles.style import Style as prompt_toolkit_styles_Style

# Themes class, pylint: disable=too-few-public-methods
class Themes:

    # Constants
    BOLD: str = 'bold'
    CYAN: str = '#00FFFF bold'
    DISABLED: str = 'italic'
    GREEN: str = '#00FF00 bold noreverse'
    SELECTED: str = 'bold noreverse'
    YELLOW: str = '#FFFF00 bold'

    # Checkbox theme
    CHECKBOX: prompt_toolkit_styles_Style = prompt_toolkit_styles_Style([
        ('answer', CYAN),
        ('disabled', DISABLED),
        ('instruction', CYAN),
        ('highlighted', BOLD),
        ('pointer', YELLOW),
        ('qmark', YELLOW),
        ('question', GREEN),
        ('selected', SELECTED),
        ('separator', YELLOW),
    ])

    # Configurations theme
    CONFIGURATIONS: prompt_toolkit_styles_Style = prompt_toolkit_styles_Style([
        ('answer', CYAN),
        ('instruction', CYAN),
        ('highlighted', GREEN),
        ('pointer', YELLOW),
        ('qmark', YELLOW),
        ('question', YELLOW),
        ('selected', SELECTED),
        ('separator', YELLOW),
    ])

    # Graphics theme
    POINTER: str = '»'
