from os.path import splitext

"""
Define additional functions / operators that can be used in winval constraints syntax
winval syntax is used inside WDL #@wd comments
For example:

#@wv suffix(bam_index_files) == {".bai"}
"""


def iff(x, y): return (x and y) or not (x or y)
def imply(x, y): return not x or y
def defined(x): return x is not None


def prefix(x):
    if type(x) == str:
        return splitext(x)[0]
    elif type(x) == list:
        return [prefix(elm) for elm in x]
    else:
        raise ValueError(f'Can not prefix non-strings: {x} of type {type(x)}')


def suffix(x):
    if type(x) == str:
        return splitext(x)[1]
    elif type(x) == list:
        result = set()
        for elm in x:
            suf = suffix(elm)
            if type(suf) == str:
                result.add(suf)
            elif type(suf) == set:
                result.update(suf)
            else:
                raise ValueError(f"Can not add recursive suffix result {suf} to suffix set")

        return result
    else:
        raise ValueError("Can only suffix str/list[str]/list[list[str]]")
