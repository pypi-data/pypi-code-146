import re

LOOP_ENTRY_REGEX = r'{%\s*for\s+(?P<key_name>\w+)(\s*,\s*(?P<value_name>\w+))?\s+in\s+(?P<dict_name>\w+)(?:\\\.items\\\(\\\))?\s+%}'
LOOP_EXIT_REGEX = r'{%\s*endfor\s*%}'

class LoopClosedBeforeOpenedException(Exception):
    def __init__(self):
        super().__init__('Loop was closed before it was opened.')

class LoopNeverClosedException(Exception):
    def __init__(self):
        super().__init__('Loop was opened but never closed.')

def invalid(_):
    raise LoopClosedBeforeOpenedException()


LOOKING_FOR_END = 0
LOOKING_FOR_START = 1
TRANSITIONS = {
    LOOKING_FOR_END: {
        'enter': lambda d: (LOOKING_FOR_END, d+1),
        'exit': lambda d: (LOOKING_FOR_END, d-1) if d > 1 else (LOOKING_FOR_START, 0)
    },
    LOOKING_FOR_START: {
        'enter': lambda _: (LOOKING_FOR_END, 1),
        'exit': invalid
    }
}

class ForLoopStateMachine:
    def __init__(self):
        self._state = (LOOKING_FOR_START, 0)

    def transition(self, event):
        self._state = TRANSITIONS[self._state[0]][event](self._state[1])

    @property
    def state(self):
        return self._state[0]

class ForLoop:
    def __init__(self, begin, end, template):
        self.begin = begin[0]
        self.end = end[2].end()
        self.content_begin = begin[2].end()
        self.content_end = end[0]
        self.content = template[self.content_begin:self.content_end].strip('\n')
        self.vars = [begin[2][1], begin[2][3]] if begin[2][3] else [begin[2][1]]
        self.name = begin[2][4]

    @property
    def id(self): #pylint: disable=invalid-name
        return f'loop_{self.begin}_{self.end}'

    @property
    def is_dict(self):
        return len(self.vars) == 2

    def __repr__(self):
        content = self.content.replace('\n', '\\n')
        return f'{self.name}: [{self.begin} - {self.end}] ({", ".join(self.vars)}); content : "{content}"'

def keep_top_loop_only(ids):
    if ids == []: return [] #pylint: disable=multiple-statements

    kept = []
    machine = ForLoopStateMachine()

    for id_ in ids:
        if machine.state == LOOKING_FOR_START:
            kept.append(id_)
        machine.transition(id_[1])
        if machine.state == LOOKING_FOR_START:
            kept.append(id_)

    if machine.state != LOOKING_FOR_START:
        raise LoopNeverClosedException()
    return kept

def identify(template):
    entries = [(entry.start(), 'enter', entry) for entry in re.finditer(LOOP_ENTRY_REGEX, template)]
    exits = [(entry.start(), 'exit', entry) for entry in re.finditer(LOOP_EXIT_REGEX, template)]
    ids = sorted(
        [*entries, *exits],
        key = lambda id_: id_[0]
    )
    return keep_top_loop_only(ids)

def find_top(template):
    ids = identify(template)
    return [
        ForLoop(ids[i], ids[i+1], template)
        for i in range(0, len(ids), 2)
    ]

def extract_top(template, loops):
    for i in range(len(loops)-1, -1, -1):
        template = template[:loops[i].begin] + f'(?P<{loops[i].id}>.*?)' + template[loops[i].end:]
    return template
