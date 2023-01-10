from snipper.block_parsing import indent


def fix_r(lines):
    for i,l in enumerate(lines):
        if "#!r" in l:
            lines[i] = indent(l) + l[l.find("#!r") + 3:].lstrip()
    return lines
