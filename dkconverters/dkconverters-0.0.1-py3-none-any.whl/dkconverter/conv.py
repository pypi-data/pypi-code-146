'''-----------'''

# FUNCTION-1


def bina(num):
    '''It converts number into its binary form which is provided as Argument'''
    l = []

    if num == 0:
        s = '0'
    else:
        for i in range(0, num+1):
            if 2**i <= num:
                l = [2**i]+l
            else:
                break
        s = '1'
        x = l[0]
        for q in range(1, len(l)):
            if x+l[q] <= num:
                x = x+(l[q])
                s = s+'1'
            else:
                s = s+'0'
    return '0b'+s

# FUNCTION-2


def octl(num):
    '''It converts number into its octal form which is provided as Argument'''
    l = []
    if num == 0:
        s = '0'
    else:
        for i in range(0, num+1):
            if 8**i <= num:
                l = [8**i]+l
            else:
                break
        s = ''
        for q in range(0, len(l)):
            if num >= 0:
                y = num//l[q]
                s = s+str(y)
                num = num-(y*l[q])
    return '0o'+s

# FUNCTION-3


def hexdcml(num):
    '''It converts number into its hexadecimal form which is provided as Argument'''
    l = []
    if num == 0:
        s = '0'
    else:
        for i in range(0, num+1):
            if 16**i <= num:
                l = [16**i]+l
            else:
                break
        s = ''
        for q in range(0, len(l)):
            if num >= 0:
                y = num//l[q]
                if y < 10:
                    s = s+str(y)
                else:
                    s = s+str(chr(97+(y-10)))
                num = num-(y*l[q])
    return '0x'+s
