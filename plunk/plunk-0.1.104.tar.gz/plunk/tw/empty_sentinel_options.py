# from tested import validate_codec
#
#
# Empty1 = type('Empty', (), {})()
# print("\nEmpty1 = type('Empty', (), {})()")
# print(f'{validate_codec(Empty1)=}')
#
#
# _Empty2 = type('Empty', (), {})
# _Empty2.__module__ = __name__
# Empty2 = _Empty2()
# print('\nsame, with _Empty2.__module__ = __name__; Empty2 = _Empty()')
# print(f'{validate_codec(Empty2)=}')
#
# _Empty3 = type('Empty', (), {})
# Empty3 = _Empty3()
# Empty3.__module__ = __name__
# print('\nwith Empty3.__module__ = __name__ (added to instance instead of class)')
# print(f'{validate_codec(Empty3)=}')
#
#
# class _Empty4:
#     ...
#
#
# Empty4 = _Empty4()
# print('\nDefining as ``class _Empty4: ...``')
# print(f'{validate_codec(Empty4)=}')
#
#
# class Empty5:
#     ...
#
#
# Empty5 = Empty5()  # overridding class (now no one else can use it!"
#
# print('\nOverwriding class Empty5 with instance Empty5')
# print(f'{validate_codec(Empty5)=}')
#
#
# class _Empty6:
#     def __repr__(self):
#         return f'Empty'
#
#
# Empty6 = _Empty6()
#
# print('\nLike Empty4, but with nice repr')
# print(f'{validate_codec(Empty6)=}')
#
# from i2 import mk_sentinel
#
# #
# #
# Empty9 = mk_sentinel('Empty9')
#
#
# print('\nWith boltons.typeutils.Sentinel')
# print(f'{validate_codec(Empty9)=}')
#
# import pickle
#
# # pickle.dumps(Empty9)


def foo():
    """
    >>> import pickle
    >>> class A: ...
    >>> unpickled_A = pickle.loads(pickle.dumps(A))
    >>> unpickled_A == A
    True
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
