

def pygameToPandaKey(pygameKey):
    '''
    Used for reading legacy keyboard mapping files.
    '''
    return PYGAME_TO_PANDA_MAP.get(pygameKey, '')


PYGAME_TO_PANDA_MAP = {
    8: 'backspace',
    9: 'tab',
    13: 'enter',
    27: 'escape',
    32: 'space',
    33: '!',
    35: '#',
    36: '$',
    38: '&',
    39: "'",
    40: '(',
    41: ')',
    42: '*',
    43: '+',
    44: ',',
    45: '-',
    46: '.',
    47: '/',
    48: '0',
    49: '1',
    50: '2',
    51: '3',
    52: '4',
    53: '5',
    54: '6',
    55: '7',
    56: '8',
    57: '9',
    58: ':',
    59: ';',
    60: '<',
    61: '=',
    62: '>',
    64: '@',
    91: '[',
    92: '\\',
    93: ']',
    94: '^',
    95: '_',
    96: '`',
    97: 'a',
    98: 'b',
    99: 'c',
    100: 'd',
    101: 'e',
    102: 'f',
    103: 'g',
    104: 'h',
    105: 'i',
    106: 'j',
    107: 'k',
    108: 'l',
    109: 'm',
    110: 'n',
    114: 'r',
    115: 's',
    116: 't',
    117: 'u',
    118: 'v',
    119: 'w',
    120: 'x',
    121: 'y',
    122: 'z',
    127: 'delete',
    256: '0',
    257: '1',
    258: '2',
    259: '3',
    260: '4',
    261: '5',
    262: '6',
    263: '7',
    264: '8',
    265: '9',
    266: '.',
    267: '/',
    268: '*',
    269: '-',
    270: '+',
    271: 'enter',
    272: '=',
    273: 'arrow_up',
    274: 'arrow_down',
    275: 'arrow_right',
    276: 'arrow_left',
    277: 'insert',
    278: 'home',
    279: 'end',
    280: 'page_up',
    281: 'page_down',
    282: 'f1',
    283: 'f2',
    284: 'f3',
    285: 'f4',
    286: 'f5',
    287: 'f6',
    288: 'f7',
    289: 'f8',
    290: 'f9',
    291: 'f10',
    292: 'f11',
    293: 'f12',
    294: 'f13',
    295: 'f14',
    296: 'f15',
    300: 'num_lock',
    301: 'caps_lock',
    302: 'scroll_lock',
    303: 'rshift',
    304: 'lshift',
    305: 'rcontrol',
    306: 'lcontrol',
    307: 'ralt',
    308: 'lalt',
    316: 'print_screen',
}


def keyDownEvent(action):
    '''
    Returns the event name for a key down event for a given action.
    '''
    return 'trosnoth-' + action


def keyUpEvent(action):
    '''
    Returns the event name for a key up event for a given action.
    '''
    return 'trosnoth-' + action + '-up'
