with open('board_xref.py', 'r') as f_xref:
    xref = list(f_xref.readlines())
    xref = (xref[:-1])
    for index in range(920, 1000):
        text = ' '*4 + "'{:04d}': [''],\n".format(index)
        xref.append(text)
    xref.append(' '*4 + '}')

with open('board_xref.py', 'w') as f_xref:
    print(''.join(xref))
    f_xref.write(''.join(xref))