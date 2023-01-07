def unpack_list(List: list | tuple):
    singles = []
    for l in List:
        if type(l) != str:
            ls = unpack_list(l)
            singles.extend(ls)
        else:
            singles.append(l)
    return singles
