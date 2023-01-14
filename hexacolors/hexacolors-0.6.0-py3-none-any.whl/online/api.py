import asyncio
from .client.clientlogin import ClientAPI

def hexadecimal(hexa:str) -> int:

    '''
    Using HexaColor:

    >>> import hexacolors
    >>> hexacolors.hexadecimal('#0000FF') #Convert Hexadecimal Color for Python understand
    '''

    if hexa[0] == '#':hexa = hexa[1::]
    
    request = asyncio.run(ClientAPI(f'hex', hexa).get())

    return int(f"0x{request}",16)

def rgb(rgb) -> int:

    '''
    Using rgb:

    >>> import hexacolors
    >>> hexacolors.rgb('255,255,255')
    '''
    
    request = asyncio.run(ClientAPI(f'rgb', rgb).get())
    
    return int(f"0x{request}",16)

def cmyk(cmyk) -> int:

    '''
    Using cmyk:

    >>> import hexacolors
    >>> hexacolors.cmyk('423,522,4,244')
    '''

    request = asyncio.run(ClientAPI(f'cmyk', cmyk).get())

    return int(f"0x{request}",16)

def hsl(hsl:str) -> int:

    '''
    Using hsl:

    >>> import hexacolors
    >>> hexacolors.hsl('423,60%,70%')
    '''

    request = asyncio.run(ClientAPI(f'hsl', hsl).get())

    return int(f"0x{request}",16)