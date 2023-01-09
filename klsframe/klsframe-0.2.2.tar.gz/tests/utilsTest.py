import klsframe.utilities.utils as utils


def test_dict_to_table():
    a = {'Nombre': 'pedro', 'Apellidos': 'perez', 'Edad': 12, 'hobbies': ['skateboarding']}
    print('\n-----> Compact mode <-----\n')
    print(utils.dict_to_table(a, compact=True))
    print('\n-----> Extended mode <-----\n')
    print(utils.dict_to_table(a))


def test_join_by():
    listilla = ['Pablito', 'clavo', 3, 'clavitos']
    print(utils.join_by(' + ', listilla))
    print(utils.join_by(' + ', [1, 2, 3, 4, 5, 6]))
    exit(0)


def test_sort_dict():
    dicto = {'1': 'shit', '2': 'here', '3': 'we', '4': 'go', '5': 'again'}
    print(f"Alphabetical Key order:\n{utils.sort_dict(dicto)}")
    print(f"Alphabetical inverse Key order:\n{utils.sort_dict(dicto, reverse=True)}")
    print(f"Alphabetical value order:\n{utils.sort_dict(dicto, sortby='values')}")
    print(f"Alphabetical inverse value order:\n{utils.sort_dict(dicto, sortby='values', reverse=True)}")


if __name__ == '__main__':
    test_dict_to_table()
