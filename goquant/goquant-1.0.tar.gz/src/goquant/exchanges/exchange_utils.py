# This function takes a list of symbol pairs that has been retrieved from an exchance and standardizes
# each symbol pair in the list.
# 
# All symbol pairs will be standardized to the following format: aaabbb
def clean_supported_symbols(available_symbols):

    clean_list = []
    for s in available_symbols:
        clean_list.append(s.lower().replace('-', '').replace('/', '').replace(' ', ''))

    return clean_list