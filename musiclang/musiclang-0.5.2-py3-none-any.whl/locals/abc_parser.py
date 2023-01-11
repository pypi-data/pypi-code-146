INDEXES_KEYS = {
    'B#': [0, 'M'],
    'C': [0, 'M'],
    'Db': [1, 'M'],
    'C#': [1, 'M'],
    'D': [2, 'M'],
    'D#': [3, 'M'],
    'Eb': [3, 'M'],
    'E': [4, 'M'],
    'Fb': [4, 'M'],
    'Es': [5, 'M'],
    'F': [5, 'M'],
    'F#': [6, 'M'],
    'Gb': [6, 'M'],
    'G': [7, 'M'],
    'G#': [8, 'M'],
    'Ab': [8, 'M'],
    'A': [9, 'M'],
    'A#': [10, 'M'],
    'Bb': [10, 'M'],
    'B': [11, 'M'],
    'Cb': [11, 'M']
}

LOCAL_KEYS = {
    'M': {
        'I': [0, 'M'],
        '#I': [1, 'M'],
        'bII': [1, 'M'],
        'II': [2, 'M'],
        '#II': [3, 'M'],
        'bIII': [3, 'M'],
        'III': [4, 'M'],
        '#III': [4, 'M'],
        'IV': [5, 'M'],
        '#IV': [6, 'M'],
        'bV': [6, 'M'],
        'V': [7, 'M'],
        '#V': [8, 'M'],
        'bVI': [8, 'M'],
        'VI': [9, 'M'],
        '#VI': [9, 'M'],
        'bVII': [10, 'M'],
        'VII': [11, 'M'],
        '#VII': [11, 'M']
    },

    'm': {
        'I': [0, 'M'],
        '#I': [1, 'M'],
        'bII': [1, 'M'],
        'II': [2, 'M'],
        '#II': [3, 'M'],
        'bIII': [3, 'M'],
        'III': [3, 'M'],
        '#III': [4, 'M'],
        'IV': [5, 'M'],
        '#IV': [6, 'M'],
        'bV': [6, 'M'],
        'V': [7, 'M'],
        '#V': [8, 'M'],
        'bVI': [8, 'M'],
        'VI': [8, 'M'],
        '#VI': [9, 'M'],
        'bVII': [10, 'M'],
        'VII': [10, 'M'],
        '#VII': [11, 'M']
    }
}

INDEXES_NUMERAL = {
    'M': {
        'I': [0, 0, 'M'],
        'ii': [1, 0, 'M'],
        'iii': [2, 0, 'M'],
        'IV': [3, 0, 'M'],
        'V': [4, 0, 'M'],
        'vi': [5, 0, 'M'],
        'vii': [6, 0, 'M'],

        'i': [0, 0, 'm'],
        'II': [4, 7, 'M'],
        'III': [4, 9, 'm'],
        'iv': [3, 0, 'm'],
        'v': [0, 7, 'm'],
        'VI': [4, 2, 'm'],
        'VII': [4, 4, 'm'],

        '#vi': [5, 0, 'm'],

        'bII': [5, 5, 'm']
    },

    'm': {
        'i': [0, 0, 'm'],
        'ii': [1, 0, 'm'],
        'III': [2, 0, 'm'],
        'iv': [3, 0, 'm'],
        'V': [4, 0, 'm'],
        'VI': [5, 0, 'm'],
        '#vii': [6, 0, 'm'],

        'I': [0, 0, 'M'],
        'II': [4, 7, 'M'],
        'iii': [0, 3, 'm'],
        'IV': [3, 0, 'M'],
        'v': [0, 7, 'm'],
        'vi': [0, 8, 'm'],
        'vii': [0, 10, 'm'],
        'VII': [4, 3, 'M'],

        '#vi': [5, 0, 'M'],
        'bII': [5, 5, 'm']
    }
}

# 7. 64. 65.  6. 43. nan  2.]
INDEXES_FIGBASS = {
    '7': [['s', 0, 0], ['s', 2, 0], ['s', 4, 0], ['s', 6, 0]],
    '64': [['s', 4, 0], ['s', 0, 1], ['s', 2, 1]],
    '6': [['s', 2, 0], ['s', 4, 0], ['s', 0, 1]],
    '65': [['s', 2, 0], ['s', 4, 0], ['s', 6, 0], ['s', 0, 1]],
    '2': [['s', 6, -1], ['s', 0, 0], ['s', 2, 0], ['s', 4, 0]],
    '43': [['s', 4, 0], ['s', 6, 0], ['s', 0, 1], ['s', 2, 1]]
}

INDEXES_CHANGES = {  # Origin, replacement, delta octave

    '': {
        '2': [2, 's', 1, 0],
        '4': [2, 's', 3, 0],
        '6': [4, 's', 5, 0],
        '7': [0, 's', 6, -1],
        '9': [2, 's', 1, 0],
        'A': [2, 's', 3, 0],
        'B': [4, 's', 5, 0]
    },

    'b': {
        '2': [2, 'h', 1, 0],
        '3': [4, 'h', 3, 0],
        '4': [2, 'h', 4, 0],
        '5': [4, 'h', 6, 0],
        '6': [4, 'h', 8, 0],
        '7': [0, 'h', 10, -1],
        '9': [2, 'h', 1, 0],
        'A': [2, 'h', 4, 0],
        'B': [4, 'h', 8, 0],
    },

    '#': {
        '2': [2, 'h', 3, 0],
        '3': [4, 'h', 4, 0],
        '4': [2, 'h', 6, 0],
        '5': [4, 'h', 8, 0],
        '6': [4, 'h', 9, 0],
        '7': [0, 'h', 11, -1],
        '9': [2, 'h', 3, 0],
        'A': [2, 'h', 6, 0],
        'B': [4, 'h', 9, 0],
    }
}

for key in list(INDEXES_KEYS.keys()):
    INDEXES_KEYS[key.lower()] = (INDEXES_KEYS[key][0], 'm')

for mode in list(LOCAL_KEYS.keys()):
    for key in list(LOCAL_KEYS[mode].keys()):
        LOCAL_KEYS[mode][key.lower()] = (LOCAL_KEYS[mode][key][0], 'm')


def parse_global_key(row):
    key = INDEXES_KEYS[row['global_key']]
    return key


def parse_local_key(row, global_root, global_mode):
    local_root, local_mode = LOCAL_KEYS[global_mode][row]
    return ((local_root + global_root) % 12, local_mode)


def parse_relative_root(row, global_root, global_mode):
    if row != row:
        return global_root, global_mode
    local_root, local_mode = LOCAL_KEYS[global_mode][row]
    return ((local_root + global_root) % 12, local_mode)


def parse_changes(change, degree, relative_mode, voicing):
    if change != change:
        return voicing

    change = change.replace('11', 'A')
    change = change.replace('13', 'B')
    mode = 'replace'
    accident = ''
    replacements = []
    additions = []
    for c in change:
        print(mode, c)
        if c == '+':
            mode = 'add'
        elif c == 'b' or c == '#':
            accident = c
        else:
            if mode == 'replace':
                replaced_val, new_type, new_val, delta_octave = INDEXES_CHANGES[accident][c]
                replacements.append([replaced_val, new_type, new_val, delta_octave])
                pass
            elif mode == 'add':
                replaced_val, new_type, new_val, delta_octave = INDEXES_CHANGES[accident][c]
                additions.append([replaced_val, new_type, new_val, delta_octave])

            accident = ''
            mode = 'replace'

    new_voicing = []

    for v in voicing:
        curr_v = list(v)
        curr_type, curr_val, curr_octave = curr_v
        already = False
        to_add = []
        for replaced_val, new_type, new_val, delta_octave in replacements:
            if replaced_val == curr_val:
                already = True
                to_add.append([new_type, new_val, curr_octave + delta_octave])

        if not already:
            new_voicing.append(curr_v)
        for a in to_add:
            new_voicing.append(a)

    for replaced_val, new_type, new_val, new_octave in additions:
        # IF less than first of voicing, add an octave

        to_add = [new_type, new_val, new_octave]
        bass_type, bass_val, bass_octave = voicing[0]
        if bass_octave > new_octave:
            to_add[-1] += 1
        elif (bass_octave == new_octave) and new_val < bass_val:
            to_add[-1] += 1

        new_voicing.append(list(to_add))

    # Sort
    new_voicing = list(sorted(new_voicing, key=lambda x: (x[2], x[1])))

    return new_voicing


def parse_figbass(row):
    if row != row:
        return [['s', 0, 0], ['s', 2, 0], ['s', 4, 0]]
    return INDEXES_FIGBASS[str(int(row))]


def parse_numeral(row, root, mode):
    if row != row:
        return 0, root, mode, 1
    row = row.replace('\\', '')
    if mode == 'M':
        row = row.replace('#', '')
    degree, final_root, final_mode = INDEXES_NUMERAL[mode][row]
    final_root = (final_root + root) % 12
    return degree, final_root, final_mode, 0


def parse_row(row, key):
    from fractions import Fraction as frac
    global_root, global_mode = key
    local_root, local_mode = parse_local_key(row['local_key'], global_root, global_mode)
    relative_root, relative_mode = parse_relative_root(row['relativeroot'], local_root, local_mode)
    degree, final_root, final_mode, silence = parse_numeral(row['numeral'], relative_root, relative_mode)
    voicing = parse_figbass(row['figbass'])
    voicing = parse_changes(row['changes'], degree, relative_mode, voicing)
    duration = row['totbeat']
    duration = frac(duration)
    return degree, final_root, final_mode, silence, voicing, duration


def parse_piece(df):
    chords = []

    key = parse_global_key(df.iloc[0])

    time = 0
    for idx, row in df.iterrows():
        chord = list(parse_row(row, key))
        time += chord[-1] - time
        if len(chords) > 0:
            chords[-1][-1] = time - chords[-1][-1]
        chords.append(chord)

    return chords


chords = parse_piece(df)
# df.iloc[-60:-50]