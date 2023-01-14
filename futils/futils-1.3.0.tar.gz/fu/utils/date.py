
class InvalidFormatError(Exception):
    pass

def parse_date(date_str: str, pattern: str):
    """
    Parses string by using provided format

    :param date_str: String to be parsed
    :param pattern:  Date format pattern used to parse 'date_str'. Following
        letters are allowed for pattern:
            D - Day of month (1 - 31)
            M - Month of year (1 - 12)
            Y - Year [0-9] x4
            - - For expected '-' characters
            _ - For expected '_' characters
            . - For expected '.' characters
              - For expected ' ' (spaces) characters
            X - For any other character that should be ignored
            * - To indicate that all remaining characters should be ignored
    :return: (year, month, day)
    """
    valid_chars = ['D', 'M', 'Y', '-', '_', '.', ' ', 'X', '*']
    day = month = year = ''

    if pattern[-1] == '*':
        if len(date_str) < len(pattern) - 1:
            raise InvalidFormatError(
                'Provided string does not matches given pattern'
            )
    elif len(pattern) != len(date_str):
        raise InvalidFormatError(
            'Provided string does not matches given pattern'
        )

    for idx in range(0, len(pattern)):
        char = pattern[idx]
        if char not in valid_chars:
            raise InvalidFormatError(
                '{} is not a valid char in pattern'.format(char)
            )

        if char == '*':
            if idx < len(pattern) - 1:
                raise InvalidFormatError(
                    '"*" should be last char in pattern'
                )
            else:
                break

        # Parse day chars
        if char == 'D':
            if len(day) == 2:
                raise InvalidFormatError(
                    '"D" digits must be consecutives and a '
                    'max 2 are allowed'
                )
            
            day = day + date_str[idx]

        # Parse month chars
        if char == 'M':
            if len(month) == 2:
                raise InvalidFormatError(
                    '"M" digits must be consecutives and a '
                    'max of 2 are allowed'
                )

            month = month + date_str[idx]
        
        # Parse year chars
        if char == 'Y':
            
            # During first 'Y' occurrence, validate 4 year digits
            # were provided
            if year == '':
                for j in range(idx, idx + 4):
                    if j >= len(pattern) or pattern[j] != 'Y':
                        raise InvalidFormatError(
                            '4 "Y" are required for year'
                        )

            # More than 4 'Y' were found
            if len(year) == 4:
                raise InvalidFormatError(
                    '"Y" digits must be consecutives and must be 4'
                )
            
            year = year + date_str[idx]
    
    return year, month, day
