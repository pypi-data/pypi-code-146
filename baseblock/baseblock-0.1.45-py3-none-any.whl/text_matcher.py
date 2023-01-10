# -*- coding: utf-8 -*-
""" Text Matcher Class """


class TextMatcher(object):
    """ Text Matcher Class """

    @staticmethod
    def exists(value: str,
               input_text: str,
               case_sensitive: bool = False) -> bool:
        """ Check for the existence of a value in input text

        Args:
            value (str): any value string
            input_text (str): any text string to search in
            case_sensitive (bool): True if case sensitivity matters

        Returns:
            bool: True if the value exists in the input text
        """

        if not case_sensitive:
            value = value.lower()
            input_text = input_text.lower()

        if value == input_text:
            return True

        match_lr = f' {value} '
        if match_lr in input_text:
            return True

        match_l = f' {value}'
        if input_text.endswith(match_l):
            return True

        match_r = f'{value} '
        if input_text.startswith(match_r):
            return True

        return False

    @staticmethod
    def replace(input_text: str,
                old_value: str,
                new_value: str,
                case_sensitive: bool = False,
                recursive: bool = False) -> bool:
        """ Check for the existence of a value in input text

        Args:
            input_text (str): any text string to search in
            old_value (str): the value that must exist in the input text
            new_value (str): the value that will replace 'old value' within the input text
            case_sensitive (bool): True if case sensitivity matters
            recursive (bool): if True, then apply method recursively until all changes are made

        Returns:
            bool: True if the value exists in the input text
        """

        if not case_sensitive:
            old_value = old_value.lower()
            input_text = input_text.lower()

        if old_value == input_text:
            return new_value

        original_text = input_text

        match_lr = f' {old_value} '
        if match_lr in input_text:
            input_text = input_text.replace(match_lr, f' {new_value} ')

        match_l = f' {old_value}'
        if input_text.endswith(match_l):
            input_text = input_text.replace(match_l, f' {new_value}')

        match_r = f'{old_value} '
        if input_text.startswith(match_r):
            input_text = input_text.replace(match_r, f'{new_value} ')

        if recursive and original_text != input_text:
            return TextMatcher.replace(
                input_text=input_text,
                old_value=old_value,
                new_value=new_value,
                case_sensitive=case_sensitive)

        return input_text

    @staticmethod
    def coords(value: str,
               input_text: str,
               case_sensitive: bool = False) -> bool:
        """ Find the X,Y coords (if any) for a given value in the supplied input text

        Args:
            input_text (str): any text string to search in
            value (str): the value to find coords for
            case_sensitive (bool): True if case sensitivity matters

        Returns:
            bool: True if the value exists in the input text
        """

        if not case_sensitive:
            value = value.lower()
            input_text = input_text.lower()

        if value == input_text:
            return 0, len(value)

        match_lr = f' {value} '
        if match_lr in input_text:
            x = input_text.index(match_lr)
            return x + 1, x + len(value) + 1

        match_l = f' {value}'
        if input_text.endswith(match_l):
            return len(input_text) - len(value), len(input_text)

        match_r = f'{value} '
        if input_text.startswith(match_r):
            return 0, len(value)

        # not found
        return None, None
