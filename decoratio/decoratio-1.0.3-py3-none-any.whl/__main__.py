#!/usr/bin/env python3
import decoratio, sys
if __name__ == '__main__':
    if sys.argv[0] == __file__:
        sys.argv[0] = 'decoratio'
    decoratio.main()
