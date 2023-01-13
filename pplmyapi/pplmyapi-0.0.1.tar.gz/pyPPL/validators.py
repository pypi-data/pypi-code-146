
def max_length(value: str, max_length: int) -> str:
    """ Check if the length of the value is less than or equal to max_length. If not, crop it"""
    if not value:
        return value
        
    if len(value) > max_length:
        return value[:max_length]
    return value