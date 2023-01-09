#############################################################################################################
###
### Conversions to human readable
###
############################################################################################################# 

import math 

def human_readable_number(x, digits=3):
    '''
    Rounds a number to a fixed number of significant digits.
    see https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python for discussion
    '''
    if not isinstance(x,int) and not isinstance(x,float):
        return x
    if digits <=0:
        return x
    if x == 0 or not math.isfinite(x):
        return x
    digits -= math.ceil(math.log10(abs(x)))
    result = round(x, digits) 
    if math.modf(result)[0] == 0:
        return int(result)
    return result  

def human_readable_number_1(x):    return human_readable_number(x, digits=1)
def human_readable_number_2(x):    return human_readable_number(x, digits=2)
def human_readable_number_3(x):    return human_readable_number(x, digits=3)
def human_readable_number_4(x):    return human_readable_number(x, digits=4)




def human_readable_seconds(seconds):
    '''Converts seconds to human readable time'''
    TIME_DURATION_UNITS = (
        ('week', 60*60*24*7),
        ('day', 60*60*24),
        ('hour', 60*60),
        ('min', 60),
        ('sec', 1)
    )

    if seconds < 60:
        return str(round(seconds, 1)) + ' secs'
    parts = []
    seconds = round(seconds, 0)
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)



def human_readable_bytes(num, suffix='B'):
    '''Converts Bytes to human readable size'''
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)   














